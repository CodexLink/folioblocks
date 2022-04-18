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
from typing import Any, Mapping
from uuid import uuid4

import jwt
from blueprint.models import associated_nodes, auth_codes, tokens, users
from blueprint.schemas import (
    EntityLoginCredentials,
    EntityLoginResult,
    EntityRegisterCredentials,
    EntityRegisterResult,
    NodeRegisterTransaction,
    NodeTransaction,
)
from core.blockchain import BlockchainMechanism, get_blockchain_instance
from core.constants import (
    ADDRESS_UUID_KEY_PREFIX,
    ASYNC_TARGET_LOOP,
    JWT_ALGORITHM,
    JWT_DAY_EXPIRATION,
    MAX_JWT_HOLD_TOKEN,
    AddressUUID,
    AssociatedNodeStatus,
    BaseAPI,
    EntityAPI,
    HashedData,
    IdentityTokens,
    JWTToken,
    NodeTransactionInternalActions,
    NodeType,
    RawData,
    TokenStatus,
    TransactionActions,
    UserActivityState,
    UserEntity,
)
from core.dependencies import (
    get_args_values,
    get_database_instance,
    get_identity_tokens,
)
from core.email import get_email_instance
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import MetaData, false, select
from sqlalchemy.sql.expression import Insert, Select, Update
from utils.processors import hash_context, verify_hash_context

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

evaluated_role: NodeType = NodeType(get_args_values().node_role)

entity_router = APIRouter(
    prefix="/entity",
    tags=[BaseAPI.ENTITY.value],
)


