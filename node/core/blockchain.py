from asyncio import create_task, gather, get_event_loop
from datetime import datetime, timedelta
from hashlib import sha256
from orjson import dumps as export_to_json
from orjson import loads as import_raw_json_to_dict
from logging import Logger, getLogger
from random import randint
from sys import maxsize as MAX_INT_PYTHON
from time import time
from typing import Any

from aiofiles import open as aopen
from blueprint.schemas import (
    Block,
    Blockchain,
    Blocks,
    SearchContext,
    Transaction,
    Transactions,
)
from frozendict import frozendict
from pympler.asizeof import asizeof

from core.consensus import AdaptedPoETConsensus
from core.constants import (
    ASYNC_TARGET_LOOP,
    BLOCK_HASH_LENGTH,
    BLOCKCHAIN_HASH_BLOCK_DIFFICULTY,
    BLOCKCHAIN_NODE_JSON_TEMPLATE,
    BLOCKCHAIN_RAW_PATH,
    AddressUUID,
    BlockchainIOAction,
    HashUUID,
    JWTToken,
    NodeRoles,
    ObjectProcessAction,
)
from core.dependencies import get_identity_tokens
from core.tasks import AsyncTaskQueue
from blueprint.schemas import HashableBlock
from copy import copy

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

# TODO: Should we seperate consensus from this class?
class BlockchainMechanism(AsyncTaskQueue, AdaptedPoETConsensus):
    def __init__(
        self,
        *,
        auth_tokens: tuple[AddressUUID, JWTToken],
        client_role: NodeRoles,
    ) -> None:

        # TODO: After finalization, seperate some methods and attributes for the SIDE and MASTER.
        # Required since this class will be invoked no matter what the role of the client instance is.
        self.client_role = client_role
        self.auth_token = auth_tokens
        self.consensus_timer: datetime = (
            datetime.now()
        )  # TODO: This will be computed based on the information by the MASTER node on how much is being participated, along with its computed value based on the average mining and iteration.
        self.blockchain_ready = False
        self.node_ready = False
        self.current_block_id: int = 1

        # TODO: Add implementation for when there's a concurrency of new data, then await all of them then sort then insert.

        super().__init__()

    async def initialize(self) -> None:
        # First check for the file if it is valid de-serializable.
        # ! Raise error if it contains nothing. The processor of the file for the blockchain should already have a context.

        # If client_role is SIDE, then fetch or call update from the AdaptedPoERTConsensus to the MASTER node that is available. Also consider checking for unfinished tasks.

        # * Check if there's a context inside of the JSON. If there's none then create 1 to 3 genesis blocks.
        # If everything is okay, then load the blockchain.
        self._chain: frozendict = frozendict(
            BLOCKCHAIN_NODE_JSON_TEMPLATE
        )  # Also classified as type: dict[str, list[frozendict]]

        # print("INITIAL LOAD:", self._chain)

        self._chain = await self._process_file_state(
            operation=BlockchainIOAction.TO_READ, chain=self._chain
        )

        # print("AFTER LOADING:", self._chain)

        # TODO: try running this if we were able to finish most parts of the blockchain. 3 to 5 times.
        for _ in range(10):
            await self.create_genesis_block()  # # We can only afford to do per block since async will not detect other variable changes. I think we don't have a variable classifier that is meant to change dramatically without determined time. And that is 'volatile'.

    # Write to file or write_to_buffer.
    async def _append(
        self,
        *,
        context: Block | Transaction,
        auth_context: tuple[AddressUUID, JWTToken],
    ) -> None:
        # I handle only the context at this moment for now.

        # TODO: Add security mechanism here.
        # * We may use this and compute its hash for comparing context and also length.

        # TODO: Add it in the file or something idk.
        self._chain["chain"].append(frozendict(context.dict()))

        # * When these blocks were appended, we know that we didn't handle its insertion to be sorted, therefore lets sort it here by renewing it since we wrapped our dict with frozendict.
        # print("AFTER APPENDING:", self._chain)
        await self._process_file_state(
            operation=BlockchainIOAction.TO_WRITE, chain=self._chain
        )

    # Overwrites existing buffer from the frozendict if consensus has been established.
    # TODO: Make the existing file loaded and deserialize it.
    # TODO: Create an attribute that tells if we are ready to do some processing or not. | PREPARED.
    # TODO: This is gonna be useful for asnyc tasks queue that we have for the consensus implementation.
    async def _process_file_state(
        self, *, operation: BlockchainIOAction, chain: frozendict
    ) -> Any | None:  # ! TYPES HAS BEEN COMPLICATED, WILL RESOLVE LATER.
        if operation in BlockchainIOAction:
            async with aopen(
                BLOCKCHAIN_RAW_PATH,
                "w" if operation == BlockchainIOAction.TO_WRITE else "r",
            ) as content_buffer:

                if chain and operation == BlockchainIOAction.TO_WRITE:
                    await content_buffer.write(
                        export_to_json(
                            await self._process_block_object(
                                action=ObjectProcessAction.TO_SERIALIZE,
                                context=dict(chain),
                            )
                        ).decode("utf-8")
                    )

                else:
                    # First we fetch something form the file.
                    raw_data = await content_buffer.read()
                    print("FILE_READ:", raw_data)
                    serialized_data = import_raw_json_to_dict(raw_data)

                    # Then we deserialize it to something that represents the default of self._chain.
                    logger.info("Chain has been loaded from the file to the in-memory!")
                    return await self._process_block_object(
                        action=ObjectProcessAction.TO_DESERIALIZE,
                        context=serialized_data,
                    )

        logger.exception(
            f"Supplied value at 'operation' is not a valid enum! Got {operation} ({type(operation)}) instead."
        )

    async def _process_block_object(
        self,
        *,
        action: ObjectProcessAction,
        context: dict[str, list[frozendict] | dict[str, str]],
    ) -> Any:  # TODO: Annotate this.
        """
        An async function that deserialize or serialize objects for process. Probably used a lot by the _overwrite_or_read_file_state.

        Args:
            action (ObjectProcessAction): _description_
            context (dict[str, list[frozendict]]): _description_
        """
        if action in ObjectProcessAction and isinstance(context, dict):
            # * Check the structure in the initial phase before processing.
            # - Ensure that the wrapped object is 'dict' regardless of their recent forms. Please process it before feeding it from this function.

            # * We need to copy the class container since we are going to modify its contents for serialization. Not copying it will result in references sharing the same changes.

            # TODO: Since it automatically appends then we can just process this function to do it per thing.
            # TODO: Then we ensure that this dictionary knows about it. We need to compare it to the self._chain for integrity purposes, which means, we get two seperate copies.

            # Set up initial run before treating other objects.
            out_serialized_data = BLOCKCHAIN_NODE_JSON_TEMPLATE.copy()
            ref_container = (
                context.copy()
                if action == ObjectProcessAction.TO_SERIALIZE
                else context
            )

            for dict_idx, dict_data in enumerate(ref_container["chain"]):
                # * Check internal structure.
                # - Ensure that we are only dealing either 'dict' or 'frozendict' at its respected 'action'. Otherwise we raise an exception.
                # * Congrats, I made hard to be readable, but hey less codespace.

                resolved_shadow_block = (
                    dict(dict_data)
                    if isinstance(dict_data, frozendict)
                    and action == ObjectProcessAction.TO_SERIALIZE
                    else frozendict(dict_data)
                )

                if action == ObjectProcessAction.TO_SERIALIZE:
                    logger.debug(
                        f"Block #{resolved_shadow_block['id']} has been appended to the temporary blockchain."
                    )
                    out_serialized_data["chain"].append(resolved_shadow_block)
                else:
                    logger.debug(
                        f"Block #{resolved_shadow_block['id']} has been inserted to the actual blockchain context."
                    )
                    ref_container["chain"][dict_idx] = resolved_shadow_block

            if action == ObjectProcessAction.TO_SERIALIZE:
                return out_serialized_data
            else:
                # * When a function contains `TO_DESERIALIZE`, do some additional work by wrapping the processed data with frozendict().E:
                ref_container = frozendict(ref_container)
                return ref_container

        print("There something wrong.")  # TODO: Create an exception of this.

    async def create_genesis_block(self) -> None:
        """
        Generates a block, hash it and append it within the context of the blockchain, for both the file and the in-memory.
        """

        # Check for the genesis_block before inserting it.
        # TODO: We may need to use create_block since we have an unallocated_block.

        mined_genesis_block = await get_event_loop().run_in_executor(
            None, self.mine_block, self.create_block(transactions=None)
        )

        await self._append(
            context=mined_genesis_block, auth_context=get_identity_tokens()
        )

    def get_sizeof(self, *, block: Block) -> int:
        return asizeof(block)

    def calculate_sleep_time(
        self, *, mine_duration: float | int, mine_iteration: int
    ) -> None:
        self.consensus_timer = datetime.now() + timedelta(
            seconds=mine_duration + (mine_iteration / 1000)
        )

    def set_node_state(self) -> None:
        self.node_ready = True if datetime.now() >= self.consensus_timer else False

    def create_block(
        self,
        *,
        transactions: list[Transaction] | None,
    ) -> Block:

        # @o When building a block, we first have to consider that there are some properties were undefined. The nonce, block_size, and hash_block.
        # @o With this, we need to seperate the contents of the block, providing a way from the inside of the block to be hashable and identifiable for hash verification.
        # ! Several properties have to be seperated due to their nature of being able to overide the computed hash block.

        _block: Block = Block(
            id=self.current_block_id,
            block_size=None,  # * Unsolvable at instantiation but can be filled before returning it.
            hash_block=None,  # ! Unsolvable, mine_block will handle it.
            contents=HashableBlock(
                nonce=None,  # ! Unsolvable, these are determined during the process of mining.
                validator=get_identity_tokens()[0],
                prev_hash_block=HashUUID("0" * BLOCK_HASH_LENGTH)
                if self.get_last_block is None
                else HashUUID(self.get_last_block.hash_block),
                transactions=transactions,
                timestamp=datetime.now(),
            ),
        )

        _block.block_size = asizeof(_block.contents.json())
        self.current_block_id += 1

        return _block

    async def create_transaction(self) -> None:
        return

    # # Cannot do keyword arguments here as per stated on excerpt: https://stackoverflow.com/questions/23946895/requests-in-asyncio-keyword-arguments
    def mine_block(self, block: Block) -> Block:
        # If success, then return the hash of the block based from the difficulty.
        prev: float = time()
        nth: int = 1

        logger.debug(f"Attempting to mine the block #{block.id} ...")

        while True:
            # https://stackoverflow.com/questions/869229/why-is-looping-over-range-in-python-faster-than-using-a-while-loop, not sure if this works here as well.

            block.contents.nonce = randint(0, MAX_INT_PYTHON)
            computed_hash: HashUUID = HashUUID(
                sha256(block.json().encode("utf-8")).hexdigest()
            )

            if (
                computed_hash[:BLOCKCHAIN_HASH_BLOCK_DIFFICULTY]
                == "0" * BLOCKCHAIN_HASH_BLOCK_DIFFICULTY
            ):
                block.hash_block = computed_hash
                logger.info(
                    f"Block #{block.id} with a nonce value of {block.contents.nonce} has a resulting hash value of `{computed_hash}`, which has been mined for {time() - prev} under {nth} iteration/s!"
                )
                self.calculate_sleep_time(
                    mine_duration=time() - prev, mine_iteration=nth
                )
                return block

            nth += 1

    # I think this should work only on miner nodes.
    async def update_chain(self) -> None:
        pass

    # Ensure to follow the rule that we made last time.
    async def search_for(self, *, type: str, uid: AddressUUID | str) -> None:
        pass

    @property
    def is_blockchain_ready(self) -> bool:
        return self.blockchain_ready

    @property
    def get_last_block(self) -> Block | None:
        # ! This return seems confusing but I have to sacrafice for my own sake of readability.
        # @o First we access the list by calling the key 'chain'.
        # @o Since we got to the list, we might wanna get the last block by slicing the list with the use of its own length - 1 to get the last block.
        # @o But before we do that, ensure that last item has a content. Accessing the last item with the use of index while it doesn't contain anything will result in `IndexError`.

        if len(self._chain["chain"]):
            last_block_ref = Block.parse_obj(
                self._chain["chain"][len(self._chain["chain"]) - 1 :][0]
            )
            logger.debug(f"Last block has been fetched. Context | {last_block_ref}")
            return last_block_ref

        logger.warning("There's no block inside blockchain.")

    async def close(self) -> None:
        pass


