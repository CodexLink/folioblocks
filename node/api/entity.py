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
    GroupTransaction,
    NodeRegisterTransaction,
    NodeTransaction,
    OrganizationUserTransaction,
)
from core.blockchain import BlockchainMechanism, get_blockchain_instance
from core.constants import (
    ASYNC_TARGET_LOOP,
    JWT_ALGORITHM,
    JWT_DAY_EXPIRATION,
    MAX_JWT_HOLD_TOKEN,
    AddressUUID,
    AssociatedNodeStatus,
    BaseAPI,
    EntityAPI,
    HashedData,
    JWTToken,
    NodeTransactionInternalActions,
    NodeType,
    OrganizationType,
    RawData,
    TokenStatus,
    TransactionActions,
    TransactionContextMappingType,
    UserActivityState,
    UserEntity,
)
from core.dependencies import generate_uuid_user, get_args_values, get_database_instance
from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import Table, false, func, select
from sqlalchemy.orm import Query
from sqlalchemy.sql.expression import Delete, Insert, Select, Update
from utils.processors import save_database_state_to_volume_storage
from utils.email import get_email_instance
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
    database_instance: Any = Depends(get_database_instance),
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance),
) -> EntityRegisterResult | JSONResponse | None:

    if not isinstance(blockchain_instance, BlockchainMechanism):
        # - Before concluding that its not yet, ready bypass this mechanism only when there's no `MASTER_NODE` in the node system.

        get_master_node_acc_query: Select = select([func.count()]).where(
            users.c.type == UserEntity.MASTER_NODE_USER
        )

        master_node_acc: Mapping[Query[Table], int] = await database_instance.fetch_val(
            get_master_node_acc_query
        )

        if (
            master_node_acc
        ):  # * When there's a count then we can prohibit others from registering unless the blockchain itself is ready.
            raise HTTPException(
                detail="Blockchain instance is not yet fully initialized. Please try again later.",
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            )

    # - Since we are going to record this in blockchain, which requires the `acceptor_address`, validate if it contains something.
    # * New instances doesn't have new credentials, check if there's an auth code for the NodeType.MASTER_NODE and it's not yet used.

    check_auth_from_new_master_query: Select = select(
        [auth_codes.c.account_type, auth_codes.c.code]
    ).where(
        (auth_codes.c.code == credentials.auth_code)
        & (auth_codes.c.is_used == false())
        & (auth_codes.c.to_email == credentials.email)
    )

    new_user_auth_register = await database_instance.fetch_one(
        check_auth_from_new_master_query
    )

    if new_user_auth_register is None:
        raise HTTPException(
            detail="Provided `auth_token` were not found.",
            status_code=HTTPStatus.NOT_FOUND,
        )
    if (
        new_user_auth_register.account_type is UserEntity.ORGANIZATION_DASHBOARD_USER
        and (
            isinstance(credentials.first_name, str)
            and isinstance(credentials.last_name, str)
        )
        and (
            (
                isinstance(credentials.association_name, str)
                and credentials.association_address is None
                and isinstance(credentials.association_type, OrganizationType)
                and isinstance(credentials.association_founded, datetime)
                and isinstance(credentials.association_description, str)
            )
            or (
                credentials.association_name is None
                and isinstance(credentials.association_address, str)
                and credentials.association_type is None
                and credentials.association_founded is None
                and credentials.association_description is None
            )
        )
    ):

        # - Ensure that this only runs when other nodes registered, this is not applied for `MASTER_NODE`.
        # @o When registering a user, there is a need of special handling, as things are recorded in the blockchain.
        if isinstance(blockchain_instance, BlockchainMechanism):
            new_user_insertion_response: HTTPException | None = (
                await blockchain_instance.insert_external_transaction(
                    action=TransactionActions.ORGANIZATION_USER_REGISTER,
                    from_address=blockchain_instance.node_identity[0],
                    to_address=None,
                    data=GroupTransaction(
                        content_type=TransactionContextMappingType.ORGANIZATION_BASE,
                        context=OrganizationUserTransaction(
                            association_address=credentials.association_address,
                            association_name=credentials.association_name,
                            association_group_type=credentials.association_type,
                            first_name=credentials.first_name,
                            last_name=credentials.last_name,
                            email=credentials.email,
                            username=credentials.username,
                            password=credentials.password,
                            org_type=credentials.association_type,
                            founded=credentials.association_founded,
                            description=credentials.association_description,
                            identity=None,
                            institution=credentials.association_address,
                        ),
                    ),
                )
            )

            if isinstance(new_user_insertion_response, HTTPException):
                raise new_user_insertion_response

        dispose_auth_code_for_org: Update = (
            auth_codes.update()
            .where(auth_codes.c.code == new_user_auth_register.code)
            .values(is_used=True)
        )

        await gather(
            database_instance.execute(dispose_auth_code_for_org),
            save_database_state_to_volume_storage(),
        )

        return JSONResponse(
            content={
                "detail": f"Registration process as a {new_user_auth_register.account_type} has been processed successfully! Please check your email for more information."
            },
            status_code=HTTPStatus.ACCEPTED,
        )

    elif new_user_auth_register.account_type is UserEntity.STUDENT_DASHBOARD_USER:
        raise HTTPException(
            detail="You are registering as an student, which is not allowed by external. Please go to any organization to have your account setup and verified.",
            status_code=HTTPStatus.FORBIDDEN,
        )
    elif (
        new_user_auth_register.account_type is UserEntity.ARCHIVAL_MINER_NODE_USER
        or new_user_auth_register.account_type is UserEntity.MASTER_NODE_USER
    ):

        if (
            credentials.association_name is not None
            or credentials.association_address is not None
            or credentials.association_type is not None
            or credentials.association_founded is not None
            or credentials.association_description is not None
            or credentials.first_name is not None
            or credentials.last_name is not None
        ):
            raise HTTPException(
                detail=f"Fields for the organization registration were detected. Are you trying to register as a {UserEntity.ARCHIVAL_MINER_NODE_USER.name} or {UserEntity.MASTER_NODE_USER.name}? Please use the `folioblocks-node-cli`.",
                status_code=HTTPStatus.FORBIDDEN,
            )

        dict_credentials: dict[str, Any] = credentials.dict()

        # - Our auth code should contain the information if that is applicable at certain role.
        # - Aside from the auth_code role assertion, fields-based on role checking is still asserted here.

        if not credentials.first_name or not credentials.last_name:
            # Asserted that this entity must be NODE_USER.
            del dict_credentials["first_name"], dict_credentials["last_name"]

        dict_credentials["type"] = new_user_auth_register.account_type

        del (
            dict_credentials["password"],
            dict_credentials["auth_code"],
            dict_credentials["association_address"],
            dict_credentials["association_type"],
            dict_credentials["association_name"],
            dict_credentials["association_founded"],
            dict_credentials["association_description"],
        )  # Remove other fields so that we can do the double starred expression for unpacking.

        data: Insert = users.insert().values(
            **dict_credentials,
            unique_address=generate_uuid_user(),
            password=hash_context(pwd=RawData(credentials.password)),
            date_registered=datetime.now(),
        )
        dispose_auth_code: Update = (
            auth_codes.update()
            .where(auth_codes.c.code == new_user_auth_register.code)
            .values(is_used=True)
        )

        user_new_uuid: AddressUUID = AddressUUID(generate_uuid_user())

        try:
            await gather(
                database_instance.execute(data),
                database_instance.execute(dispose_auth_code),
                save_database_state_to_volume_storage(),
            )

            create_task(
                get_email_instance().send(
                    content=f"<html><body><h1>Hello from Folioblocks::Node Users!</h1><p>Thank you for registering as a <b><i>`{new_user_auth_register.account_type.value}`</b></i>! Remember, please be responsible of your assigned role. Any suspicious actions will be sanctioned. Please talk to any administrators to guide you on how to use our system. Once again, thank you!</p><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
                    subject="Hello from Folioblocks::Node Users!",
                    to=credentials.email,
                ),
                name=f"{get_email_instance.__name__}_send_register_welcome_node",
            )

            # - After that, record this transaction from the blockchain.
            # @o This callback in particular is not part of the consolidated internal transactions declared from the `dependencies.py` under < class 'EnsureAuthorized'>
            # ! That is due to its several previous variables were used.
            if isinstance(blockchain_instance, BlockchainMechanism):
                if (
                    new_user_auth_register.account_type is UserEntity.MASTER_NODE_USER
                    or new_user_auth_register.account_type
                    is UserEntity.ARCHIVAL_MINER_NODE_USER
                    and blockchain_instance.node_role is NodeType.MASTER_NODE
                ):
                    await blockchain_instance.insert_internal_transaction(
                        action=TransactionActions.NODE_GENERAL_REGISTER_INIT,
                        data=NodeTransaction(
                            action=NodeTransactionInternalActions.INIT,
                            context=NodeRegisterTransaction(
                                acceptor_address=AddressUUID(
                                    blockchain_instance.node_identity[0]
                                ),
                                new_address=AddressUUID(user_new_uuid),
                                role=new_user_auth_register.account_type,
                                timestamp=datetime.now(),
                            ),
                        ),
                    )

                    return EntityRegisterResult(
                        user_address=user_new_uuid,
                        username=credentials.username,
                        date_registered=datetime.now(),
                        role=dict_credentials["type"],
                    )

        except IntegrityError as e:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Your credential already exists. Please request to replace your password if you already have an account. | Info: {e}",
            )
    else:
        raise HTTPException(
            detail=f"Cannot proceed when field and the given role conditions (received {new_user_auth_register.account_type.name}) were unmet. Please remove other fields with respect to your given role by your representative/s.",
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        )