@entity_router.post(
    "/register",
    tags=[EntityAPI.REGISTRATION_API.value],
    response_model=EntityRegisterResult,
    summary="Registers a node from the blockchain network.",
    description="An API endpoint that allows a node to be introduced to the blockchain network.",
)
async def register_entity(
    *,
    credentials: EntityRegisterCredentials,
    db: Any = Depends(get_database_instance),
) -> EntityRegisterResult:

    tokens: IdentityTokens | None = get_identity_tokens()

    # - Since we are going to record this in blockchain, which requires the `acceptor_address`, validate if it contains something.
    # * New instances doesn't have new credentials, check if there's an auth code for the NodeType.MASTER_NODE and it's not yet used.
    check_auth_from_new_master_query: Select = select([auth_codes.c.to_email]).where(
        (auth_codes.c.account_type == UserEntity.MASTER_NODE_USER)
        & (auth_codes.c.is_used == false())
    )

    check_auth_from_new_master_email = await db.fetch_one(
        check_auth_from_new_master_query
    )

    if tokens is None and check_auth_from_new_master_email is None:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Identity tokens seem to be missing. This should not be possible! Please report this to the developer!",
        )

    # TODO: Check for the association only when the entry has been labelled as non-node.
    # If there are no association then push that first.
    # db.execute(Association(name="Test"))

    unique_address_ref: AddressUUID = AddressUUID(
        f"{ADDRESS_UUID_KEY_PREFIX}:{uuid4().hex}"
    )
    dict_credentials: dict[str, Any] = credentials.dict()

    # - Our auth code should contain the information if that is applicable at certain role.
    # - Aside from the auth_code role assertion, fields-based on role checking is still asserted here.

    get_auth_token_query: Select = auth_codes.select().where(
        (auth_codes.c.code == credentials.auth_code)
        & (auth_codes.c.to_email == credentials.email)
        & (
            auth_codes.c.is_used == false()
        )  # ! Not sure why, but I have to arbitrary convert this bool to str, I guess there's no resolve.
        & (auth_codes.c.expiration >= datetime.now())
    )

    auth_token = await db.fetch_one(get_auth_token_query)

    if auth_token is not None:
        if not credentials.first_name or not credentials.last_name:
            # Asserted that this entity must be NODE_USER.
            del dict_credentials["first_name"], dict_credentials["last_name"]

        dict_credentials["type"] = (
            auth_token[
                3
            ]  # @o 3th index represents the account type from the `auth_token` metadata table.
            if auth_token.account_type in UserEntity
            else UserEntity.DASHBOARD_USER
        )  #  else SQLEntityUser.ADMIN_USER

        del (
            dict_credentials["password"],
            dict_credentials["auth_code"],
        )  # Remove other fields so that we can do the double starred expression for unpacking.

        data: Insert = users.insert().values(
            **dict_credentials,
            unique_address=unique_address_ref,
            password=hash_context(pwd=RawData(credentials.password))
            # association=, # I'm not sure on what to do with this one, as of now.
        )
        dispose_auth_code: Update = (
            auth_codes.update()
            .where(auth_codes.c.code == auth_token.code)
            .values(is_used=True)
        )

        try:
            await gather(db.execute(dispose_auth_code), db.execute(data))

            create_task(
                get_email_instance().send(  # TODO: Update of this content.
                    content="<html><body><h1>Hello from Folioblocks!</h1><p>Thank you for registering with us! Expect accessibility within a day or so.</p><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
                    subject="Welcome to Folioblocks!",
                    to=credentials.email,
                ),
                name=f"{get_email_instance.__name__}_send_register_welcome_notification",
            )

            blockchain_instance: BlockchainMechanism | None = get_blockchain_instance()

            # - After that, record this transaction from the blockchain.
            # @o This callback in particular is not part of the consolidated internal transactions declared from the `dependencies.py` under < class 'EnsureAuthorized'>
            # ! That is due to its several previous variables were used.
            if isinstance(blockchain_instance, BlockchainMechanism):
                if (
                    UserEntity(auth_token.account_type) is UserEntity.MASTER_NODE_USER
                    or UserEntity(auth_token.account_type)
                    is UserEntity.ARCHIVAL_MINER_NODE_USER
                    and blockchain_instance.node_role is NodeType.MASTER_NODE
                ):
                    await blockchain_instance._insert_internal_transaction(
                        action=TransactionActions.NODE_GENERAL_REGISTER_INIT,
                        data=NodeTransaction(
                            action=NodeTransactionInternalActions.INIT,
                            context=NodeRegisterTransaction(
                                acceptor_address=AddressUUID(
                                    tokens[1]
                                    if tokens is not None
                                    else check_auth_from_new_master_email
                                ),
                                new_address=AddressUUID(unique_address_ref),
                                role=auth_token.account_type,
                                timestamp=datetime.now(),
                            ),
                        ),
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
    *, credentials: EntityLoginCredentials, db: Any = Depends(get_database_instance)
) -> EntityLoginResult:  # * We didn't use aiohttp.BasicAuth because frontend has a form, and we don't need a prompt.

    credential_to_look: Select = users.select().where(
        users.c.username == credentials.username
    )
    fetched_credential_data = await db.fetch_one(credential_to_look)

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

        # @o Parse the datetime object to be string literal.
        payload["date_registered"] = payload["date_registered"].isoformat()

        if verify_hash_context(
            real_pwd=RawData(credentials.password),
            hashed_pwd=HashedData(fetched_credential_data.password),
        ):
            other_tokens_query: Select = tokens.select().where(
                (tokens.c.from_user == fetched_credential_data.unique_address)
                & (tokens.c.state == TokenStatus.CREATED_FOR_USE.name)
            )

            other_tokens: list[Mapping] = await db.fetch_all(other_tokens_query)

            # - Check if this user has more than MAX_JWT_HOLD_TOKEN active JWT tokens.
            if len(other_tokens) >= MAX_JWT_HOLD_TOKEN:
                raise HTTPException(
                    detail=f"This user `{fetched_credential_data.unique_address}` -> `{fetched_credential_data.username}` withold/s {len(other_tokens)} JWT tokens. The maximum value that the user can withold should be only {MAX_JWT_HOLD_TOKEN}.",
                    status_code=HTTPStatus.BAD_REQUEST,
                )

            # - If all other conditions are clear, then create the JWT token.
            jwt_expire_at: datetime | None = None
            if fetched_credential_data.type is UserEntity.DASHBOARD_USER:
                jwt_expire_at = datetime.now() + timedelta(days=JWT_DAY_EXPIRATION)

                payload[
                    "expire_at"
                ] = jwt_expire_at.isoformat()  # # Make it different per request.

            token = jwt.encode(payload, env.get("SECRET_KEY", JWT_ALGORITHM))

            # - Put a new token to the database then update the user as it receives the token.
            new_token: Insert = tokens.insert().values(
                from_user=fetched_credential_data.unique_address,
                token=token,
                expiration=jwt_expire_at,
            )
            logged_user_query: Update = (
                users.update()
                .where(users.c.unique_address == fetched_credential_data.unique_address)
                .values(activity=UserActivityState.ONLINE)
            )

            try:
                await gather(db.execute(logged_user_query), db.execute(new_token))

                # - Check if this node does have a association certificate token.

                if fetched_credential_data.type == UserEntity.ARCHIVAL_MINER_NODE_USER:
                    logger.info(
                        "Checking if this node has its own associate node certificate token."
                    )

                    logged_user_has_association_token_query: Select = (
                        associated_nodes.select().where(
                            associated_nodes.c.user_address
                            == fetched_credential_data.unique_address
                        )
                    )

                    associated_token_from_logged_user: Mapping | None = (
                        await db.fetch_one(logged_user_has_association_token_query)
                    )

                    print(
                        associated_token_from_logged_user,
                        type(associated_token_from_logged_user),
                        dir(associated_token_from_logged_user),
                    )

                    if associated_token_from_logged_user is not None:
                        update_associate_node_state_query: Update = (
                            associated_nodes.update()
                            .where(
                                associated_nodes.c.user_address
                                == fetched_credential_data.unique_address
                            )
                            .values(status=AssociatedNodeStatus.CURRENTLY_AVAILABLE)
                        )

                        await db.execute(update_associate_node_state_query)

                        logger.info(
                            f"Associate Reference ({fetched_credential_data.unique_address}) has been updated to {AssociatedNodeStatus.CURRENTLY_AVAILABLE.name}."
                        )

                    else:
                        logger.warning(
                            "This node user doesn't have a certificate token, assuming first instance."
                        )

                return EntityLoginResult(
                    user_address=fetched_credential_data.unique_address,
                    user_role=fetched_credential_data.type,
                    jwt_token=JWTToken(token),
                    expiration=jwt_expire_at,
                )

            except IntegrityError as e:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"For some reason, there's an existing data of a request for new token. This is an error, please report this to the developer as possible. | Additional Info: {e}",
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
async def logout_entity(
    *,
    x_token: JWTToken = Header(..., description="The acquired token to invalidate."),
    db: Any = Depends(get_database_instance),
) -> None:

    fetched_token_query: Select = tokens.select().where(
        (tokens.c.token == x_token) & (tokens.c.state != TokenStatus.EXPIRED)
    )

    fetched_token = await db.fetch_one(fetched_token_query)

    if fetched_token is not None:
        token_ref: Update = (
            tokens.update()
            .where(tokens.c.token == x_token)
            .values(state=TokenStatus.EXPIRED)
        )

        # - Fetch the user from this token for the extra step.
        user_ref_query: Select = users.select().where(
            users.c.unique_address == fetched_token.from_user
        )

        user_ref = await db.fetch_one(user_ref_query)

        if user_ref is not None:

            # - Check if this user is ARCHIVAL_MINER_NODE_USER, otherwise ignore this extra step.
            if user_ref.type == UserEntity.ARCHIVAL_MINER_NODE_USER:

                # - Fetch first before updating.
                associate_from_user_ref_query: Select = associated_nodes.select().where(
                    associated_nodes.c.user_address == user_ref.unique_address
                )

                associate_from_user_ref = await db.fetch_one(
                    associate_from_user_ref_query
                )

                if associate_from_user_ref is not None:
                    update_associate_state_from_user_query: Update = (
                        associated_nodes.update()
                        .where(
                            associated_nodes.c.user_address == user_ref.unique_address
                        )
                        .values(status=AssociatedNodeStatus.CURRENTLY_NOT_AVAILABLE)
                    )

                    await db.execute(update_associate_state_from_user_query)

                    logger.info(
                        f"An associate ({associate_from_user_ref.user_address}) reference status has been updated to {AssociatedNodeStatus.CURRENTLY_NOT_AVAILABLE.name}."
                    )

            else:
                logger.warning(
                    "Ignoring this extra step due to condition regarding user role."
                )

        await db.execute(token_ref)
        return

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="The inferred token does not exist or is already labeled as expired!",
    )
