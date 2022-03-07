from blueprint.schemas import (
    Block,
    Blockchain,
    Blocks,
    SearchContext,
    Transaction,
    Transactions,
)

from core.constants import AddressUUID
from core.tasks import AsyncTaskQueue
from core.consensus import AdaptedPoETConsensus

# TODO: Should we seperate consensus from this class?
class Blockchain(AsyncTaskQueue, AdaptedPoETConsensus):
    def __init__(self) -> None:
        super().__init__()

    def __ainit__(self) -> None:
        pass

    # Write to file or write_to_buffer.
    async def _write(self):
        pass

    async def _append(self):
        pass

    async def _overwrite(self):
        pass

    @staticmethod
    def initialize_genesis_block() -> Transaction:
        return Transaction()

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
    async def get_last_block(self) -> Block:
        return Block()

    # A set of tasks to run from the main module.
    # * Note that I cannot invoke the fastapi_utils.run_every here.
    # ! TO BE TESTED.
    async def call_required_tasks(self) -> None:
        pass

    #  sync_chain


# # This approach was (not completely) taken from stackoverflow.
# * Please refer to the node/core/email.py:132 for more information.
blockchain_service: Blockchain | None = None


def get_blockchain_instance_or_initialize() -> Blockchain:
    global blockchain_service

    if blockchain_service is None:

        blockchain_service = Blockchain()

    return blockchain_service
