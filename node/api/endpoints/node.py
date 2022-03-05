"""
API — Explorer and Node API for the Master Node.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from datetime import datetime, timedelta
from enum import EnumMeta
from os import environ as env

# Libraries
from typing import Any
from uuid import uuid4

import jwt
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
from fastapi import APIRouter, Depends, HTTPException

# from database.models import Association
from utils.constants import (
    JWT_ALGORITHM,
    JWT_DAY_EXPIRATION,
    AddressUUID,
    BaseAPI,
    HashedData,
    NodeAPI,
    RawData,
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
        UserEntity.NODE_USER if is_node else UserEntity.DASHBOARD_USER
    )  #  else SQLEntityUser.ADMIN_USER

    del (
        dict_credentials["password"],
        dict_credentials["auth_code"],
    )  # Remove other fields so that we can do the double starred expression for unpacking.

    data = users.insert().values(
        **dict_credentials,
        uaddr=uaddr_ref,
        password=hash_user_password(RawData(credentials.password))
        # association=, # I'm not sure on what to do with this one, as of now.
    )

    await db.execute(data)

    data = NodeRegisterResult(
        user_address=uaddr_ref,
        username=credentials.username,
        date_registered=datetime.now(),
        role=dict_credentials["user_type"],
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
) -> NodeLoginContext:

    # Query the user first.
    credential_to_look = users.select().where(users.c.uaddr == credentials.user_address)

    fetched_data = await db.fetch_one(credential_to_look)

    # TODO: This is implementable when we have the capability to lock out users due to suspicious activities.
    # * Check if they are unlocked or not. THIS REQUIRES ANOTHER CHECK TO ANOTHER DATABASE. SUCH AS THE BLACKLISTED.
    if fetched_data is not None:
        payload: dict[str, Any] = dict(zip(fetched_data._fields, fetched_data))

        # Adjust the payload to be compatible with JWT encoding.

        # Since there are several enum.Enum, we need to convert them to literal values for the JWT to encode it. Objects are not possible to encode.
        for each_item in payload:
            if isinstance(type(payload[each_item]), EnumMeta):
                payload[each_item] = payload["user_activity"].name

        payload["date_registered"] = payload["date_registered"].isoformat()

        if verify_user_hash(
            RawData(credentials.password), HashedData(fetched_data["password"])
        ):

            # Create the JWT token.
            token = jwt.encode(payload, env.get("SECRET_KEY", JWT_ALGORITHM))

            return NodeLoginContext(
                username=fetched_data.username,
                user_address=fetched_data.uaddr,
                jwt_token=token,
                expiration=datetime.now() + timedelta(days=JWT_DAY_EXPIRATION),
            )

    raise HTTPException(
        status_code=404,
        detail="User is not found. Please check your credentials and try again.",
    )


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
    auth: Any = Depends(ensure_authorized(UserEntity.NODE_USER)),
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
    role: Any = Depends(ensure_authorized(UserEntity.NODE_USER)),  # TODO: # ! No TYPE!
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
