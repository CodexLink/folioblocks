"""
Dependencies (dependencies.py) | Contains a set of functions and attributes that is classified to run under FastAPI.Depends and a sub-dependencies of `depends`. Some attributes are required for the sake of authenticating the client for operation.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from argparse import Namespace
from asyncio import sleep
from base64 import b32encode
from datetime import datetime, timedelta
from http import HTTPStatus
from logging import Logger, getLogger
from os import environ as env
from secrets import token_hex
from sqlite3 import IntegrityError
from typing import Any, Final

from aiohttp import (
    ClientError,
    ClientResponse,
)
from blueprint.models import auth_codes, tokens, users
from blueprint.schemas import EntityLoginResult, Tokens
from databases import Database
from fastapi import Depends, Header, HTTPException, Request
from pydantic import EmailStr
from pyotp import TOTP
from sqlalchemy import and_, false, select, true
from core.constants import IdentityTokens
from core.constants import ArgsPlusDatabaseInstances, UserCredentials
from core.constants import CredentialContext
from utils.http import get_http_client_instance
from sqlalchemy.sql.expression import Select
from core.constants import (
    ASYNC_TARGET_LOOP,
    AUTH_CODE_MAX_CONTEXT,
    AUTH_CODE_MIN_CONTEXT,
    AUTH_ENV_FILE_NAME,
    TOTP_PASSCODE_REFRESH_INTERVAL,
    TOTP_VALID_WINDOW_SECONDS,
    AddressUUID,
    HTTPQueueMethods,
    JWTToken,
    NodeType,
    TokenStatus,
    URLAddress,
    UserEntity,
    random_generator,
)
from sqlalchemy.sql.expression import Insert, Select, Update

args_value: Namespace
identity_tokens: IdentityTokens
db_instance: Database
logger: Logger = getLogger(ASYNC_TARGET_LOOP)
master_node_properties: dict[str, str] = {}


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


def get_database_instance() -> Database:
    global db_instance
    return db_instance


def store_identity_tokens(_tokens: tuple[AddressUUID, JWTToken]) -> None:
    logger.debug(
        f"Identity tokens were stored. | Context: (Address: {_tokens[0]}, JWT Token: {_tokens[1]})"
    )
    global identity_tokens
    identity_tokens = _tokens


def get_identity_tokens() -> IdentityTokens | None:
    try:
        global identity_tokens
        return identity_tokens
    except NameError:
        pass


def set_master_node_properties(*, key: str, context: Any) -> None:
    global master_node_properties
    master_node_properties[key] = context


def get_master_node_properties(
    *, all: bool = False, key: str | None = None
) -> dict[str, str] | str | int:
    global master_node_properties

    return (
        master_node_properties[key]
        if not all and key is not None
        else master_node_properties
    )


# TODO: Not sure why we have this function signature.
# def generate_auth_token(to: EmailStr, type: UserEntity, expires: timedelta) -> None:
def generate_auth_token() -> str:
    generated: str = token_hex(
        random_generator.randint(AUTH_CODE_MIN_CONTEXT, AUTH_CODE_MAX_CONTEXT)
    )
    logger.debug(
        f"Auth token generated with the following constraints: Min Length is {AUTH_CODE_MIN_CONTEXT}, Max Length is {AUTH_CODE_MAX_CONTEXT}. | Context: {generated}"
    )
    return generated


async def authenticate_node_client(
    *,
    role: NodeType,
    instances: ArgsPlusDatabaseInstances,
) -> None:

    from utils.processors import (
        ensure_input_prompt,
    )  # @o Imported inside method due to circular dependency.

    user_credentials: UserCredentials

    logger.debug(f"Attempting to authenticate node client as '{role.name}'...")

    if env.get("NODE_USERNAME", None) is None and env.get("NODE_PWD", None) is None:
        logger.warning(
            "Environment file doesn't contain the values for `NODE_USERNAME` and/or `NODE_PWD` or is entirely missing. Assuming first-time instance ..."
        )

        while True:
            try:
                logger.info(
                    f"As a {role.name}, {f'The system will perform to create keys such as an `auth_token` for you to register and authenticate yourself.' if role == NodeType.MASTER_NODE else f'you need to enter credentials for you to enter in blockchain.'} | Please enter your email address first."
                )
                if role is NodeType.MASTER_NODE:
                    # - Check for an existing email in the database.
                    # @o This was intended, especially when the administrator accidentally hits `CTRL+C` or `CTRL+BREAK` after master node email registration.
                    # @o This was useful to avoid re-entering email.

                    logger.info(
                        "Checking previous email if there's any, even on new-instance."
                    )
                    check_previous_registered_email_stmt: Select = select(
                        [auth_codes.c.to_email]
                    ).where(
                        (auth_codes.c.is_used == true())
                        & (auth_codes.c.account_type == UserEntity.MASTER_NODE_USER)
                    )

                    previous_registered_email = await instances[1].fetch_one(
                        check_previous_registered_email_stmt
                    )

                    if previous_registered_email is None:
                        logger.debug(
                            "Checking for emails that haven't used their auth code ..."
                        )

                        unused_code_email_stmt = select(
                            [auth_codes.c.to_email, auth_codes.c.expiration]
                        ).where(
                            and_(
                                auth_codes.c.is_used == false(),
                                auth_codes.c.account_type
                                == UserEntity.MASTER_NODE_USER,
                            )
                        )

                        unused_code_email = await instances[1].fetch_one(
                            unused_code_email_stmt
                        )

                        email_address: EmailStr = EmailStr()
                        generated_token: str = ""

                        if unused_code_email is None:
                            logger.debug(
                                f"There are no existing previous email registered for {UserEntity.MASTER_NODE_USER}."
                            )
                            email_address = await ensure_input_prompt(
                                input_context="Master Email Address",
                                hide_input_from_field=False,
                                generalized_context="master email address",
                                additional_context="You will have to restart the instance if you confirmed it late that it was a mistake!",
                            )
                            generated_token = generate_auth_token()

                        else:
                            if datetime.now() > unused_code_email.expiration:
                                logger.warning(
                                    f"An email address associated to {unused_code_email.to_email} haven't used its `auth_code` and is already expired. Sending new email for the new code. If you want to cancel this one, please reset the node files and start a new instance instead."
                                )

                                generated_token = generate_auth_token()
                                new_code_from_previous_email_stmt: Update = (
                                    auth_codes.update()
                                    .where(
                                        auth_codes.c.to_email
                                        == unused_code_email.to_email
                                    )
                                    .values(code=generated_token)
                                )

                                await instances[1].execute(
                                    new_code_from_previous_email_stmt
                                )
                                email_address = unused_code_email.to_email

                            else:
                                logger.warning(
                                    f"An email address associated to {unused_code_email.to_email} has its `auth_code` not yet expired. Please use it as possible!"
                                )

                        if unused_code_email is None or (
                            unused_code_email is not None
                            and datetime.now() > unused_code_email.expiration
                        ):
                            generated_token = generate_auth_token()

                            from core.email import get_email_instance

                            await get_email_instance().send(
                                content=f"<html><body><h1>Self-Service: MASTER Node's Auth Code from Folioblocks!</h1><p>Thank you for taking interest! To continue, please enter the authentication code for the registration. <b>DO NOT SHARE THIS TO ANYONE.</b></p><br><br><h4>Auth Code: {generated_token}<b></b></h4><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
                                subject="Register Auth Code for Master Node Registration @ Folioblocks",
                                to=email_address,
                            )

                            insert_generated_token_stmt: Insert = (
                                auth_codes.insert().values(
                                    code=generated_token,
                                    account_type=UserEntity.MASTER_NODE_USER,
                                    to_email=email_address,
                                    expiration=datetime.now() + timedelta(days=2),
                                )
                            )

                            await instances[1].execute(insert_generated_token_stmt)

                    else:
                        logger.info(
                            "Previous entry to registration of master email has been retrieved and is identified as registered. Skipping registration."
                        )

                    # * This functionality is only available on `MASTER` in local / self instance.
                else:  # @o Resolves to NodeType.ARCHIVAL_MINER_NODE.
                    inputted_credentials: list[Any] = await ensure_input_prompt(
                        input_context=[
                            "Personal e-mail representing this node",
                            "Node username",
                            "Node password",  # * I cannot implement password-checking because I have no time to do it.
                            "Auth code",
                        ],
                        hide_input_from_field=[False, False, True, False],
                        generalized_context="credentials",
                        additional_context="You will have to ensure it this time to avoid potential conflicts from the startup!",
                        enable_async=True,
                    )

                    register_node: Any = await get_http_client_instance().enqueue_request(
                        url=URLAddress(
                            f"http://{instances[0].target_host}:{instances[0].target_port}/entity/register"
                        ),
                        method=HTTPQueueMethods.POST,
                        do_not_retry=True,
                        await_result_immediate=True,
                        data={
                            "email": inputted_credentials[0],
                            "username": inputted_credentials[1],
                            "password": inputted_credentials[2],
                            "auth_code": inputted_credentials[3],
                        },
                    )

                    if not register_node.ok:
                        logger.error(
                            f"There seems to be an error during request. Please try again | Additional Info: {await register_node.json()}"
                        )
                        continue

                    logger.warning(
                        "Auth code will be used as auth acceptance for blockchain operation."
                    )
                    with open(AUTH_ENV_FILE_NAME, "a") as env_writer:
                        env_writer.write(
                            f"NODE_USERNAME={inputted_credentials[1]}\nNODE_PWD={inputted_credentials[2]}\nAUTH_ACCEPTANCE_CODE={inputted_credentials[3]}\n"
                        )

                    from utils.processors import load_env
                    load_env()

                    logger.info(f"{role} registration successful!")

            # ! Assumeing that the email service is running, I have to step away from this since complexity rises if I continue on improving it.
            except IntegrityError as e:
                from utils.processors import unconventional_terminate

                unconventional_terminate(
                    message=f"Your input matches one of the records for `{NodeType.MASTER_NODE.name} registration.` Are you attempting to restart instance? Please delete the generated files and try again.",
                )

            logger.info(
                f"A generated code has been sent or has been skipped. Please register from the '{instances[0].node_host}:{instances[0].node_port}/entity/register' endpoint and login with your credentials on the next prompt."
            )

            break

    while True:
        if (
            env.get("NODE_USERNAME", None) is None
            and env.get("NODE_PWD", None) is None
            and role == NodeType.MASTER_NODE
        ):
            user_credentials = await ensure_input_prompt(  # # 'Any' type for now.
                input_context=["MASTER Node Username", "MASTER Node Password"],
                hide_input_from_field=[False, True],
                generalized_context="username and password",
                additional_context="You will have to ensure it this time to avoid potential conflicts!",
                enable_async=True,
            )
        else:  # - Assumed as NodeType.ARCHIVAL_MINER_NODE.
            user_credentials = (
                CredentialContext(env.get("NODE_USERNAME", None)),
                CredentialContext(env.get("NODE_PWD", None)),
            )

        # Ensure that ENV will be covered here.
        try:
            if role == NodeType.MASTER_NODE:
                resolved_host, resolved_port = (
                    instances[0].node_host,
                    instances[0].node_port,
                )
            else:
                resolved_host, resolved_port = (
                    instances[0].target_host,
                    instances[0].target_port,
                )

            login_request: ClientResponse | None = (
                await get_http_client_instance().enqueue_request(
                    url=URLAddress(
                        f"http://{resolved_host}:{resolved_port}/entity/login"
                    ),
                    method=HTTPQueueMethods.POST,
                    await_result_immediate=True,
                    do_not_retry=True,
                    data={
                        "username": user_credentials[0],
                        "password": user_credentials[1],
                    },
                )
            )

            if isinstance(login_request, ClientResponse):
                if login_request.ok:
                    resolved_model = EntityLoginResult.parse_obj(
                        await login_request.json()
                    )  # * Resolve via pydantic.

                    resolve_entity_to_role = (
                        NodeType.MASTER_NODE
                        if resolved_model.user_role == UserEntity.MASTER_NODE_USER
                        else NodeType.ARCHIVAL_MINER_NODE
                    )

                    # TODO: Please test this one.
                    if resolve_entity_to_role.value != get_args_value().assigned_role:
                        from utils.processors import unconventional_terminate

                        unconventional_terminate(
                            message=f"Node was able to login successfully but the acccount type is not suitable for the type of instance. Account has a type suitable `for {resolve_entity_to_role}`, got {get_args_value().assigned_role} instead.",
                            early=True,
                        )

                    # With this, we should also save the context by using store_auth_token().
                    store_identity_tokens(
                        (
                            AddressUUID(resolved_model.user_address),
                            JWTToken(resolved_model.jwt_token),
                        )
                    )

                    # * Since we have a different way of registering `MASTER_NODE` (self-registration), we have to handle its output here.
                    if role == NodeType.MASTER_NODE:
                        with open(AUTH_ENV_FILE_NAME, "a") as env_writer:
                            env_writer.write(
                                f"NODE_USERNAME={user_credentials[0]}\nNODE_PWD={user_credentials[1]}\n"
                            )

                    logger.info(f"Authenticated as {resolved_model.user_address}.")
                    break

                else:
                    logger.error(
                        f"Credentials are incorrect! Please try again. | Object: {login_request} | Additional Info: {await login_request.json()}"
                    )
            else:
                logger.error(
                    f"Login request returned an invalid object! It returned {type(login_request)} instead of {ClientResponse}. This may be an issue with connectivitity. Please try again."
                )

            await sleep(1.5)
            continue

        # * This should cover the following exceptions: (ClientConnectorError, ClientConnectorSSLError, ClientConnectorCertificateError, and ClientConnectionError)
        except ClientError as e:
            logger.critical(
                f"There was an error during request. Please try again. | Context: {e}"
            )
            await sleep(1.5)
            continue


class EnsureAuthorized:
    def __init__(
        self, *, _as: UserEntity | list[UserEntity], blockchain_related: bool = False
    ) -> None:
        self._as: UserEntity | list[UserEntity] = _as
        self._blockchain_related: Final[bool] = blockchain_related

    async def __call__(
        self,
        request: Request,
        x_token: JWTToken = Header(
            ..., description="The token that is inferred for validation."
        ),
        x_certificate_token: str
        | None = Header(
            None,
            description=f"The certificate token that proves the negotiation between {NodeType.ARCHIVAL_MINER_NODE.name} and {NodeType.MASTER_NODE.name}",
        ),  # TODO: Type-hint.
        db: Database = Depends(get_database_instance),
    ) -> None:  # TODO.

        print("Debug from the call function, ", request, dir(request))

        if x_token:
            req_ref_token = tokens.select().where(
                (tokens.c.token == x_token) & (tokens.c.state != TokenStatus.EXPIRED)
            )

            req_token = await db.fetch_one(req_ref_token)

            if req_token:
                ref_token = Tokens.parse_obj(req_token)

                # ! I didn't use the Metadata().select() because its parameter `whereclause` prohibits selective column to return.
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

        if self._blockchain_related and x_certificate_token is not None:
            return

        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="You are unauthorized to access this endpoint.",
        )


# TODO: MAY BE DEPRECATED LATER.
def ensure_past_negotiations(
    *,
    identity: tuple[AddressUUID, JWTToken] = Depends(get_identity_tokens),
    db: Database = Depends(get_database_instance),
) -> bool:
    # Maybe query or use the current session or the Node ID.
    # We need to contact the other part to ensure that there is negotiations.
    return False


# # Passcode Generators — START


class PasscodeTOTP:
    def __init__(
        self, *, base_code: list[str] | str, interval: int = 10, issuer: str
    ) -> None:
        code: str = ""

        # - Resolve the `base_code` by appending or just using only one.
        if isinstance(base_code, list):
            for each_code_given in base_code:
                code += each_code_given

        elif isinstance(base_code, str):
            code = base_code

        else:
            from utils.processors import unconventional_terminate

            unconventional_terminate(
                message=f"Internal Error: The given parameters were not a type `{type(str)}` or `{type(list)}`. This is a developer-related issue. Please report as possible.",
            )

        # - Resolve by converting it into a consumable base32 output.
        resolved_code: str = b32encode(code.encode("utf-8")).decode("utf-8")
        self.otp_auth = TOTP(resolved_code, interval=interval, issuer=issuer)

    def get_code(self) -> str:
        return self.otp_auth.now()

    def verify(self, code: str) -> bool:
        return self.otp_auth.verify(code, valid_window=TOTP_VALID_WINDOW_SECONDS)


totp_instance: PasscodeTOTP | None = None


def get_totp_instance() -> PasscodeTOTP | None:
    global totp_instance

    if totp_instance is None:
        env_secret: str | None = env.get("AUTH_KEY", None)
        env_auth: str | None = env.get("SECRET_KEY", None)

        if env_secret is not None and env_auth is not None:
            totp_instance = PasscodeTOTP(
                base_code=[env_secret, env_auth],
                interval=TOTP_PASSCODE_REFRESH_INTERVAL,
                issuer=get_identity_tokens()[0],
            )

    else:
        logger.error(
            f"The environment key `AUTH_KEY` or `SECRET_KEY` is missing! Call this function when those fields exists from the `{AUTH_ENV_FILE_NAME}` file."
        )

    return totp_instance


# # Passcode Generators — END