# # This approach was (not completely) taken from stackoverflow.
# * Please refer to the node/core/email.py:132 for more information.
blockchain_service: BlockchainMechanism | None = None


def get_blockchain_instance(
    *,
    role: NodeRoles | None = None,
) -> BlockchainMechanism:

    global blockchain_service
    token_ref: tuple[AddressUUID, JWTToken] | None = get_identity_tokens()

    logger.debug("Initializing or returning blockchain instance ...")

    if role and blockchain_service is None and token_ref is not None:
        # # Note that this will create an issue later when we tried SIDE node mode later on.
        blockchain_service = BlockchainMechanism(
            auth_tokens=token_ref,
            client_role=role,
        )

    # If there are no resulting objective, then we can log this as an error, otherwise return the object.
    if blockchain_service is None:
        logger.critical(
            "Unresolved role from this instance. Please specify your role. This may be a developer issue, please report this as possible or try again."
        )

    if token_ref is None:
        logger.critical(
            "There are no identity tokens inferred from your instance. A login authentication should not bypass this method from running. This a developer issue, please report as possible or try again."
        )

    logger.debug("Blockchain instance retrieved, returning to the requestor ...")
    return blockchain_service  # type: ignore # Not sure how can I comprehend where's the mistake, or I just got caffeine overdose to understand mypy's complaint.
