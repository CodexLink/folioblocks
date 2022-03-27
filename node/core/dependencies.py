"""
Dependencies (dependencies.py) | Contains a set of functions and attributes that is classified to run under FastAPI.Depends and a sub-dependencies of `depends`. Some attributes are required for the sake of authenticating the client for operation.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from argparse import Namespace
from asyncio import sleep
from datetime import datetime, timedelta
from http import HTTPStatus
from logging import Logger, getLogger
from os import environ as env
from random import randint
from secrets import token_hex
from sqlite3 import IntegrityError
from typing import Any

from aioconsole import ainput
from aiohttp import (
    BasicAuth,
    ClientConnectionError,
    ClientConnectorCertificateError,
    ClientConnectorError,
    ClientConnectorSSLError,
    ClientError,
    ClientSession,
)
from blueprint.models import auth_codes, tokens, users
from blueprint.schemas import EntityLoginResult, Tokens
from databases import Database
from fastapi import Depends, Header, HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from utils.http import get_http_client_instance

from core.constants import (
    ASYNC_TARGET_LOOP,
    AUTH_CODE_MAX_CONTEXT,
    AUTH_CODE_MIN_CONTEXT,
    AUTH_ENV_FILE_NAME,
    MASTER_NODE_IP_PORT,
    AddressUUID,
    CredentialContext,
    HTTPQueueMethods,
    JWTToken,
    NodeType,
    TokenStatus,
    URLAddress,
    UserEntity,
)
from core.email import get_email_instance

args_value: Namespace
identity_tokens: tuple[AddressUUID, JWTToken]
db_instance: Database
logger: Logger = getLogger(ASYNC_TARGET_LOOP)


def store_args_value(args: Namespace) -> None:
    logger.debug(f"Argument values from `Argparse` has been stored. | Context: {args}")
    global args_value
    args_value = args


def get_args_value() -> Namespace:
    global args_value
    return args_value


def store_db_instance(instance: Database) -> None:
    logger.debug(f"Database instance has been stored. | Context: {instance}")
    global db_instance
    db_instance = instance


def get_db_instance() -> Database:
    global db_instance
    return db_instance


def store_identity_tokens(_tokens: tuple[AddressUUID, JWTToken]) -> None:
    logger.debug(
        f"Identity tokens were stored. | Context: (Address: {_tokens[0]}, JWT Token:{_tokens[1]})"
    )
    global identity_tokens
    identity_tokens = _tokens


def get_identity_tokens() -> tuple[AddressUUID, JWTToken]:
    try:
        global identity_tokens
        return identity_tokens
    except NameError:
        pass


# TODO: Not sure why we have this function signature.
# def generate_auth_token(to: EmailStr, type: UserEntity, expires: timedelta) -> None:
def generate_auth_token() -> str:
    generated: str = token_hex(randint(AUTH_CODE_MIN_CONTEXT, AUTH_CODE_MAX_CONTEXT))
    logger.debug(
        f"Auth token generated with the following constraints: Min Length is {AUTH_CODE_MIN_CONTEXT}, Max Length is {AUTH_CODE_MAX_CONTEXT}. | Context: {generated}"
    )
    return generated


# TODO Implement blacklisted users!
async def authenticate_node_client(
    *,
    role: NodeType,
    instances: tuple[Namespace, Database],
) -> None:

    from utils.processors import (
        ensure_input_prompt,
    )  # ! Imported on function due to circular dependency.

    user_credentials: tuple[CredentialContext, CredentialContext] | None = None

    logger.debug("Attempting to authenticate ...")

    if env.get("NODE_USERNAME", None) is None and env.get("NODE_PWD", None) is None:
        logger.warning(
            "Environment file doesn't contain the values for `NODE_USERNAME` and/or `NODE_PWD` or is entirely missing. Assuming first-time instance."
        )

        while True:
            try:
                logger.info(
                    f"{f'To start, the system will create an `auth_token` for you to register yourself.' if role == NodeType.MASTER_NODE else f'Since this a new instance, you need credentials for you to enter in blockchain.'} | Please enter your email address."
                )

                if role == NodeType.MASTER_NODE:
                    email_address: EmailStr = await ensure_input_prompt(
                        input_context="Email Address",
                        hide_fields=False,
                        generalized_context="email address",
                        additional_context="You will have to restart the instance if you confirmed it late that it was a mistake!",
                    )

                    # * This functionality is only available on `MASTER` in local / self instance.
                    generated_token: str = generate_auth_token()
                    insert_generated_token_stmt = auth_codes.insert().values(
                        code=generated_token,
                        account_type=UserEntity.MASTER_NODE_USER,
                        to_email=email_address,
                        expiration=datetime.now() + timedelta(days=2),
                    )

                    await instances[1].execute(insert_generated_token_stmt)

                    await get_email_instance().send(
                        content=f"<html><body><h1>Register Auth Code from Folioblocks!</h1><p>Thank you for taking interest! To continue, please enter the authentication code for the registration. <b>DO NOT SHARE THIS TO ANYONE.</b></p><br><br><h4>Auth Code: {generated_token}<b></b></h4><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
                        subject="Register Auth Code for Registration @ Folioblocks",
                        to=email_address,
                    )
                else:  # @o Resolves to NodeType.ARCHIVAL_MINER_NODE.
                    inputted_credentials: list[Any] = await ensure_input_prompt(
                        input_context=[
                            "Personal e-mail representing this node",
                            "Node username",
                            "Node password",  # * I cannot implement password-checking because I have no time to do it.
                        ],
                        hide_fields=[False, False, True],
                        generalized_context="credentials",
                        additional_context="You will have to ensure it this time to avoid potential conflicts from the startup!",
                        enable_async=True,
                    )

                    register_node: Any = await get_http_client_instance().enqueue_request(
                        url=URLAddress(
                            f"http://{instances[0].host}:{instances[0].port}/entity/register"
                        ),
                        method=HTTPQueueMethods.POST,
                        data={
                            "email": inputted_credentials[0],
                            "username": inputted_credentials[1],
                            "password": inputted_credentials[2],
                        },
                    )

                    if not register_node.ok:
                        logger.error(
                            f"There seems to be an error during request. Please try again | Info: {register_node.json()}"
                        )
                        continue

                    logger.info(
                        "Registration seems to be successful! Please re-enter your username and password to continue."
                    )

            # ! Assumeing that the email service is running, I have to step away from this since complexity rises if I continue on improving it.
            except IntegrityError as e:
                from utils.processors import unconventional_terminate

                unconventional_terminate(
                    message=f"Your input matches one of the records for `{NodeType.MASTER_NODE.name} registration.` Are you attempting to restart instance? Please delete the generated files and try again.",
                )

            logger.info(
                f"A generated code has been sent. Please register from the '{instances[0].host}:{instances[0].port}/entity/register' endpoint and login with your credentials on the next prompt."
            )
            break

    while True:
        if env.get("NODE_USERNAME", None) is None and env.get("NODE_PWD", None) is None:
            user_credentials = await ensure_input_prompt(
                input_context=["Node Username", "Node Password"],
                hide_fields=[False, True],
                generalized_context="username and password",
                additional_context="You will have to ensure it this time to avoid potential conflicts!",
                enable_async=True,
            )

        # Ensure that ENV will be covered here.
        try:
            login_req: Any = await get_http_client_instance().enqueue_request(
                url=URLAddress(
                    f"http://{instances[0].host}:{get_args_value().port}/entity/login"
                ),
                method=HTTPQueueMethods.POST,
                data={
                    "username": env.get("NODE_USERNAME", None)
                    if user_credentials is None
                    else user_credentials[0],
                    "password": env.get("NODE_PWD", None)
                    if user_credentials is None
                    else user_credentials[1],
                },
            )

            if login_req.ok:
                # Resolve via pydantic.
                resolved_model = EntityLoginResult.parse_obj(await login_req.json())

                resolve_entity_to_role = (
                    NodeType.MASTER_NODE
                    if resolved_model.user_role == UserEntity.MASTER_NODE_USER
                    else NodeType.ARCHIVAL_MINER_NODE
                )

                # TODO: Please test this one.
                if resolve_entity_to_role.value != get_args_value().prefer_role:
                    unconventional_terminate(
                        message=f"Node was able to login successfully but the acccount type is not suitable for instance type. Account has a type suitable `for {resolve_entity_to_role}`, got {get_args_value().prefer_role} instead.",
                        early=True,
                    )

                # With this, we should also save the context by using store_auth_token().
                store_identity_tokens(
                    (
                        AddressUUID(resolved_model.user_address),
                        JWTToken(resolved_model.jwt_token),
                    )
                )

                if (  # Ensure fields are None from the environment file and process the credentials.
                    env.get("NODE_USERNAME", None) is None
                    and env.get("NODE_PWD", None) is None
                    and user_credentials
                ):
                    with open(AUTH_ENV_FILE_NAME, "a") as env_writer:
                        env_writer.write(
                            f"NODE_USERNAME={user_credentials[0]}\nNODE_PWD={user_credentials[1]}"
                        )

                    logger.info(f"Authenticated as {resolved_model.user_address}.")
                break

            else:
                logger.error(
                    f"Credentials are incorrect! Please try again. | Object: {login_req} | Info: {await login_req.json()}"
                )
                await sleep(1.5)
                continue

        # * Should cover the following exceptions: (ClientConnectorError, ClientConnectorSSLError, ClientConnectorCertificateError, and ClientConnectionError)
        except ClientError as e:
            logger.critical(
                f"There was an error during request. Please try again. | Context: {e}"
            )
            await sleep(1.5)
            continue


class EnsureAuthorized:
    def __init__(self, _as: UserEntity | list[UserEntity]) -> None:
        self._as: UserEntity | list[UserEntity] = _as

    async def __call__(
        self,
        x_token: JWTToken = Header(
            ..., description="The token that is inferred for validation."
        ),
        db: Database = Depends(get_db_instance),
    ) -> None:  # TODO.

        if x_token:
            req_ref_token = tokens.select().where(
                (tokens.c.token == x_token) & (tokens.c.state != TokenStatus.EXPIRED)
            )

            req_token = await db.fetch_one(req_ref_token)

            if req_token:
                ref_token = Tokens.parse_obj(req_token)

                # ! I didn't use the Metadata().select() because its parameter whereclause blocks selective column to return.
                # * Therefore use the general purpose sqlalchemy.select instead.
                user_role_ref = select([users.c.type]).where(
                    users.c.unique_address == ref_token.from_user
                )

                user_role = await db.fetch_val(user_role_ref)

                if isinstance(self._as, list):
                    for each_role in self._as:
                        if user_role is each_role:
                            return
                else:
                    if user_role is self._as:
                        return

        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="You are unauthorized to access this endpoint. Please login first.",
        )


def ensure_past_negotiations(
    *,
    identity: tuple[AddressUUID, JWTToken] = Depends(get_identity_tokens),
    db: Database = Depends(get_db_instance),
) -> bool:
    # Maybe query or use the current session or the Node ID.
    # We need to contact the other part to ensure that there is negotiations.
    return False
