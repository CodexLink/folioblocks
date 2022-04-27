"""
Node Component, Explorer API

It contains the necessary API endpoints for the nodes who will participate in the blockchain. Note that some of these endpoints will be exclusive under 'master' node role. Also, note that most of these endpoints require JWT token to access.
It contains API endpoints that can be accessed by the Explorer Frontend UI (combined with the Dashboard UI @ 'web/' directory). Note that the base endpoint will not be the same from Frontend API endpoints.That is intended so that there will be no confusion, upon selection of the endpoint to use.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""
from http import HTTPStatus
from http.client import SERVICE_UNAVAILABLE

from blueprint.schemas import (
    Block,
    Blockchain,
    BlockOverview,
    NodeMasterInformation,
    Transaction,
)
from core.blockchain import BlockchainMechanism, get_blockchain_instance
from core.constants import (
    BaseAPI,
    ExplorerAPI,
)
from fastapi import APIRouter, Depends, HTTPException, Path

from core.constants import AddressUUID

explorer_router = APIRouter(
    prefix="/explorer",
    tags=[BaseAPI.EXPLORER.value],
)


@explorer_router.get(
    "/chain",
    tags=[
        ExplorerAPI.GENERAL_FETCH.value,
        ExplorerAPI.LIST_FETCH.value,
    ],
    response_model=Blockchain,
    summary="Fetch the context of the blockchain, formatted for displaying in the web.",
    description="An API endpoint that parses the current state of the blockchain under JSON-format for data display in the web. Note that this returns a fixed amount of data.",
)
async def get_node_info() -> Blockchain:
    blockchain_instance: BlockchainMechanism | None = get_blockchain_instance()

    if isinstance(blockchain_instance, BlockchainMechanism):

        return Blockchain(
            block=await blockchain_instance.fetch_blocks(limit_to=5),
            transactions=await blockchain_instance.fetch_transactions(limit_to=5),
            node_info=await blockchain_instance.get_blockchain_public_state(),
        )

    raise HTTPException(
        detail="Unable to fetch information of this node.",
        status_code=HTTPStatus.FORBIDDEN,
    )


@explorer_router.get(
    "/blocks",
    tags=[ExplorerAPI.LIST_FETCH.value, ExplorerAPI.BLOCK_FETCH.value],
    response_model=list[BlockOverview],
    summary="Fetches all blocks from the blockchain.",
    description="An API endpoint that specifically obtains all blocks from the blockchain.",
)
async def get_blocks(
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance),
) -> list[BlockOverview]:

    if isinstance(blockchain_instance, BlockchainMechanism):
        # - Instead of automatically deconstructing the model `Block`, use the already optimized model `BlockOverview`.
        # @o `BlockOverview` was added due to the endpoint `explorer/chain`.

        return await blockchain_instance.fetch_blocks()

    raise HTTPException(
        detail="Cannot fetch a set of blocks, please try again later.",
        status_code=HTTPStatus.SERVICE_UNAVAILABLE,
    )


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
async def get_block(
    *,
    block_id: int = Path(..., title="The ID of the block."),
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance)
) -> Block:

    if not isinstance(blockchain_instance, BlockchainMechanism):
        raise HTTPException(
            detail="Failed to fetch a block, please try again later.",
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        )

    block: Block | None = await blockchain_instance.fetch_block(id=block_id)

    if block is not None:
        return block

    raise HTTPException(detail="Block not found.", status_code=HTTPStatus.NOT_FOUND)


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
async def get_transactions(*, tx_count: int) -> None:
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
async def get_particular_transaction() -> None:
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
async def get_addresses(*, addr_count: int) -> None:
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
async def get_particular_addresses(*, address_uuid: AddressUUID) -> None:
    return


@explorer_router.get(
    "/search",
    tags=[ExplorerAPI.GENERAL_FETCH.value],
    # response_model=SearchContext,
    summary="Search an entity (block, transaction, address) on the blockchain.",
    description="An API endpoint that attempts to search for an entity provided by input. This endpoint enforce length restrictions, as well as returns a singleton data as a redirection link.",
)
async def search_in_explorer(
    # *,
    # context: str = Query()
    #     ...,
    #     title="The context to search in the blockchain.",
    #     min_length=3,
    #     max_length=32,
    # ),
) -> None:
    return
