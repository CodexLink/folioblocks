"""
Node Component, Explorer API

It contains the necessary API endpoints for the nodes who will participate in the blockchain. Note that some of these endpoints will be exclusive under 'master' node role. Also, note that most of these endpoints require JWT token to access.
It contains API endpoints that can be accessed by the Explorer Frontend UI (combined with the Dashboard UI @ 'web/' directory). Note that the base endpoint will not be the same from Frontend API endpoints.That is intended so that there will be no confusion, upon selection of the endpoint to use.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

if __name__ == "__main__":
    raise SystemExit(
        "This {__file__} (module) should not be executed as an entrypoint code! This module contains API endpoints for the Node API, which is an extension of this Explorer API."
    )

from blueprint.schemas import (
    Block,
    Blockchain,
    Transaction,
)
from core.constants import (
    QUERY_CURRENT_INDEX_NAME_DESCRIPTION,
    QUERY_CURRENT_INDEX_PAGE_NAME,
    QUERY_TRANSACTION_RETURN_DESCRIPTION,
    QUERY_TRANSACTION_RETURN_NAME,
    AddressUUID,
    BaseAPI,
    BlockID,
    ExplorerAPI,
    ItemReturnCount,
    TxID,
)
from fastapi import APIRouter, Depends, Query

"""
# Regarding Dependency Injection on this endpoint.

Note that we are iterating through JSON and we might need the folowing:
- AsyncIterator
- AIOFiles-related JSON Reader and Writer

But before we deal with this matter, we need to ensure that we can first do the following:
- Blockchain File and Block Finalization.

Since this endpoint is just returning by reading through file, we can make this one good to go or a little bit easy but not underestimated.

"""

explorer_router = APIRouter(
    prefix="/explorer",
    tags=[BaseAPI.EXPLORER.value],
)

# ! Note: Most of these operations require the need of the original JSON of the master node. From there, we may be able to cache the output.


@explorer_router.get(
    "explorer/",
    tags=[
        ExplorerAPI.GENERAL_FETCH.value,
        ExplorerAPI.LIST_FETCH.value,
    ],
    response_model=Blockchain,
    summary="Fetch the context of the blockchain, formatted for displaying in the web.",
    description="An API endpoint that parses the current state of the blockchain under JSON-format for data display in the web. Note that this returns a fixed amount of data.",
)
async def get_blockchain() -> None:
    return


@explorer_router.get(
    "/blocks",
    tags=[ExplorerAPI.LIST_FETCH.value, ExplorerAPI.BLOCK_FETCH.value],
    response_model=list[Block],
    summary="Fetches all blocks from the blockchain.",
    description="An API endpoint that specifically obtains all blocks from the blockchain.",  # TODO: Search for the cached output.
)
async def get_blocks(
    *,
    block_count: int
    | None = Query(
        ItemReturnCount.MIN,
        title="Number of Block Return",
        description="The value that signifies the number of blocks to return from the requestor.",
    ),
    page: int
    | None = Query(
        None,
        title=QUERY_CURRENT_INDEX_PAGE_NAME,
        description=QUERY_CURRENT_INDEX_NAME_DESCRIPTION,
    ),
) -> None:
    return


@explorer_router.get(
    "/block/{block_id}",
    tags=[
        ExplorerAPI.SPECIFIC_FETCH.value,
        ExplorerAPI.BLOCK_FETCH.value,
    ],
    response_model=Block,
    summary="Fetches a certain block from the blockchain.",
    description="An API endpoint that specifically obtains a certain block from the blockchain.",
)
async def get_certain_block(
    *,
    block_id: BlockID,
    tx_count: int
    | None = Query(
        ItemReturnCount.MID,
        title=QUERY_TRANSACTION_RETURN_NAME,
        description=QUERY_TRANSACTION_RETURN_DESCRIPTION,
    ),
    page: int
    | None = Query(
        None,
        title=QUERY_CURRENT_INDEX_PAGE_NAME,
        description="The page you are currently sitting, defaults to page 1. Other pages are available if the tx_count is higher than the number of total transactions from that block.",
    ),
) -> None:
    return


@explorer_router.get(
    "/transactions",
    tags=[
        ExplorerAPI.LIST_FETCH.value,
        ExplorerAPI.TRANSACTION_FETCH.value,
    ],
    response_model=list[Transaction],
    summary="Fetch all transactions for all blocks.",
    description="An API endpoint that returns all transactions that recently entered in the blockchain.",
)
async def get_transactions(
    *,
    tx_count: int
    | None = Query(
        ItemReturnCount.MIN,
        title=QUERY_TRANSACTION_RETURN_NAME,
        description=QUERY_TRANSACTION_RETURN_DESCRIPTION,
    ),
    page: int
    | None = Query(
        None,
        title=QUERY_CURRENT_INDEX_PAGE_NAME,
        description=QUERY_CURRENT_INDEX_NAME_DESCRIPTION,
    ),
) -> None:
    return


@explorer_router.get(
    "/transaction/{tx_id}",
    tags=[
        ExplorerAPI.SPECIFIC_FETCH.value,
        ExplorerAPI.TRANSACTION_FETCH.value,
    ],
    response_model=Transaction,
    summary="Fetches a specific transaction.",
    description="An API endpoint that returns a specific transaction that matches for all block inserted in the blockchain.",
)
async def get_particular_transaction(*, tx_id: TxID) -> None:
    return


@explorer_router.get(
    "/addresses",
    tags=[
        ExplorerAPI.LIST_FETCH.value,
        ExplorerAPI.ADDRESS_FETCH.value,
    ],
    # response_model=Addresses,
    summary="Fetch all addresses that has been recorded in blockchain.",
    description="An API endpoint that returns all addresses that is recorded in blockchain.",
)
async def get_addresses(
    *,
    addr_count: int
    | None = Query(
        ItemReturnCount.MIN,
        title="Number of Address Return",
        description="The number of addresses to return.",
    ),
    page: int
    | None = Query(
        None,
        title=QUERY_CURRENT_INDEX_PAGE_NAME,
        description=QUERY_CURRENT_INDEX_NAME_DESCRIPTION,
    ),
) -> None:
    return


@explorer_router.get(
    "/address/{address_uuid}",
    tags=[
        ExplorerAPI.SPECIFIC_FETCH.value,
        ExplorerAPI.ADDRESS_FETCH.value,
    ],
    # response_model=Address,
    summary="Fetch a specific address recorded in blockchain.",
    description="An API endpoint that obtains an address and display its transactions associated in the blockchain.",
)
async def get_particular_addresses(
    *,
    address_uuid: AddressUUID,
    tx_count: int
    | None = Query(
        ItemReturnCount.MIN,
        title=QUERY_TRANSACTION_RETURN_NAME,
        description=QUERY_TRANSACTION_RETURN_DESCRIPTION,
    ),
    page: int
    | None = Query(
        None,
        title=QUERY_CURRENT_INDEX_PAGE_NAME,
        description=QUERY_CURRENT_INDEX_NAME_DESCRIPTION,
    ),
) -> None:
    return


@explorer_router.get(
    "/search",
    tags=[ExplorerAPI.GENERAL_FETCH.value],
    # response_model=SearchContext,
    summary="Search an entity (block, transaction, address) on the blockchain.",
    description="An API endpoint that attempts to search for an entity provided by input. This endpoint enforce length restrictions, as well as returns a singleton data as a redirection link.",
)
async def search_in_explorer(
    *,
    context: str = Query(
        ...,
        title="The context to search in the blockchain.",
        min_length=3,
        max_length=32,
    ),
) -> None:
    return
