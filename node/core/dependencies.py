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
    AddressUUID,
    CredentialContext,
    HTTPQueueMethods,
    JWTToken,
    NodeRoles,
    TokenStatus,
    URLAddress,
    UserEntity,
)
from core.email import get_email_instance

identity_tokens: tuple[AddressUUID, JWTToken]
db_instance: Database
logger: Logger = getLogger(ASYNC_TARGET_LOOP)


def store_db_instance(instance: Database) -> None:
    logger.debug(f"Database instance has been stored. | Context: {instance}")
    global db_instance
    db_instance = instance


def get_db_instance() -> Database:
    logger.debug(f"Database instance has been fetched.")
    global db_instance
    return db_instance


def store_identity_tokens(_tokens: tuple[AddressUUID, JWTToken]) -> None:
    logger.debug(
        f"Identity tokens were stored. | Context: (Address: {_tokens[0]}, JWT Token:{_tokens[1]})"
    )
    global identity_tokens
    identity_tokens = _tokens


def get_identity_tokens() -> tuple[AddressUUID, JWTToken]:
    logger.debug(f"Identity tokens were fetched.")
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


# ! Implement blacklisted users!
async def authenticate_node_client(
    *,
    role: NodeRoles,
    instances: tuple[Namespace, Database],
) -> None:  # Create a pydantic model from this.

    # Inserted from this context due to circular import.
    from utils.processors import ensure_input_prompt

    user_credentials: tuple[CredentialContext, CredentialContext] | None = None

    logger.debug("Attempting to authenticate ...")

    if env.get("NODE_USERNAME", None) is None and env.get("NODE_PWD", None) is None:
        logger.debug(
            "Environment file doesn't contain the values for 'NODE_USERNAME' and/or 'NODE_PWD' or is entirely missing. Assuming first-time instance."
        )

        logger.info(
            f"The system will create an `auth_token` for you to register yourself as a {NodeRoles.MASTER.name}. Please enter your email address."
        )

        while True:
            try:
                email_address: EmailStr = await ensure_input_prompt(
                    input_context="Email Address",
                    hide_fields=False,
                    generalized_context="email address",
                    additional_context="You will have to restart the instance if you confirmed it late that it was a mistake!",
                )

                generated_token: str = generate_auth_token()

                insert_generated_token_stmt = auth_codes.insert().values(
                    code=generated_token,
                    account_type=UserEntity.NODE_USER,
                    to_email=email_address,
                    expiration=datetime.now() + timedelta(days=2),
                )

                await instances[1].execute(insert_generated_token_stmt)

                await get_email_instance().send(
                    content=f"<html><body><h1>Register Auth Code from Folioblocks!</h1><p>Thank you for taking interest! To continue, please enter the authentication code for the registration. <b>DO NOT SHARE THIS TO ANYONE.</b></p><br><br><h4>Auth Code: {generated_token}<b></b></h4><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
                    subject="Register Auth Code for Registration @ Folioblocks",
                    to=email_address,
                )

            # ! Assumes email service is running, so unhandled it for now because complexity rises.
            except IntegrityError as e:
                logger.critical(
                    f"Your input matches one of the records for `{NodeRoles.MASTER.name} registration.` Are you attempting to restart instance? Please delete the generated files and try again."
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
                    f"http://{instances[0].host}:{instances[0].port}/entity/login"
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
    ) -> None:

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
                        if user_role is not each_role:
                            continue
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