"""
Node Component, Explorer API

It contains the necessary API endpoints for the nodes who will participate in the blockchain. Note that some of these endpoints will be exclusive under 'master' node role. Also, note that most of these endpoints require JWT token to access.

It contains API endpoints that can be accessed by the Explorer Frontend UI (combined with the Dashboard UI @ 'web/' directory). Note that the base endpoint will not be the same from Frontend API endpoints.That is intended so that there will be no confusion, upon selection of the endpoint to use.

======================================================

This file is part of Folioblocks.

Folioblocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Folioblocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Folioblocks. If not, see <https://www.gnu.org/licenses/>.
"""

# TODO: Finish config, and then design schema for both the blockchain and the config and test it later on.

if __name__ == "__main__":
    raise SystemExit("This {__file__} (module) should not be executed as an entrypoint code! This module contains API endpoints for the Node API, which is an extension of this Explorer API.")

from typing import Final
from fastapi import APIRouter, Depends, Query
from utils.constants import BlockID, ExplorerAPITags, ItemReturnCount
# from core.models import Blockchain

explorer_router = APIRouter(
    prefix="/explorer",
    tags=["Explorer API"],
    responses= {404: {"description": "Not Found."}} # TODO: Handle more than Not Found.
)

# ! Note: Most of these operations require the need of the original JSON of the master node. From there, we may be able to cache the output.

@explorer_router.get(
    "/",
    tags=[
        ExplorerAPITags.GENERAL_FETCH.name,
        ExplorerAPITags.LIST_FETCH.name
    ],
    # response_model=Blockchain,
    summary="Fetch the context of the blockchain, formatted for displaying in the web.",
    description="An API endpoint that parses the current state of the blockchain under JSON-format for data display in the web. Note that this returns a fixed amount of data." (# TODO)
)
async def get_blockchain():
    pass

@explorer_router.get(
    "/blocks",
    tags=[
        ExplorerAPITags.LIST_FETCH.name,
        ExplorerAPITags.BLOCK_FETCH.name
    ],
    # response_model=Blocks,
    summary="Fetches all blocks from the blockchain.",
    description="An API endpoint that specifically fetches all blocks from the blockchain." # TODO: Search for the cached output.
)
async def get_blocks(
    block_count: int | None = Query(
        ItemReturnCount.MIN,
        title="Number of Block Return",
        description="The value that signifies the number of blocks to return from the requestor."
    ),
    page: int | None = Query(
        None,
        title="Current Index Page",
        description="The page you are currently sitting, defaults to page 1. Other pages are available if the block_count is higher than the number of returned blocks."
    )
):
    pass

@explorer_router.get(
    "/block/{block_id}",
    tags=[
        ExplorerAPITags.SPECIFIC_FETCH.name,
        ExplorerAPITags.BLOCK_FETCH.name
    ],
    # response_model=Block,
    summary="Fetches a certain block from the blockchain.",
    description="An API endpoint that specifically fetches a certain block from the blockchain." # TODO: Search for the cached output.
)
async def get_certain_block(
    block_id: BlockID,
    tx_count: int | None: Query(
        ItemReturnCount.MID,
        title="Number of Transaction Return"
        description="The number of transactions to return on that block."
    ),
    page: int | None = Query(
        None,
        title="Current Index Page"
        description="The page you are currently sitting, defaults to page 1. Other pages are available if the tx_count is higher than the number of total transactions from that block."
    )
):
    pass

@explorer_router.get(
    "/transactions",
    tags=[
        ExplorerAPITags.LIST_FETCH.name,
        ExplorerAPITags.TRANSACTION_FETCH.name
    ]
    # response_model=TXs,
    summary="Fetch all transactions for all blocks.",
    description="An API endpoint that returns all transactions that recently entered in the blockchain."
)
async def get_transactions(
    tx_count: int | None = Query(
        ItemReturnCount.MIN,
        title="Number of Transaction Return",
        description="The number of transactions to return."
    ),
    page: int | None = Query(
        None,
        title="Current Index Page",
        description="The page you are currently sitting, defaults to page 1. Other pages are available if the block_count is higher than the number of returned blocks."
):
    pass

@explorer_router.get(
    "/transaction/{tx_id}",
    tags=[
        ExplorerAPITags.SPECIFIC_FETCH.name,
        ExplorerAPITags.TRANSACTION_FETCH.name
    ],
    # response_model=TX,
    summary="Fetches a specific transaction.",
    description="An API endpoint that returns a specific transaction that matches for all block inserted in the blockchain."
)
async def get_particular_transaction(tx_id: TxID):
    pass

@explorer_router.get(
    "/addresses",
    tags=[
        ExplorerAPITags.LIST_FETCH.name,
        ExplorerAPITags.ADDRESS_FETCH.name
    ],
    # response_model=Addresses,
    summary="Fetch all addresses that has been recorded in blockchain.",
    description="An API endpoint that returns all addresses that is recorded in blockchain."
)
async def get_addresses(
    addr_count: int | None = Query(
        ItemReturnCount.MIN,
        title="Number of Address Return",
        description="The number of addresses to return."
    ),
    page: int | None = Query(
        None,
        title="Current Index Page",
        description="The page you are currently sitting, defaults to page 1. Other pages are available if the block_count is higher than the number of returned blocks."
):
    pass

@explorer_router.get(
    "/address/{address_uuid}",
    tags=[
        ExplorerAPITags.SPECIFIC_FETCH.name,
        ExplorerAPITags.ADDRESS_FETCH.name
    ],
    # response_model=Address,
    summary="Fetch a specific address recorded in blockchain.",
    description="An API endpoint that fetches an address and display its transactions associated in the blockchain."
)
async def get_particular_addresses(
    address_uuid: AddressUUID,
    tx_count: int | None = Query(
        ItemReturnCount.MIN,
        title="Number of Transaction Return",
        description="The number of transactions to return."
    ),
    page: int | None = Query(
        None,
        title="Current Index Page",
        description="The page you are currently sitting, defaults to page 1. Other pages are available if the block_count is higher than the number of returned blocks."
):
    pass

@explorer_router.get(
    "/search",
    tags=[ExplorerAPITags.GENERAL_FETCH.name],
    # response_model=Search,
    summary="Search an entity (block, transaction, address) on the blockchain.",
    description="An API endpoint that attempts to search for an entity provided by input. This endpoint enforce length restrictions, as well as returns a singleton data as a redirection link."
)
async def search_in_explorer(context: Query(..., min_length=3, max_length=32):
    pass