@entity_router.post(
    "/login",
    tags=[EntityAPI.LOGIN_API.value],
    response_model=EntityLoginResult,
    summary="Logs an entity from the blockchain network.",
    description="An API endpoint that logs an entity to the blockchain network.",
)
async def login_entity(
    *,
    credentials: EntityLoginCredentials,
    database_instance: Any = Depends(get_database_instance),
) -> EntityLoginResult:  # * We didn't use aiohttp.BasicAuth because frontend has a form, and we don't need a prompt.

    credential_to_look: Select = users.select().where(
        users.c.username == credentials.username
    )
    fetched_credential_data = await database_instance.fetch_one(credential_to_look)

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

            other_tokens: list[Mapping] = await database_instance.fetch_all(
                other_tokens_query
            )

            # - Exception, specially for our scenario. We delete other tokens upon logging in, which should only renew our token instead.
            if (
                fetched_credential_data.type is UserEntity.MASTER_NODE_USER
                or fetched_credential_data.type is UserEntity.ARCHIVAL_MINER_NODE_USER
            ):
                # ! Note that we should only maintain one node per account, other organization who hosts the nodes should have seperate accounts for those.
                update_existing_alive_tokens_query: Update = (
                    tokens.update()
                    .where(
                        (tokens.c.from_user == fetched_credential_data.unique_address)
                        & (tokens.c.state == TokenStatus.CREATED_FOR_USE)
                    )
                    .values(state=TokenStatus.LOGGED_OUT)
                )

                await gather(
                    database_instance.execute(update_existing_alive_tokens_query),
                    save_database_state_to_volume_storage(),
                )

            else:
                # - Check if this user has more than MAX_JWT_HOLD_TOKEN active JWT tokens.
                if len(other_tokens) >= MAX_JWT_HOLD_TOKEN:
                    raise HTTPException(
                        detail=f"This user withold/s a maximum of {len(other_tokens)} JWT tokens. Please logout other tokens or wait for them to expire.",
                        status_code=HTTPStatus.FORBIDDEN,
                    )

            # - If all other conditions are clear, then create the JWT token.
            jwt_expire_at: datetime | None = None
            if fetched_credential_data.type in [
                UserEntity.STUDENT_DASHBOARD_USER,
                UserEntity.ORGANIZATION_DASHBOARD_USER,
            ]:
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
                await gather(
                    database_instance.execute(logged_user_query),
                    database_instance.execute(new_token),
                    save_database_state_to_volume_storage(),
                )
                # - Check if this node does have a association certificate token.

                if fetched_credential_data.type is UserEntity.ARCHIVAL_MINER_NODE_USER:
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
                        await database_instance.fetch_one(
                            logged_user_has_association_token_query
                        )
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

                        await gather(
                            database_instance.execute(
                                update_associate_node_state_query
                            ),
                            save_database_state_to_volume_storage(),
                        )

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
                    detail=f"There's was an existing request for the new token. | Additional Info: {e}",
                    status_code=HTTPStatus.BAD_REQUEST,
                )

        raise HTTPException(
            detail="Your credentials are incorrect.",
            status_code=HTTPStatus.UNAUTHORIZED,
        )

    raise HTTPException(
        detail="User not found. Please check your credentials and try again.",
        status_code=HTTPStatus.NOT_FOUND,
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
    database_instance: Any = Depends(get_database_instance),
) -> None:

    fetched_token_query: Select = tokens.select().where(
        (tokens.c.token == x_token) & (tokens.c.state != TokenStatus.EXPIRED)
    )

    fetched_token = await database_instance.fetch_one(fetched_token_query)

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

        user_ref = await database_instance.fetch_one(user_ref_query)

        if user_ref is not None:

            # - Check if this user is ARCHIVAL_MINER_NODE_USER, otherwise ignore this extra step.
            if user_ref.type == UserEntity.ARCHIVAL_MINER_NODE_USER:

                # - Fetch first before updating.
                associate_from_user_ref_query: Select = associated_nodes.select().where(
                    associated_nodes.c.user_address == user_ref.unique_address
                )

                associate_from_user_ref = await database_instance.fetch_one(
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

                    await database_instance.execute(
                        update_associate_state_from_user_query
                    )

                    logger.info(
                        f"An associate ({associate_from_user_ref.user_address}) reference status has been updated to {AssociatedNodeStatus.CURRENTLY_NOT_AVAILABLE.name}."
                    )

            else:
                logger.warning(
                    "Ignoring this extra step due to condition regarding user role."
                )

        await gather(
            database_instance.execute(token_ref),
            save_database_state_to_volume_storage(),
        )
        return

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="The inferred token does not exist or is already labelled as expired!",
    )
