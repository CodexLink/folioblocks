from fastapi import Depends as Depends
from typing import Any
from utils.constants import AddressUUID as AddressUUID, BlockID as BlockID, TxID as TxID

explorer_router: Any

async def get_blockchain() -> None: ...
async def get_blocks(block_count: Union[int, None] = ..., page: Union[int, None] = ...): ...
async def get_certain_block(block_id: BlockID, tx_count: Union[int, None] = ..., page: Union[int, None] = ...): ...
async def get_transactions(tx_count: Union[int, None] = ..., page: Union[int, None] = ...): ...
async def get_particular_transaction(tx_id: TxID): ...
async def get_addresses(addr_count: Union[int, None] = ..., page: Union[int, None] = ...): ...
async def get_particular_addresses(address_uuid: AddressUUID, tx_count: Union[int, None] = ..., page: Union[int, None] = ...): ...
async def search_in_explorer(context: str = ...): ...