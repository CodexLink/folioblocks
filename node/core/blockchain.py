from asyncio import create_task, gather, get_event_loop
from copy import deepcopy
from datetime import datetime, timedelta
from hashlib import sha256
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
    HashableBlock,
    SearchContext,
    Transaction,
    Transactions,
)
from frozendict import frozendict
from orjson import dumps as export_to_json
from orjson import loads as import_raw_json_to_dict
from pympler.asizeof import asizeof

from core.consensus import AdaptedPoETConsensus
from core.constants import (
    ASYNC_TARGET_LOOP,
    BLOCK_HASH_LENGTH,
    BLOCKCHAIN_HASH_BLOCK_DIFFICULTY,
    BLOCKCHAIN_NODE_JSON_TEMPLATE,
    BLOCKCHAIN_RAW_PATH,
    BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS,
    AddressUUID,
    BlockchainIOAction,
    HashUUID,
    JWTToken,
    NodeRoles,
    ObjectProcessAction,
)
from core.dependencies import get_identity_tokens
from core.tasks import AsyncTaskQueue

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

        # * Required Variables for the Blockchain Operaetion.
        self.client_role = client_role
        self.auth_token = auth_tokens

        self.consensus_timer: datetime = (
            datetime.now()
        )  # TODO: This will be computed based on the information by the MASTER node on how much is being participated, along with its computed value based on the average mining and iteration.

        # * State and Variable References
        self.node_ready = False
        self.current_block_id: int = 1

        super().__init__()

    async def initialize(self) -> None:
        """
        A method that initialize resources needed for the blockchain system to work.

        TODO
        * If client_role is SIDE, then fetch or call update from the AdaptedPoERTConsensus to the MASTER node that is available. Also consider checking for unfinished tasks.
        """

        # Load the blockchain.

        self._chain: frozendict | None = await self._process_file_state(
            operation=BlockchainIOAction.TO_READ
        )

        # * Check if there's a context inside of the JSON. If there's none then create 1 to 3 genesis blocks.
        if (
            self._chain is not None
            and "chain" in self._chain
            and not self._chain["chain"]
        ):
            for _ in range(BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS):
                await self.create_genesis_block()  # * We can only afford to do per block since async will not detect other variable changes. I think we don't have a variable classifier that is meant to change dramatically without determined time. And that is 'volatile'.

    async def _append(
        self,
        *,
        context: Block | Transaction,
        auth_context: tuple[AddressUUID, JWTToken],
    ) -> None:
        """
        A method that is callad whenever a new block is ready to be inserted from the blockchain, both in-memory and to the file.

        Args:
            context (Block | Transaction): The context of the block as is.
            auth_context (tuple[AddressUUID, JWTToken]): Authentication attribute, not sure what to do on this one yet.

        TODO
        * Implement security of some sort, use `auth_context` or something. | We may use this and compute its hash for comparing context and also length.
        """
        if self._chain is not None:
            block_context = context.dict()
            block_context["contents"] = frozendict(block_context["contents"])
            self._chain["chain"].append(frozendict(block_context))
            await self._process_file_state(operation=BlockchainIOAction.TO_WRITE)

        else:
            logger.exception(
                "There's no 'chain' from the root dictionary of blockchain! This is a developer-implementation issue, please execute 'CTRL + BREAK' as possible and report to the developers as soon as possible!"
            )
            input()

    # Overwrites existing buffer from the frozendict if consensus has been established.
    async def _process_file_state(
        self,
        *,
        operation: BlockchainIOAction,
    ) -> frozendict | None:
        if operation in BlockchainIOAction:
            async with aopen(
                BLOCKCHAIN_RAW_PATH,
                "w" if operation == BlockchainIOAction.TO_WRITE else "r",
            ) as content_buffer:

                if operation == BlockchainIOAction.TO_WRITE:
                    await content_buffer.write(
                        export_to_json(
                            self._chain, default=self.serialize_to_file_blockchain
                        ).decode("utf-8")
                    )
                    return None

                else:
                    raw_data = await content_buffer.read()
                    partial_deserialized_data = import_raw_json_to_dict(raw_data)
                    deserialized_data = self.load_deserialized_blockchain(
                        partial_deserialized_data
                    )
                    logger.info(
                        f"Chain has been loaded from the file to the in-memory!"
                    )
                    return deserialized_data

        logger.exception(
            f"Supplied value at 'operation' is not a valid enum! Got {operation} ({type(operation)}) instead."
        )
        return None

    def serialize_to_file_blockchain(self, o: frozendict) -> dict[str, Any]:
        """
        A method that serializes the python objects to the blockchain file. This represents the JSON form of the blockchain.

        Args:
            o (frozendict): The whole chain, wrapped in frozendict.

        Raises:
            TypeError: Cast TypeError when the constraint from the `o` is not followed.

        Returns:
            dict[str, Any]: Returns the JSON form of the blockchain that is in-memory.

        Note:
        *  By this point, I still haven't consider for scalability and its impact from processing such data.
        * Until there's an impact, I will implement in-memory caching to reduce processing time and insert only data that is missing from the data pool.
        """

        if isinstance(o, frozendict):  # * Cast mutability on the whole chain.
            _o = dict(deepcopy(o))
            for block_idx, each_block in enumerate(_o["chain"]):
                # * Then cast mutability from the whole block of the chain.
                _o["chain"][block_idx] = dict(each_block)

                # * Lastly, cast mutability to the content of the whole block of the chain.
                _o["chain"][block_idx]["contents"] = dict(each_block["contents"])

            return _o

        raise TypeError

    def load_deserialized_blockchain(
        self,
        context: dict[str, Any],
    ) -> frozendict:
        """
        A method that deserializes the blockchain into an immutable dictionary (frozendict) from the outsourced-data of the blockchain file.

        Args:
            context (dict[str, Any]): The consumable data (type-compatible) that is loaded by the orjson.

        Returns:
            frozendict: Returns the immutable version of the given `context`.
        """

        # *  Ensure that the wrapped object is 'dict' regardless of their recent forms.
        if isinstance(context, dict):

            for dict_idx, dict_data in enumerate(context["chain"]):
                # * For every block, we have to deserialize (1) timestamps to `datetime`, (2) `content` to immutable 'dict' (frozendict) and transactions.

                context["chain"][dict_idx]["contents"] = frozendict(
                    dict_data["contents"]
                )
                # * Then, make the whole block immutable and insert it as reference from the blockchain.
                context["chain"][dict_idx] = frozendict(dict_data)

            logger.info(
                "The blockchain context from the file has been loadede in-memory and is secured by immutability!"
            )
            return frozendict(context)

        logger.exception(
            f"The given `context` is not a valid dictionary object! | Received: {context} ({type(context)})."
        )

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
                else HashUUID(self.get_last_block.hash_block),  # type: ignore
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
