"""
API — Entity API | API for accessibility for services in the network.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""
from asyncio import create_task, gather
from datetime import datetime, timedelta
from enum import EnumMeta
from http import HTTPStatus
from logging import Logger, getLogger
from os import environ as env
from sqlite3 import IntegrityError
from typing import Any
from uuid import uuid4

import jwt
from blueprint.models import auth_codes, tokens, users
from blueprint.schemas import (
    EntityLoginCredentials,
    EntityLoginResult,
    EntityRegisterCredentials,
    EntityRegisterResult,
)
from core.constants import (
    ASYNC_TARGET_LOOP,
    JWT_ALGORITHM,
    JWT_DAY_EXPIRATION,
    MAX_JWT_HOLD_TOKEN,
    UUID_KEY_PREFIX,
    AddressUUID,
    BaseAPI,
    CredentialContext,
    EntityAPI,
    HashedData,
    JWTToken,
    NodeType,
    RawData,
    TokenStatus,
    UserActivityState,
    UserEntity,
)
from core.dependencies import get_db_instance
from core.email import get_email_instance
from fastapi import APIRouter, Depends, Header, HTTPException
from utils.exceptions import MaxJWTOnHold
from utils.processors import hash_context, verify_hash_context

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

entity_router = APIRouter(
    prefix="/entity",
    tags=[BaseAPI.ENTITY.value],
)

# # WARNING: When this was ARCHIVAL_MINER_NODE mode, use endpoints instead of using it's own SQL database.
@entity_router.post(
    "/register",
    tags=[EntityAPI.REGISTRATION_API.value],
    response_model=EntityRegisterResult,
    summary="Registers a node from the blockchain network.",
    description="An API endpoint that allows a node to be introduced to the blockchain network.",
)
async def register_entity(
    *, credentials: EntityRegisterCredentials, db: Any = Depends(get_db_instance)
) -> EntityRegisterResult:

    # TODO: Check for the association only when the entry has been labelled as non-node.
    # If there are no association then push that first.
    # db.execute(Association(name="Test"))

    unique_address_ref: AddressUUID = AddressUUID(f"{UUID_KEY_PREFIX}:{uuid4().hex}")
    dict_credentials: dict[str, Any] = credentials.dict()

    # - Our auth code should contain the information if that is applicable at certain role.
    # - Aside from the auth_code role assertion, fields-based on role checking is still asserted here.

    get_auth_token_stmt = auth_codes.select().where(
        (auth_codes.c.code == credentials.auth_code)
        & (auth_codes.c.to_email == credentials.email)
        & (
            auth_codes.c.is_used == "False"
        )  # ! Not sure why, but I have to arbitrary convert this bool to str, I guess there's no resolve.
        & (auth_codes.c.expiration >= datetime.now())
    )

    auth_token = await db.fetch_one(get_auth_token_stmt)

    if auth_token:
        if not credentials.first_name or not credentials.last_name:
            # Asserted that this entity must be NODE_USER.
            del dict_credentials["first_name"], dict_credentials["last_name"]

        dict_credentials["type"] = (
            UserEntity.NODE_USER
            if auth_token.account_type == UserEntity.NODE_USER.name
            else UserEntity.DASHBOARD_USER
        )  #  else SQLEntityUser.ADMIN_USER

        del (
            dict_credentials["password"],
            dict_credentials["auth_code"],
        )  # Remove other fields so that we can do the double starred expression for unpacking.

        data = users.insert().values(
            **dict_credentials,
            unique_address=unique_address_ref,
            password=hash_context(pwd=RawData(credentials.password))
            # association=, # I'm not sure on what to do with this one, as of now.
        )
        dispose_auth_code = (
            auth_codes.update()
            .where(auth_codes.c.code == auth_token.code)
            .values(is_used=True)
        )

        try:
            await gather(db.execute(dispose_auth_code), db.execute(data))
            create_task(
                get_email_instance().send(
                    content="<html><body><h1>Hello from Folioblocks!</h1><p>Thank you for registering with us! Expect accessibility within a day or so.</p><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
                    subject="Welcome to Folioblocks!",
                    to=credentials.email,
                )
            )

        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Your credential input already exists. Please request to replace your password if you think you already have an account.",
            )

        return EntityRegisterResult(
            user_address=unique_address_ref,
            username=credentials.username,
            date_registered=datetime.now(),
            role=dict_credentials["type"],
        )

    raise HTTPException(
        status_code=HTTPStatus.NOT_ACCEPTABLE,
        detail="The `auth code` you entered is not valid! Please check your input and try again. If persists, you may not be using the email that the code was sent on, or the code has expired.",
    )


@entity_router.post(
    "/login",
    tags=[EntityAPI.LOGIN_API.value],
    response_model=EntityLoginResult,
    summary="Logs an entity from the blockchain network.",
    description="An API endpoint that logs an entity to the blockchain network.",
)
async def login_entity(
    *, credentials: EntityLoginCredentials, db: Any = Depends(get_db_instance)
) -> EntityLoginResult:  # * We didn't use aiohttp.BasicAuth because frontend has a form, and we don't need a prompt.

    credential_to_look = users.select().where(users.c.username == credentials.username)
    fetched_credential_data = await db.fetch_one(credential_to_look)

    # TODO: Check if they are unlocked or not. THIS REQUIRES ANOTHER CHECK TO ANOTHER DATABASE. SUCH AS THE BLACKLISTED.
    # - This is implementable when we have the capability to lock out users due to suspicious activities.

    if fetched_credential_data is not None:

        # We cannot use pydantic model because we need to do some modification that violates use-case of pydantic.
        payload: dict[str, Any] = dict(
            zip(fetched_credential_data._fields, fetched_credential_data)
        )

        # Adjust the payload to be compatible with JWT encoding.
        # Since there are several enum.Enum, we need to convert them to literal values for the JWT to encode it.

        for each_item in payload:
            if isinstance(type(payload[each_item]), EnumMeta):
                payload[each_item] = payload["activity"].name

        payload["date_registered"] = payload["date_registered"].isoformat()

        if verify_hash_context(
            real_pwd=RawData(credentials.password),
            hashed_pwd=HashedData(fetched_credential_data.password),
        ):
            other_tokens_stmt = tokens.select().where(
                (tokens.c.from_user == fetched_credential_data.unique_address)
                & (tokens.c.state == TokenStatus.CREATED_FOR_USE.name)
            )

            other_tokens = await db.fetch_all(other_tokens_stmt)

            # Check if this user has more than MAX_JWT_HOLD_TOKEN active JWT tokens.
            if len(other_tokens) >= MAX_JWT_HOLD_TOKEN:
                raise MaxJWTOnHold(
                    (
                        fetched_credential_data.unique_address,
                        CredentialContext(fetched_credential_data.username),
                    ),
                    len(other_tokens),
                )

            # If all other conditions are clear, then create the JWT token.
            jwt_expire_at: datetime | None = None
            if fetched_credential_data.type == NodeType.ARCHIVAL_MINER_NODE:
                jwt_expire_at = datetime.now() + timedelta(days=JWT_DAY_EXPIRATION)

                payload[
                    "expire_at"
                ] = jwt_expire_at.isoformat()  # Make it different per request.

            token = jwt.encode(payload, env.get("SECRET_KEY", JWT_ALGORITHM))

            # Put a new token to the database then update the user as it receives the token.
            new_token = tokens.insert().values(
                from_user=fetched_credential_data.unique_address,
                token=token,
                expiration=jwt_expire_at,
            )
            logged_user = (
                users.update()
                .where(users.c.unique_address == fetched_credential_data.unique_address)
                .values(activity=UserActivityState.ONLINE)
            )

            try:
                await gather(db.execute(logged_user), db.execute(new_token))

                return EntityLoginResult(
                    user_address=fetched_credential_data.unique_address,
                    jwt_token=JWTToken(token),
                    expiration=jwt_expire_at,
                )

            except IntegrityError as e:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"For some reason, there's an existing data of a request for new token. This is an error, please report this to the developer as possible. | Info: {e}",
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
    status_code=HTTPStatus.ACCEPTED,
)

# TODO: Implement logout then we go implement the info for the header testing and then we go to the blockchain.
async def logout_entity(
    *,
    x_token: JWTToken = Header(..., description="The acquired token to invalidate."),
    db: Any = Depends(get_db_instance),
) -> None:

    fetched_token = tokens.select().where(
        (tokens.c.token == x_token) & (tokens.c.state != TokenStatus.EXPIRED)
    )

    if await db.fetch_one(fetched_token):
        token_ref = (
            tokens.update()
            .where(tokens.c.token == x_token)
            .values(state=TokenStatus.EXPIRED)
        )

        if await db.execute(token_ref):
            return

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="The inferred token does not exist or is already labeled as expired!",
    )


@entity_router.get(
    "/info",
    summary="Obtains the information of the entity.",
    description="An API endpoint that obtains information of the user. This is useful when browsed in the website.",
)
async def get_entity() -> None:  # * This requires custom pydantic model.
    raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not yet implemented.")
