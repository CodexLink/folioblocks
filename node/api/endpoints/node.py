"""
API — Explorer and Node API for the Master Node.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

# Libraries
from fastapi import APIRouter
from api.core.models import (
    NodeInfoContext,
    NodeLoginContext,
    NodeLoginCredentials,
    NodeNegotiation,
    NodeNegotiationProcess,
    NodeRegisterCredentials,
)
from utils.constants import NodeAPI

# from secrets import token_hex

node_router = APIRouter(
    prefix="/node",
    tags=["Node API"],
    responses={404: {"description": "Not Found."}},  # TODO: Handle more than Not Found.
)


@node_router.post(
    "/register",
    tags=[NodeAPI.GENERAL_NODE_API.value],
    response_model=NodeRegisterCredentials,
    summary="Registers a node from the blockchain network.",
    description="An API endpoint that allows a node to be introduced to the blockchain network.",
)
async def register_node():
    pass


@node_router.get(
    "/login",
    tags=[NodeAPI.GENERAL_NODE_API.value],
    response_model=NodeLoginContext,
    summary="Logs a node from the blockchain network.",
    description="An API endpoint that logs the node to the blockchain network.",
)
async def login_node(credentials: NodeLoginCredentials):
    pass


@node_router.get(
    "/info",
    tags=[
        NodeAPI.GENERAL_NODE_API.value,
        NodeAPI.NODE_TO_NODE_API.value,
        NodeAPI.MASTER_NODE_API.value,
    ],
    response_model=NodeInfoContext,
    summary="Fetch information from the master node.",
    description="An API endpoint that returns information based on the authority of the client's requests. This requires special headers.",  # TODO
)
async def get_chain_info():  # Includes, time_estimates, mining_status, consensus, config. # TODO, accept multiple contents.
    pass


@node_router.post(
    "/negotiate/{phase_state}",
    tags=[
        NodeAPI.NODE_TO_NODE_API.value,
    ],
    response_model=NodeNegotiation,
    summary="Initiates and finishes negotiation from master node to side node and vice versa.",
    description="An API endpoint that handles the negotiations from node-to-node.",  # TODO: Add some test cases. This was intended to ensure that we really know wtf are we doing.
)
async def pre_post_negotiate(
    phase_state: str | None = None,
):  # Argument is TODO. Actions should be, receive_block, send_hash_block (During this, one of the assert processes will be executed.)
    pass


@node_router.put(
    "/negotiate/{negotiation_id}",  # Aside from client identification, we should have an identifier.
    tags=[NodeAPI.NODE_TO_NODE_API.value],
    response_model=NodeNegotiationProcess,
    summary="Execute and acknowledge payloads given from this endpoint.",
    description="An exclusive-situational API endpoint that allows nodes to communicate during process stage of the negotiation.",
)
async def process_negotiate():  # Actions should be updating data for the master node to communicate.
    pass


# TODO: Add a consensus endpoint or a functionality from the negotiation!!!
