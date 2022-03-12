from argparse import Namespace
from logging import Logger, getLogger
from random import randint

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
from hashlib import sha256

from core.constants import BLOCK_HASH_LENGTH
from core.consensus import AdaptedPoETConsensus
from core.constants import ASYNC_TARGET_LOOP, AddressUUID, NodeRoles
from core.tasks import AsyncTaskQueue
from core.constants import HashUUID, JWTToken
from datetime import datetime

from core.dependencies import get_identity_token
from pympler.asizeof import asizeof
from time import time

from node.core.constants import BLOCKCHAIN_HASH_BLOCK_DIFFICULTY, BLOCKCHAIN_RAW_PATH

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

# TODO: Should we seperate consensus from this class?
class Blockchain(AsyncTaskQueue, AdaptedPoETConsensus):
    def __init__(
        self,
        client_role: NodeRoles,
        auth_token: JWTToken | None = None,
    ) -> None:
        # Required since this class will be invoked no matter what the role of the client instance is.
        self.client_role = client_role
        self.auth_token = auth_token

        super().__init__()

    async def initialize(self) -> None:
        # First check for the file if it is valid de-serializable.
        # ! Raise error if it contains nothing. The processor of the file for the blockchain should already have a context.

        # If client_role is SIDE, then fetch or call update from the AdaptedPoERTConsensus to the MASTER node that is available.

        # ! Check if there's a context inside of the JSON. If there's none then create 3 to 5 genesis blocks from the blockchain with the create_genesis_block.

        # If everything is okay, then load the blockchain.
        self._chain: dict[str, list[frozendict]] = frozendict(
            {"chain": frozendict({})}
        )  # TODO.

    # TODO: Not sure if this should be here or from the processor.
    async def serialize(self) -> None:
        pass

    # Write to file or write_to_buffer.
    async def _append(
        self, context: Block | Transaction, auth_context: tuple[AddressUUID, JWTToken]
    ) -> None:
        # I handle only the context at this moment for now.

        # TODO: Add security mechanism here.
        # TODO: Add it in the file or something idk.
        # * We may use this and compute its hash for comparing context and also length.

        self._chain["chain"].append(frozendict(context.json()))

    # Overwrites existing buffer from the frozendict if consensus has been established.
    async def _overwrite_file_state(self) -> None:
        async with aiofiles.open(BLOCKCHAIN_RAW_PATH, "wb") as writer:
            pass
            await writer.write()

    async def create_genesis_block(self) -> None:
        """
        Generates a block, hash it and append it within the context of the blockchain, for both the file and the in-memory.
        """

        # Check for the genesis_block before inserting it.

        genesis_block: Block = Block(
            id=1,
            nonce=None,
            block_size=None,
            validator=get_identity_token()[0],
            prev_hash_block=HashUUID("0" * BLOCK_HASH_LENGTH),
            hash_block=None,
            next_hash_block=None,
            transactions=None,
            timestamp=datetime.now(),
        )

        genesis_block.hash_block = await self.mine_block(genesis_block)
        genesis_block.block_size = self.get_sizeof(genesis_block)

        await self._append(genesis_block, get_identity_token())

    def get_sizeof(self, block: Block) -> int:
        return asizeof(block)

    async def create_block(
        self,
    ) -> None:  # We need to trigger this so that it will be inserted.
        pass

    async def create_transaction(self) -> None:
        pass

    async def mine_block(self, block: Block) -> HashUUID:
        # If success, then return the hash of the block based from the difficulty.
        prev: float = time()
        nth = 1

        logger.debug(f"Attempting to mine the block {block.id} ...")

        while True:
            # https://stackoverflow.com/questions/869229/why-is-looping-over-range-in-python-faster-than-using-a-while-loop, not sure if this works here as well.

            block.nonce = randint(0, 100000000)
            computed_hash: HashUUID = HashUUID(
                sha256(block.json().encode("utf-8")).hexdigest()
            )

            if (
                computed_hash[:BLOCKCHAIN_HASH_BLOCK_DIFFICULTY]
                == "0" * BLOCKCHAIN_HASH_BLOCK_DIFFICULTY
            ):
                logger.info(
                    f"Block #{block.id} with hash `{block.hash_block}` has been mined for {time() - prev} under {nth} iteration/s!"
                )
                return computed_hash

            nth += 1
            continue

    # I think this should work only on miner nodes.
    async def update_chain(self) -> None:
        pass

    # Ensure to follow the rule that we made last time.
    async def search_for(self, type: str, uid: AddressUUID | str) -> None:
        pass

    @property
    def get_last_block(self) -> frozendict:
        return self._chain[:-1]  # This is not working.

    # A set of tasks to run from the main module.
    # * Note that I cannot invoke the fastapi_utils.run_every here.
    # ! TO BE TESTED.
    async def call_required_tasks(self) -> None:
        pass

    async def close(self) -> None:
        pass

    #  sync_chain


# # This approach was (not completely) taken from stackoverflow.
# * Please refer to the node/core/email.py:132 for more information.
blockchain_service: Blockchain | None = None


def get_blockchain_instance_or_initialize(_instances: Namespace) -> Blockchain:
    global blockchain_service

    if blockchain_service is None:
        blockchain_service = Blockchain(
            # client_role
        )

    return blockchain_service
