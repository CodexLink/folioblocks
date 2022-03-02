"""
API — Explorer and Node API for the Master Node.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from datetime import datetime

# Libraries
from typing import Any
from uuid import uuid4

from api.core.schemas import (
    NodeInfoContext,
    NodeLoginContext,
    NodeLoginCredentials,
    NodeNegotiation,
    NodeNegotiationProcess,
    NodeRegisterCredentials,
    NodeRegisterResult,
)
from database.models import users
from fastapi import APIRouter, Depends

# from database.models import Association
from utils.constants import (
    AddressUUID,
    BaseAPI,
    NodeAPI,
    RawData,
    SQLUserEntity,
    UserEntity,
)
from utils.database import (
    ensure_authorized,
    ensure_past_negotiations,
    get_db_instance,
    hash_user_password,
    verify_user_hash,
)

node_router = APIRouter(
    prefix="/node",
    tags=[BaseAPI.NODE.value],
    responses={
        404: {"description": "Not Found."}
    },  # TODO: Handle more than Not Found. ADD METADATA here or something.
)


@node_router.post(
    "/register",
    tags=[NodeAPI.GENERAL_NODE_API.value],
    response_model=NodeRegisterResult,
    summary="Registers a node from the blockchain network.",
    description="An API endpoint that allows a node to be introduced to the blockchain network.",
)

# TODO: Add the auth_code generation when endpoint is done.
async def register_entity(
    credentials: NodeRegisterCredentials,
    db: Any = Depends(
        get_db_instance
    ),  # Soon??? on this context? existing_auth: Any = Depends(validate_auth_code)
) -> NodeRegisterResult:

    # If there are no association then push that first.
    # db.execute(Association(name="Test"))

    uaddr_ref: AddressUUID = AddressUUID("fl:" + uuid4().hex)
    dict_credentials: dict[str, Any] = credentials.dict()
    is_node: bool = False
    # Save something from the database here.

    # TODO
    # Our auth code should contain the information if that is applicable at certain role.
    # Aside from the auth_code role assertion, fields-based on role checking is still asserted here.

    if not credentials.first_name or not credentials.last_name:
        # Asserted that this entity must be NODE_USER.
        del dict_credentials["first_name"], dict_credentials["last_name"]
        is_node = True  # This is just a temporary.

    dict_credentials["user_type"] = (
        SQLUserEntity.NODE if is_node else SQLUserEntity.DASHBOARD
    )  #  else SQLEntityUser.ADMIN_USER

    del (
        dict_credentials["password"],
        dict_credentials["auth_code"],
    )  # Remove other fields so that we can do the double starred expression for unpacking.

    data = users.insert().values(
        **dict_credentials,
        uaddr=uaddr_ref,
        password=hash_user_password(RawData(credentials.password))
        # association=,
    )

    await db.execute(data)

    data = NodeRegisterResult(
        user_address=uaddr_ref,
        date_registered=datetime.now(),
        role=UserEntity.NODE if is_node else UserEntity.DASHBOARD,
    )

    return data


@node_router.post(
    "/login",
    tags=[NodeAPI.GENERAL_NODE_API.value],
    response_model=NodeLoginContext,
    summary="Logs a node from the blockchain network.",
    description="An API endpoint that logs the node to the blockchain network.",
)
async def login_node(
    credentials: NodeLoginCredentials, db: Any = Depends(get_db_instance)
) -> dict[str, Any]:  # TODO

    # Validate the user first.
    # Check if they are unlocked or not.
    # Check if their password matches from the hashed password.

    if verify_user_hash():
        return


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
async def get_chain_info(
    auth: Any = Depends(ensure_authorized(UserEntity.NODE)),
) -> None:  # Includes, time_estimates, mining_status, consensus, config. # TODO, accept multiple contents.
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
    role: Any = Depends(ensure_authorized(UserEntity.NODE)),  # TODO: # ! No TYPE!
):  # Argument is TODO. Actions should be, receive_block, (During this, one of the assert processes will be executed.)
    pass


@node_router.put(
    "/negotiate/{negotiation_id}",  # Aside from client identification, we should have an identifier.
    tags=[NodeAPI.NODE_TO_NODE_API.value],
    response_model=NodeNegotiationProcess,
    summary="Execute and acknowledge payloads given from this endpoint.",
    description="An exclusive-situational API endpoint that allows nodes to communicate during process stage of the negotiation.",
)
async def process_negotiate(
    deps: Any = Depends(ensure_past_negotiations),
):  # Actions should be updating data for the master node to communicate.
    pass


# TODO: Add a consensus endpoint or a functionality from the negotiation!!!
