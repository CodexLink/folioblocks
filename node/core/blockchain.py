from logging import Logger, getLogger

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
from node.core.constants import JWTToken

logger = getLogger(ASYNC_TARGET_LOOP)

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
        self._chain: frozendict = frozendict()

    # Write to file or write_to_buffer.
    async def _append(self, context: Block | Transaction) -> None:
        pass

    # Overwrites existing buffer from the frozendict if consensus has been established.
    async def _overwrite(self) -> None:
        pass

    async def create_genesis_block(self) -> None:
        """
        Generates a block, hash it and append it within the context of the blockchain, for both the file and the in-memory.
        """
        # for

        # genesis_block: block = block(
        #     id=1,
        #     nonce=none,
        #     prev_block = "0" * block_hash_length,
        #     next_hash_block=none,
        #     transactions=[
        #         transaction(

        #         )
        #         ]
        #     )



        # ! Add some protection to avoid polluting the blockchain.
        return

    async def get_length(self) -> None:
        pass

    async def create_block(self) -> None:
        pass

    async def create_transaction(self) -> None:
        pass

    async def mine_block(self) -> None:
        pass

    # I think this should work only on miner nodes.
    async def update_chain(self) -> None:
        pass

    # Ensure to follow the rule that we made last time.
    async def search_for(self, type: str, uid: AddressUUID | str) -> None:
        pass

    @property
    def get_last_block(self) -> frozendict:
        return self._chain[:-1] # This is not working.

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


def get_blockchain_instance_or_initialize(*, ) -> Blockchain:
    global blockchain_service

    if blockchain_service is None:
        blockchain_service = Blockchain(
            client_role
        )

    return blockchain_service
