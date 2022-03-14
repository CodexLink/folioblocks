from asyncio import create_task, get_event_loop
from datetime import datetime
from hashlib import sha256
from json import dumps as export_to_json
from json import loads as import_raw_json_to_dict
from logging import Logger, getLogger
from random import randint
from time import time
from typing import Any

import aiofiles
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

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

# TODO: Should we seperate consensus from this class?
class BlockchainMechanism(AsyncTaskQueue, AdaptedPoETConsensus):
    def __init__(
        self,
        auth_tokens: tuple[AddressUUID, JWTToken],
        client_role: NodeRoles,
    ) -> None:

        # TODO: After finalization, seperate some methods and attributes for the SIDE and MASTER.
        # Required since this class will be invoked no matter what the role of the client instance is.
        self.client_role = client_role
        self.auth_token = auth_tokens
        self.consensus_timer: datetime | None = None
        self.blockchain_ready = False

        # TODO: Add implementation for when there's a concurrency of new data, then await all of them then sort then insert.

        super().__init__()

    async def initialize(self) -> None:
        # First check for the file if it is valid de-serializable.
        # ! Raise error if it contains nothing. The processor of the file for the blockchain should already have a context.

        # If client_role is SIDE, then fetch or call update from the AdaptedPoERTConsensus to the MASTER node that is available. Also consider checking for unfinished tasks.

        # TODO.
        # ! Check if there's a context inside of the JSON. If there's none then create 1 to 3 genesis blocks.

        # If everything is okay, then load the blockchain.
        # self._chain: dict[str, list[frozendict]] = frozendict({"chain": []})
        self._chain = {}

        self._chain = await self._process_file_state(
            operation=BlockchainIOAction.TO_READ, chain=self._chain
        )

        # TODO: try running this if we were able to finish most parts of the blockchain. 3 to 5 times.
        for _ in range(randint(1, 4)):
            create_task(
                self.create_genesis_block()
            )  # * Add this to async queue then await for the return with the sorted data based on block id.

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

        await self._process_file_state(
            operation=BlockchainIOAction.TO_WRITE, chain=self._chain
        )

    # Overwrites existing buffer from the frozendict if consensus has been established.
    # TODO: Make the existing file loaded and deserialize it.
    # TODO: Create an attribute that tells if we are ready to do some processing or not. | PREPARED.
    # TODO: This is gonna be useful for asnyc tasks queue that we have for the consensus implementation.
    async def _process_file_state(
        self, *, operation: BlockchainIOAction, chain: dict[str, list[frozendict]] | Any
    ) -> Any | None:  # ! TYPES HAS BEEN COMPLICATED, WILL RESOLVE LATER.
        async with aiofiles.open(
            BLOCKCHAIN_RAW_PATH,
            "w" if operation == BlockchainIOAction.TO_WRITE else "r",
        ) as writer:
            if chain and operation == BlockchainIOAction.TO_WRITE:
                # TODO for the r. or r+ whatever.
                await writer.write(
                    export_to_json(
                        await self._process_objects(
                            action=ObjectProcessAction.TO_SERIALIZE,
                            context=dict(chain),
                        )
                    )
                )
            elif chain and operation == BlockchainIOAction.TO_READ:
                # First we fetch something form the file.
                raw_data = await writer.read()
                serialized_data = import_raw_json_to_dict(raw_data)

                # Then we deserialize it to something that represents the default of self._chain.
                logger.warning("Chain has been loaded from the file to the in-memory.")
                return await self._process_objects(
                    action=ObjectProcessAction.TO_SERIALIZE, context=serialized_data
                )

    async def _process_objects(
        self, *, action: ObjectProcessAction, context: dict[str, list[frozendict] | str]
    ) -> dict[str, list[frozendict]] | frozendict:  # TODO: Annotate this.
        """
        An async function that deserialize or serialize objects for process. Probably used a lot by the _overwrite_or_read_file_state.

        Args:
            action (ObjectProcessAction): _description_
            context (dict[str, list[frozendict]]): _description_
        """
        #

        # * Check the structure in the initial phase before processing.
        # - Ensure that the wrapped object is 'dict' regardless of their recent forms. Please process it before feeding it from this function.
        if action in ObjectProcessAction and isinstance(context, dict):

            # TODO: Post Feature (Low Priority) | Properly set types.
            for dict_idx, dict_data in enumerate(context["chain"]):

                # * Check internal structure.
                # - Ensure that we are only dealing either 'dict' or 'frozendict' at its respected 'action'. Otherwise we raise an exception.
                # * Congrats, I made hard to be readable, but hey less codespace.

                context["chain"][dict_idx] = (  # type: ignore # Reports something about indexing.
                    dict(dict_data)
                    if isinstance(dict_data, frozendict)
                    and action == ObjectProcessAction.TO_SERIALIZE
                    else frozendict(dict_data)
                )

                # @o Since we know that we have a format, meaning we don't need to assume, statically declare to modify timestamp to be compatible in JSON serialization.
                context["chain"][dict_idx]["timestamp"] = (  # type: ignore
                    context["chain"][dict_idx]["timestamp"].isoformat()  # type: ignore
                    if ObjectProcessAction.TO_SERIALIZE
                    and isinstance(context["chain"][dict_idx]["timestamp"], datetime)  # type: ignore
                    else datetime.fromisoformat(context["chain"][dict_idx]["timestamp"])  # type: ignore
                )  # type: ignore
                # ! Here me out, this is ugly, but elegant for some reason. Don't blame my code formatter for this.

            # * When a function contains `TO_DESERIALIZE`, do some additional work by wrapping the processed data with frozendict().
            if action == ObjectProcessAction.TO_SERIALIZE:
                context = frozendict(context)

            return context

        print("There something wrong.")  # TODO: Create an exception of this.

    async def create_genesis_block(self) -> None:
        """
        Generates a block, hash it and append it within the context of the blockchain, for both the file and the in-memory.
        """

        # Check for the genesis_block before inserting it.

        genesis_block: Block = Block(
            id=1,
            nonce=None,
            block_size=None,
            validator=get_identity_tokens()[0],
            prev_hash_block=HashUUID("0" * BLOCK_HASH_LENGTH),
            hash_block=None,
            next_hash_block=None,
            transactions=None,
            timestamp=datetime.now(),
        )

        ensured_future_hash_block = get_event_loop().run_in_executor(
            None, self.mine_block, genesis_block
        )

        genesis_block.nonce, genesis_block.hash_block = await ensured_future_hash_block
        genesis_block.block_size = self.get_sizeof(genesis_block)

        await self._append(genesis_block, get_identity_tokens())

    def get_sizeof(self, block: Block) -> int:
        return asizeof(block)

    async def create_block(
        self,
    ) -> None:  # We need to trigger this so that it will be inserted.
        pass

    async def create_transaction(self) -> None:
        pass

    # ! We may need thread pool here if we have multiple things happening.
    def mine_block(self, *, block: Block) -> tuple[int, HashUUID]:
        # If success, then return the hash of the block based from the difficulty.
        prev: float = time()
        nth: int = 1

        logger.debug(f"Attempting to mine the Block #{block.id} ...")

        while True:
            # https://stackoverflow.com/questions/869229/why-is-looping-over-range-in-python-faster-than-using-a-while-loop, not sure if this works here as well.

            block.nonce = randint(0, 1 * 1000000000000000)
            computed_hash: HashUUID = HashUUID(
                sha256(block.json().encode("utf-8")).hexdigest()
            )

            if (
                computed_hash[:BLOCKCHAIN_HASH_BLOCK_DIFFICULTY]
                == "0" * BLOCKCHAIN_HASH_BLOCK_DIFFICULTY
            ):
                logger.info(
                    f"Block #{block.id} with a nonce value of {block.nonce} has a resulting hash value of `{computed_hash}`, which has been mined for {time() - prev} under {nth} iteration/s!"
                )
                return block.nonce, computed_hash

            nth += 1
            continue

    # I think this should work only on miner nodes.
    async def update_chain(self) -> None:
        pass

    # Ensure to follow the rule that we made last time.
    async def search_for(self, type: str, uid: AddressUUID | str) -> None:
        pass

    @property
    def is_blockchain_ready(self) -> bool:
        return self.blockchain_ready

    @property
    def get_last_block(self) -> frozendict:
        return self._chain[:-1]  # ! This is not working.

    # A set of tasks to run from the main module.
    # * Note that I cannot invoke the fastapi_utils.run_every here.
    # ! TO BE TESTED.
    async def call_required_tasks(self) -> None:
        pass

    async def close(self) -> None:
        pass


# # This approach was (not completely) taken from stackoverflow.
# * Please refer to the node/core/email.py:132 for more information.
blockchain_service: BlockchainMechanism | None = None


def get_blockchain_instance_or_initialize(
    role: NodeRoles | None = None,
) -> BlockchainMechanism:

    global blockchain_service

    token_ref = get_identity_tokens()

    if token_ref is None:
        logger.critical(
            "There are no identity tokens inferred from your instance. A login authentication should not bypass this method from running. This a developer issue, please report as possible or try again."
        )

    # Resolve.
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

    return blockchain_service  # type: ignore # Not sure how can I comprehend where's the mistake, or I just got caffeine overdose to understand mypy's complaint.
