"""
API — Explorer and Node API for the Master Node.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""


from typing import Any

from blueprint.schemas import NodeInformation
from core.blockchain import get_blockchain_instance
from core.constants import AddressUUID, BaseAPI, NodeAPI, UserEntity
from core.dependencies import (
    EnsureAuthorized,
    ensure_past_negotiations,
    get_identity_tokens,
)
from fastapi import APIRouter, Depends

node_router = APIRouter(
    prefix="/node",
    tags=[BaseAPI.NODE.value],
)


@node_router.get(
    "/info",
    tags=[
        NodeAPI.GENERAL_NODE_API.value,
        NodeAPI.NODE_TO_NODE_API.value,
        NodeAPI.MASTER_NODE_API.value,
    ],
    response_model=NodeInformation,
    summary="Fetch information from the master node.",
    description="An API endpoint that returns information based on the authority of the client's requests. This requires special headers.",
)
async def get_node_info(
    *,
    auth: Any = Depends(
        EnsureAuthorized(_as=[UserEntity.NODE_USER, UserEntity.DASHBOARD_USER])
    ),
) -> NodeInformation:
    blockchain_state = get_blockchain_instance().get_blockchain_state

    return NodeInformation(
        owner=AddressUUID(
            get_identity_tokens()[0] if get_identity_tokens is not None else "0"
        ),
        is_sleeping=blockchain_state["sleeping"],
        is_mining=blockchain_state["mining"],
        consensus_timer=blockchain_state["consensus_timer"],
        last_mined_block=blockchain_state["last_mined_block"],
    )


@node_router.post(
    "/negotiate/{phase_state}",
    tags=[
        NodeAPI.NODE_TO_NODE_API.value,
    ],
    # response_model=NodeNegotiation,
    summary="Initiates and finishes negotiation from mafster node to side node and vice versa.",
    description="An API endpoint that handles the negotiations from node-to-node.",  # TODO: Add some test cases. This was intended to ensure that we really know wtf are we doing.
)
async def pre_post_negotiate(
    *,
    phase_state: str | None = None,
    role: Any = Depends(
        EnsureAuthorized(_as=UserEntity.NODE_USER)
    ),  # TODO: # ! No TYPE!
) -> None:  # TODO: Actions should be, receive_block, (During this, one of the assert processes will be executed.)
    return


@node_router.put(
    "/negotiate/{negotiation_id}",  # Aside from client identification, we should have an identifier.
    tags=[NodeAPI.NODE_TO_NODE_API.value],
    # response_model=NodeNegotiationProcess,
    summary="Execute and acknowledge payloads given from this endpoint.",
    description="An exclusive-situational API endpoint that allows nodes to communicate during process stage of the negotiation.",
)
async def process_negotiate(
    *,
    deps: Any = Depends(ensure_past_negotiations),
) -> None:  # Actions should be updating data for the master node to communicate.
    return
