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
from typing import Mapping

from blueprint.models import consensus_negotiation, tx_content_mappings, users
from blueprint.schemas import (
    Block,
    Blockchain,
    BlockOverview,
    TransactionDetail,
    TransactionOverview,
)
from core.blockchain import BlockchainMechanism, get_blockchain_instance
from core.constants import AddressUUID, BaseAPI, ExplorerAPI, HashUUID
from databases import Database
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from sqlalchemy import Column, Table, func, select
from sqlalchemy.sql.expression import Select

from blueprint.schemas import EntityAddress
from core.dependencies import get_database_instance
from core.constants import UserEntity
from sqlalchemy.orm import Query as SQLQuery

from node.blueprint.schemas import EntityAddressDetail

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
    "/block/{id}",
    tags=[
        ExplorerAPI.SPECIFIC_FETCH.value,
        ExplorerAPI.BLOCK_FETCH.value,
    ],
    response_model=Block,
    summary="Fetches a certain block from the blockchain.",
    description="An API endpoint that specifically obtains a certain block from the blockchain.",
)
async def get_block(
    id: int = Path(
        ...,
        title="Block ID",
        description="The block of the ID to fetch from the chain.",
    ),
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance),
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
    response_model=list[TransactionOverview],
    summary="Fetch all transactions for all blocks.",
    description="An API endpoint that returns all transactions that recently entered in the blockchain.",
)
async def get_transactions(
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance),
) -> list[TransactionOverview]:
    if not isinstance(blockchain_instance, BlockchainMechanism):
        raise HTTPException(
            detail="Failed to fetch transactions, please try again later.",
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        )

    return await blockchain_instance.fetch_transactions()


@explorer_router.get(
    "/transaction/{tx_hash}",
    tags=[
        ExplorerAPI.SPECIFIC_FETCH.value,
        ExplorerAPI.TRANSACTION_FETCH.value,
    ],
    response_model=TransactionDetail,
    summary="Fetches a specific transaction.",
    description="An API endpoint that returns a specific transaction that matches for all block inserted in the blockchain.",
)
async def get_particular_transaction(
    tx_hash: HashUUID = Query(
        ...,
        title="Transaction Hash (TX)",
        description="The hash of the transaction to fetch from the chain.",
    ),
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance),
) -> TransactionDetail:

    if not isinstance(blockchain_instance, BlockchainMechanism):
        raise HTTPException(
            detail="Failed to fetch a transaction, please try again later.",
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        )

    transaction: TransactionDetail | None = await blockchain_instance.fetch_transaction(
        tx_hash=tx_hash
    )

    if isinstance(transaction, TransactionDetail):
        return transaction

    raise HTTPException(
        detail="Transaction not found.", status_code=HTTPStatus.NOT_FOUND
    )


@explorer_router.get(
    "/addresses",
    tags=[
        ExplorerAPI.LIST_FETCH.value,
        ExplorerAPI.ADDRESS_FETCH.value,
    ],
    response_model=list[EntityAddress],
    summary="Fetch all addresses that has been recorded in blockchain.",
    description="An API endpoint that returns all addresses that is recorded in blockchain.",
)
async def get_addresses(
    database_instance: Database = Depends(get_database_instance),
) -> list[EntityAddress]:
    entity_addresses: list[EntityAddress] = []

    fetch_entity: Select = select(
        [users.c.unique_address, users.c.association, users.c.type]
        # ).where(users.c.type != UserEntity.MASTER_NODE_USER)
    ).select_from(users)

    fetched_entities: list[Mapping[Table, Column]] = await database_instance.fetch_all(
        fetch_entity
    )

    for entity in fetched_entities:
        tx_bindings_count: int = 0
        node_negotiations_count: int = 0

        # - Fill other fields based on their role.
        if entity.type is UserEntity.ARCHIVAL_MINER_NODE_USER:
            fetch_negotiation_count_query: Select = select([func.count()]).where(
                consensus_negotiation.c.peer_address == entity.unique_address
            )

            node_negotiations_count = await database_instance.fetch_val(
                fetch_negotiation_count_query
            )
        else:
            fetch_tx_bindings_query: Select = select([func.count()]).where(
                tx_content_mappings.c.address_ref == entity.unique_address
            )

            tx_bindings_count = await database_instance.fetch_val(
                fetch_tx_bindings_query
            )

        entity_addresses.append(
            EntityAddress(
                uuid=entity.unique_address,
                association_uuid=entity.association,
                entity_type=entity.type,
                negotiations_count=node_negotiations_count,
                tx_bindings_count=tx_bindings_count,
            )
        )

    return entity_addresses


@explorer_router.get(
    "/address/{uuid}",
    tags=[
        ExplorerAPI.SPECIFIC_FETCH.value,
        ExplorerAPI.ADDRESS_FETCH.value,
    ],
    response_model=EntityAddressDetail,
    summary="Fetch a specific address recorded in blockchain.",
    description="An API endpoint that obtains an address and display its transactions associated in the blockchain.",
)
async def get_particular_addresses(uuid: AddressUUID) -> EntityAddressDetail:
    return


@explorer_router.get(
    "/search",
    tags=[ExplorerAPI.GENERAL_FETCH.value],
    summary="Search an entity (block, transaction, address) on the blockchain.",
    description="An API endpoint that attempts to search for an entity provided by input. This endpoint enforce length restrictions, as well as returns a singleton data as a redirection link.",
)
async def search_in_explorer(parameter: str) -> Response:
    # - Remember about the one that requires classifying the parameter if it was a block, transaction or an address.
    return Response(status_code=HTTPStatus.ACCEPTED)
