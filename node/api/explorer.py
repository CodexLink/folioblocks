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
from typing import Any, Generic, Literal, Mapping, TypeVar

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
from sqlalchemy import Column, MetaData, Table, func, select
from sqlalchemy.sql.expression import Select

from blueprint.schemas import EntityAddress
from core.dependencies import get_database_instance
from core.constants import UserEntity
from sqlalchemy.orm import Query as SQLQuery
from sqlalchemy.engine.row import Row
from blueprint.schemas import EntityAddressDetail

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
            block=await blockchain_instance.get_blocks(limit_to=5),
            transactions=await blockchain_instance.get_transactions(limit_to=5),
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

        return await blockchain_instance.get_blocks()

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

    block: Block | None = await blockchain_instance.get_block(id=block_id)

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

    return await blockchain_instance.get_transactions()


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
async def get_transaction(
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

    transaction: TransactionDetail | None = await blockchain_instance.get_transaction(
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

    get_entity: Select = select(
        [users.c.unique_address, users.c.association, users.c.type]
    ).where(users.c.type != UserEntity.MASTER_NODE_USER)

    fetched_entities: list[Mapping[Any, Any]] = await database_instance.fetch_all(
        get_entity
    )

    for entity in fetched_entities:
        tx_bindings_count: int = 0
        node_negotiations_count: int = 0

        # - Fill other fields based on their role.
        if entity.type is UserEntity.ARCHIVAL_MINER_NODE_USER:
            get_negotiation_count_query: Select = select([func.count()]).where(
                consensus_negotiation.c.peer_address == entity.unique_address
            )

            node_negotiations_count: int = await database_instance.fetch_val(
                get_negotiation_count_query
            )
        else:
            get_tx_bindings_query: Select = select([func.count()]).where(
                tx_content_mappings.c.address_ref == entity.unique_address
            )

            tx_bindings_count: int = await database_instance.fetch_val(
                get_tx_bindings_query
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
async def get_address(
    uuid: AddressUUID,
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance),
    database_instance: Database = Depends(get_database_instance),
) -> EntityAddressDetail:

    if not isinstance(blockchain_instance, BlockchainMechanism):
        raise HTTPException(
            detail="Failed to fetch address information due to service disruption, please try again later.",
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        )

    # - Fill Variables.
    user_description: str | None = None
    tx_count: int = 0
    negotiation_count: int = 0

    # - Get the address of the user.
    get_user_via_address_query: Select = select(
        [users.c.association, users.c.description, users.c.type]
    ).where(users.c.unique_address == uuid)

    user_props: Mapping | None = await database_instance.fetch_one(
        get_user_via_address_query
    )

    if user_props is None:
        raise HTTPException(
            detail="Address not found.", status_code=HTTPStatus.NOT_FOUND
        )
    else:

        # - Fill the information of the field `description` if this user was a type `UserEntity.ORGANIZATION_DASHBOARD_USER`.
        if user_props.type is UserEntity.ORGANIZATION_DASHBOARD_USER:
            user_description = user_props.description

        # - Fill the information of the field `tx_bindings_count` if this user was a type `UserEntity.APPLICANT_DASHBOARD_USER`.
        elif user_props.type is UserEntity.APPLICANT_DASHBOARD_USER:
            user_tx_count_query: Select = select([func.count()]).where(
                tx_content_mappings.c.address_ref == uuid
            )

            tx_count = await database_instance.fetch_val(user_tx_count_query)

        # - FIll the information of the field `negotiations_count` if this user was a type `UserEntity.ARCHIVAL_MINER_NODE_USER`.
        elif user_props.type is UserEntity.ARCHIVAL_MINER_NODE_USER:
            user_negotiation_count_query: Select = select(func.count()).where(
                consensus_negotiation.c.peer_address == uuid
            )

            negotiation_count = await database_instance.fetch_val(
                user_negotiation_count_query
            )

        else:
            raise HTTPException(
                detail="Failed to parse user due to out of scope type.",
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        return EntityAddressDetail(
            uuid=uuid,
            association_uuid=user_props.association,
            description=user_description,
            entity_type=user_props.type,
            tx_bindings_count=tx_count,
            negotiations_count=negotiation_count,
            # - Get the transaction associated from this user.
            related_txs=await blockchain_instance.get_transactions(address=uuid),
        )
