from consensus import Consensus
from node.core.constants import AddressUUID


class Blockchain(Consensus):
    async def __ainit__(self) -> None:
        pass

    async def create_block(self) -> None:
        pass

    async def get_last_block(self) -> None:
        pass

    async def search_for(self, type: str, uid: AddressUUID | str) -> None:
        pass

    async def initiate_consensus(self) -> None:
        pass

    async def resolve_consensus(self) -> None:
        pass

    #  sync_chain


# if __main__ == "__mp_main__":
# pass
# email_service: Blockchain = Blockchain()
