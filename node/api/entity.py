"""
API — Entity API | API for accessibility for services in the network.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""
from datetime import datetime, timedelta
from enum import EnumMeta
from http import HTTPStatus
from os import environ as env
from sqlite3 import IntegrityError
from typing import Any
from uuid import uuid4

import jwt
from blueprint.models import tokens, users
from blueprint.schemas import (
    EntityLoginCredentials,
    EntityLoginResult,
    EntityRegisterCredentials,
    EntityRegisterResult,
)
from core.constants import (
    JWT_ALGORITHM,
    JWT_DAY_EXPIRATION,
    UUID_KEY_PREFIX,
    AddressUUID,
    BaseAPI,
    EntityAPI,
    HashedData,
    JWTToken,
    RawData,
    UserEntity,
)
from core.dependencies import get_db_instance
from fastapi import APIRouter, Depends, HTTPException
from utils.processors import hash_user_password, verify_user_hash

entity_router = APIRouter(
    prefix="/entity",
    tags=[BaseAPI.ENTITY.value],
    responses={
        404: {"description": "Not Found."}
    },  # TODO: Handle more than Not Found. ADD METADATA here or something.
)

# # WARNING: When this was SIDE mode, use endpoints instead of using it's own SQL database.


@entity_router.post(
    "/register",
    tags=[EntityAPI.REGISTRATION_API.value],
    response_model=EntityRegisterResult,
    summary="Registers a node from the blockchain network.",
    description="An API endpoint that allows a node to be introduced to the blockchain network.",
)

# TODO: Add the auth_code generation when endpoint is done.
async def register_entity(
    credentials: EntityRegisterCredentials,
    db: Any = Depends(
        get_db_instance
    ),  # Soon??? on this context? existing_auth: Any = Depends(validate_auth_code)
) -> EntityRegisterResult:

    # If there are no association then push that first.
    # db.execute(Association(name="Test"))

    unique_address_ref: AddressUUID = AddressUUID(f"{UUID_KEY_PREFIX}:{uuid4().hex}")
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
        unique_address=unique_address_ref,
        password=hash_user_password(RawData(credentials.password))
        # association=, # I'm not sure on what to do with this one, as of now.
    )

    try:
        await db.execute(data)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Your credential input already exists. Please request to replace your password if you think you already have an account.",
        )

    data = EntityRegisterResult(
        user_address=unique_address_ref,
        username=credentials.username,
        date_registered=datetime.now(),
        role=dict_credentials["user_type"],
    )

    return data


@entity_router.post(
    "/login",
    tags=[EntityAPI.LOGIN_API.value],
    response_model=EntityLoginResult,
    summary="Logs an entity from the blockchain network.",
    description="An API endpoint that logs an entity to the blockchain network.",
)
async def login_entity(
    credentials: EntityLoginCredentials, db: Any = Depends(get_db_instance)
) -> EntityLoginResult:

    # Query the user first.
    credential_to_look = users.select().where(users.c.username == credentials.username)

    fetched_data = await db.fetch_one(credential_to_look)

    # TODO: This is implementable when we have the capability to lock out users due to suspicious activities.
    # * Check if they are unlocked or not. THIS REQUIRES ANOTHER CHECK TO ANOTHER DATABASE. SUCH AS THE BLACKLISTED.

    print(dir(fetched_data), fetched_data)

    if fetched_data is not None:
        # payload = Users
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
            jwt_expire_at = datetime.now() + timedelta(days=JWT_DAY_EXPIRATION)

            payload[
                "expire_at"
            ] = jwt_expire_at.isoformat()  # Make it different per request.

            token = jwt.encode(payload, env.get("SECRET_KEY", JWT_ALGORITHM))

            # Put a new token to the database.
            new_token = tokens.insert().values(
                from_user=fetched_data.unique_address,
                token=token,
                expiration=jwt_expire_at,
            )

            try:
                await db.execute(new_token)

                return EntityLoginResult(
                    user_address=fetched_data.unique_address,
                    jwt_token=JWTToken(token),
                    expiration=jwt_expire_at,
                )
            except IntegrityError:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="For some reason, there's an existing data of a request for new token. This is an error, please report this to the developer as possible.",
                )

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="User is not found. Please check your credentials and try again.",
    )


@entity_router.post(
    "/logout",
    tags=[EntityAPI.ENTITY_GENERAL_API.value],
    summary="Logs out the entity from the blockchain network.",
    description="An API endpoint that logs out any entity to the blockchain network.",
)

# TODO: Implement logout then we go implement the info for the header testing and then we go to the blockchain.
async def logout_entity(
    key: Any = Depends(),  # make ensure authorized compatible for with-return and non-return context.
    db: Any = Depends(get_db_instance),  # Probably another dependency injection.
) -> EntityLoginResult:
    return EntityLoginResult()


# TODO: USER INFORMATION ENDPOINT
@entity_router.get(
    "/info",
    summary="Obtains the information of the entity.",
    description="An API endpoint that obtains information of the user. This is useful when browsed in the website.",
)
async def get_entity():  # * This requires custom pydantic model.
    raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not yet implemented.")
