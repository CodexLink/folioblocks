"""
Dependencies (dependencies.py) | Contains a set of functions and attributes that is classified to run under FastAPI.Depends and a sub-dependencies of `depends`. Some attributes are required for the sake of authenticating the client for operation.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from argparse import Namespace
from asyncio import sleep
from datetime import timedelta
from http import HTTPStatus
from logging import Logger, getLogger
from os import environ as env
from random import randint
from secrets import token_hex

from aiohttp import BasicAuth, ClientSession
from blueprint.models import auth_codes, tokens, users
from blueprint.schemas import EntityLoginResult, Tokens
from databases import Database
from fastapi import Depends, Header, HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from node.core.constants import AddressUUID
from utils.processors import ensure_input_prompt, hash_context

from core.constants import (
    ASYNC_TARGET_LOOP,
    AUTH_ENV_FILE_NAME,
    CredentialContext,
    HashedData,
    JWTToken,
    NodeRoles,
    RawData,
    TokenStatus,
    UserEntity,
)
from core.email import get_email_instance_or_initialize

identity_tokens: tuple[AddressUUID, JWTToken]
db_instance: Database
logger: Logger = getLogger(ASYNC_TARGET_LOOP)


def store_db_instance(instance: Database) -> None:
    global db_instance
    db_instance = instance


def get_db_instance() -> Database:
    global db_instance
    return db_instance


def store_identity_tokens(_tokens: tuple[AddressUUID, JWTToken]) -> None:
    global identity_tokens
    identity_tokens = _tokens


def get_identity_token() -> tuple[AddressUUID, JWTToken]:
    global identity_tokens
    return identity_tokens


def generate_auth_token(to: EmailStr, type: UserEntity, expires: timedelta) -> None:
    # To identify who the heck did it, we need to ensure fetch its token or otherwise put it to None. But we need to ensure that anyone who uses this must be authenticated. This function will be used by master anyway.
    pass


# ! Implement blacklisted users!
async def authenticate_node_client(
    instances: tuple[Namespace, Database],
) -> None:  # Create a pydantic model from this.

    user_credentials: tuple[CredentialContext, CredentialContext] | None = None

    if env.get("NODE_USERNAME", None) is None and env.get("NODE_PWD", None) is None:
        logger.debug(
            "Environment file doesn't contain the values for 'NODE_USERNAME' and/or 'NODE_PWD' or is entirely missing. Assuming first-time instance."
        )

        logger.info(
            f"The system will create an auth_token for you to register yourself as a {NodeRoles.MASTER.name}. Please enter your email address:"
        )

        while True:
            email_address: EmailStr = ensure_input_prompt(
                "Email Address > ",
                False,
                "email address",
                "You will have to restart the instance if you confirmed it late that it was a mistake!",
            )

            await get_email_instance_or_initialize().send(
                content=f"<html><body><h1>Register Auth Code from olioblocks!</h1><p>Thank you for taking interest! To continue, please enter the authentication code for the registration. <b>DO NOT SHARE THIS TO ANYONE</b></p><br><br><h4>Auth Code: {token_hex(randint(6, 12))}<b></b></h4><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
                subject="Register Auth Code for Registration @ Folioblocks",
                to=email_address,
            )

            logger.info(
                f"A generated code has been sent. Please register from the '{instances[0].host}:{instances[0].port}/entity/register' endpoint. Once done, press any key to continue and put your `auth_code` to login."
            )

            break

        while True:
            auth_code = ensure_input_prompt("Auth Code >", False, "auth code", None)
            check_auth_stmt = (
                auth_codes.select().where(auth_codes.c.code == auth_code).count()
            )
            auth_result = await instances[1].fetch_one(check_auth_stmt)

            if not auth_result:
                logger.error(
                    "Auth code is not valid! Please enter again and check if you have mis-typed it."
                )
                continue

            logger.info(
                "Auth code is validated, please login and enter your credentials to save it from the environment file for future sessions."
            )
            break

        while True:
            if (
                env.get("NODE_USERNAME", None) is None
                and env.get("NODE_PWD", None) is None
            ):
                user_credentials = ensure_input_prompt(
                    ["Node Username > ", "Node Password > "],
                    [False, True],
                    "username and password",
                    "You will have to ensure it this time to avoid potential conflicts!",
                )

            # Create a session for this request.
            login_session = ClientSession()

            # Ensure that ENV will be covered here.
            login_req = await login_session.post(
                f"{instances[0].host}:{instances[0].port}/entity/login",
                auth=BasicAuth(
                    login=(
                        env.get("NODE_USERNAME", None)
                        if user_credentials is None
                        else user_credentials[0]
                    ),
                    password=(
                        env.get("NODE_PWD", None)
                        if user_credentials is None
                        else user_credentials[1]
                    ),
                ),
            )

            if login_req.ok:
                # Resolve via pydantic.
                resolved_model = EntityLoginResult.parse_obj(login_req.json())

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
                        hashed_pwd: HashedData = hash_context(
                            RawData(user_credentials[1])
                        )
                        env_writer.write(
                            f"NODE_USERNAME={user_credentials[0]}, NODE_PWD={hashed_pwd}"
                        )
                    return

            else:
                logger.critical("Credentials are incorrect! Please try again...")
                await sleep(3)
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


# TODO: Class version of this one soon.
def ensure_past_negotiations() -> bool:
    # Maybe query or use the current session or the Node ID.
    # We need to contact the other part to ensure that there is negotiations.
    return False
