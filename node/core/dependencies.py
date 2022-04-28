"""
Dependencies (dependencies.py) | Contains a set of functions and attributes that is classified to run under FastAPI.Depends and a sub-dependencies of `depends`. Some attributes are required for the sake of authenticating the client for operation.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from argparse import Namespace
from asyncio import create_task, sleep
from base64 import b32encode
from datetime import datetime, timedelta
from http import HTTPStatus
from logging import Logger, getLogger
from os import environ as env
from secrets import token_hex
from sqlite3 import IntegrityError
from typing import Any, Final, Mapping
from uuid import uuid4

from aiohttp import ClientError, ClientResponse
from blueprint.models import associated_nodes, auth_codes, tokens, users
from blueprint.schemas import EntityLoginResult
from databases import Database
from fastapi import Depends, Header, HTTPException
from pydantic import EmailStr
from pyotp import TOTP
from sqlalchemy import and_, false, func, select, true
from sqlalchemy.sql.expression import Insert, Select, Update
from utils.http import get_http_client_instance

from core.constants import (
    ADDRESS_UUID_KEY_PREFIX,
    ASYNC_TARGET_LOOP,
    AUTH_CODE_MAX_CONTEXT,
    AUTH_CODE_MIN_CONTEXT,
    AUTH_ENV_FILE_NAME,
    BLOCKCHAIN_CONSENSUS_SLEEP_BASE_VALUE,
    TOTP_PASSCODE_REFRESH_INTERVAL,
    TOTP_VALID_WINDOW_SECONDS,
    AddressUUID,
    ArgsPlusDatabaseInstances,
    CredentialContext,
    HTTPQueueMethods,
    IdentityTokens,
    JWTToken,
    NodeType,
    TokenStatus,
    URLAddress,
    UserCredentials,
    UserEntity,
    random_generator,
)

args_value: Namespace
identity_tokens: IdentityTokens
db_instance: Database
logger: Logger = getLogger(ASYNC_TARGET_LOOP)
master_node_properties: dict[str, str] = {}


def store_args_value(args: Namespace) -> None:
    logger.debug(f"Argument values from `Argparse` has been stored. | Context: {args}")
    global args_value
    args_value = args


def get_args_values() -> Namespace:
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


def generate_auth_token() -> str:
    generated: str = token_hex(
        random_generator.randint(AUTH_CODE_MIN_CONTEXT, AUTH_CODE_MAX_CONTEXT)
    )
    logger.debug(
        f"Auth token generated with the following constraints: Min Length is {AUTH_CODE_MIN_CONTEXT}, Max Length is {AUTH_CODE_MAX_CONTEXT}. | Context: {generated}"
    )
    return generated


def generate_consensus_sleep_time(*, block_timer: int) -> float:
    return (
        random_generator.uniform(BLOCKCHAIN_CONSENSUS_SLEEP_BASE_VALUE, block_timer)
        * block_timer
    )  # * `block_timer` can be used as a multiplier for given other time to participate.


def generate_uuid_user() -> AddressUUID:
    return AddressUUID(f"{ADDRESS_UUID_KEY_PREFIX}:{uuid4().hex}")


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

        master_email_address: EmailStr = EmailStr()
        while True:
            try:
                logger.info(
                    f"As a {role.name}, {f'The system will perform to create keys such as an `auth_token` for you to register and authenticate yourself.' if role is NodeType.MASTER_NODE else f'you need to enter credentials for you to enter in blockchain.'} | Please enter your email address first."
                )
                if role is NodeType.MASTER_NODE:
                    # - Check for an existing email in the database.
                    # @o This was intended, especially when the administrator accidentally hits `CTRL+C` or `CTRL+BREAK` after master node email registration.
                    # @o This was useful to avoid re-entering email.

                    logger.info(
                        "Checking previous email if there's any, even on new-instance."
                    )
                    check_previous_registered_email_query: Select = select(
                        [auth_codes.c.to_email]
                    ).where(
                        (auth_codes.c.is_used == true())
                        & (auth_codes.c.account_type == UserEntity.MASTER_NODE_USER)
                    )

                    previous_registered_email = await instances[1].fetch_one(
                        check_previous_registered_email_query
                    )

                    if previous_registered_email is None:
                        logger.debug(
                            "Checking for emails that haven't used their auth code ..."
                        )

                        unused_code_email_query = select(
                            [auth_codes.c.to_email, auth_codes.c.expiration]
                        ).where(
                            and_(
                                auth_codes.c.is_used == false(),
                                auth_codes.c.account_type
                                == UserEntity.MASTER_NODE_USER,
                            )
                        )

                        unused_code_email = await instances[1].fetch_val(
                            unused_code_email_query
                        )

                        master_email_address = EmailStr()
                        generated_token: str

                        if unused_code_email is None:
                            logger.debug(
                                f"There are no existing previous email registered for {UserEntity.MASTER_NODE_USER}."
                            )
                            master_email_address = await ensure_input_prompt(
                                input_context="MASTER Email Address",
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
                                new_code_from_previous_email_query: Update = (
                                    auth_codes.update()
                                    .where(
                                        auth_codes.c.to_email
                                        == unused_code_email.to_email
                                    )
                                    .values(code=generated_token)
                                )

                                await instances[1].execute(
                                    new_code_from_previous_email_query
                                )
                                master_email_address = EmailStr(
                                    unused_code_email.to_email
                                )

                            else:
                                logger.warning(
                                    f"An email address associated to {unused_code_email.to_email} has its `auth_code` not yet expired. Please use it as possible!"
                                )
                                master_email_address = EmailStr(
                                    unused_code_email.to_email
                                )

                        if unused_code_email is None or (
                            unused_code_email is not None
                            and datetime.now() > unused_code_email.expiration
                        ):
                            from utils.email import get_email_instance

                            create_task(
                                get_email_instance().send(
                                    content=f"<html><body><h1>Self-Service: MASTER Node's Auth Code from Folioblocks!</h1><p>Thank you for taking interest! To continue, please enter the authentication code for the registration. <b>DO NOT SHARE THIS TO ANYONE.</b></p><br><br><h4>Auth Code: {generated_token}<b></b></h4><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
                                    subject="Register Auth Code for Master Node Registration @ Folioblocks",
                                    to=master_email_address,
                                ),
                                name=f"{get_email_instance.__name__}_send_auth_for_registration",
                            )

                            insert_generated_token_query: Insert = (
                                auth_codes.insert().values(
                                    code=generated_token,
                                    account_type=UserEntity.MASTER_NODE_USER,
                                    to_email=master_email_address,
                                    expiration=datetime.now() + timedelta(days=2),
                                )
                            )

                            await instances[1].execute(insert_generated_token_query)

                    else:
                        logger.info(
                            "Previous entry to registration of master email has been retrieved and is identified as registered. Skipping registration."
                        )
                        master_email_address = EmailStr(previous_registered_email)

                # - After extra handling some functions for validating email address, we can now do register.
                resolved_context_fields: list[str]
                resolved_hidden_fields: list[bool]

                if role is NodeType.MASTER_NODE:
                    resolved_context_fields, resolved_hidden_fields = [
                        "MASTER Node Username",
                        "MASTER Node Password",
                        "Auth Acceptance Code",
                    ], [False, True, False]

                else:
                    resolved_context_fields, resolved_hidden_fields = [
                        "Personal E-Mail representing this ARCHIVAL Node",
                        "ARCHIVAL Node Username",
                        "ARCHIVAL Node Password",
                        "Auth Acceptance Code",
                    ], [False, False, True, False]

                # NOTE I cannot implement password-checking because I have no time to do it.
                inputted_credentials: list[Any] = await ensure_input_prompt(
                    input_context=resolved_context_fields,
                    hide_input_from_field=resolved_hidden_fields,
                    generalized_context="credentials",
                    additional_context="You will have to ensure it this time to avoid potential conflicts from the startup!",
                    enable_async=True,
                )

                # @o What is being resolved here is basically the index declaration. Since there's no other way to DRY this (in smartest and cleanest way) by dynamically decrementing the offset by one. We should go for re-declaration method instead.
                resolved_data: dict[str, str] = (
                    {
                        "username": inputted_credentials[0],
                        "password": inputted_credentials[1],
                        "auth_code": inputted_credentials[2],
                    }
                    if role is NodeType.MASTER_NODE
                    else {
                        "username": inputted_credentials[1],
                        "password": inputted_credentials[2],
                        "auth_code": inputted_credentials[3],
                    }
                )

                resolved_origin: tuple[str, int] = (
                    (get_args_values().node_host, get_args_values().node_port)
                    if role is NodeType.MASTER_NODE
                    else (instances[0].target_host, instances[0].target_port)
                )

                register_node: ClientResponse = (
                    await get_http_client_instance().enqueue_request(
                        url=URLAddress(
                            f"{resolved_origin[0]}:{resolved_origin[1]}/entity/register"
                        ),
                        method=HTTPQueueMethods.POST,
                        do_not_retry=True,
                        await_result_immediate=True,
                        data={
                            "email": inputted_credentials[0]
                            if role is NodeType.ARCHIVAL_MINER_NODE
                            else master_email_address,
                            **resolved_data,
                        },
                        name=f"register_node_{resolved_data['auth_code'][-4:]}",
                    )
                )

                if not register_node.ok:
                    logger.error(
                        f"There seems to be an error during request. Please check recent log regarding HTTP requests and try again."
                    )
                    continue

                resolved_env_contents: str = (  # ! Nope, I don't want to complicate this further. I have an idea though, but no, just don't.
                    f"NODE_USERNAME={inputted_credentials[1]}\nNODE_PWD={inputted_credentials[2]}\nAUTH_ACCEPTANCE_CODE={inputted_credentials[3]}\n"
                    if role is NodeType.ARCHIVAL_MINER_NODE
                    else f"NODE_USERNAME={inputted_credentials[0]}\nNODE_PWD={inputted_credentials[1]}\n"
                )

                # ! This only checks the whole variables as-is, NOT per variable. I don't want to complicate this further.
                if (
                    env.get("NODE_USERNAME", None) is None
                    and env.get("NODE_PWD", None) is None
                    and (
                        role is NodeType.MASTER_NODE
                        or role is NodeType.ARCHIVAL_MINER_NODE
                        and env.get("AUTH_ACCEPTANCE_CODE", None) is None
                    )
                ):

                    with open(AUTH_ENV_FILE_NAME, "a") as env_writer:
                        env_writer.write(resolved_env_contents)

                    logger.info("Credentials invoked in the environment file.")

                    from utils.processors import load_env

                    load_env()
                    logger.debug(
                        "Environment file has been loaded due to new credentials invoked."
                    )

                logger.info(f"{role.name} registration successful!")

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
            and role is NodeType.MASTER_NODE
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
            if role is NodeType.MASTER_NODE:
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
                    url=URLAddress(f"{resolved_host}:{resolved_port}/entity/login"),
                    method=HTTPQueueMethods.POST,
                    await_result_immediate=True,
                    do_not_retry=True,
                    data={
                        "username": user_credentials[0],
                        "password": user_credentials[1],
                    },
                    name=f"node_login_as_{role.name.lower()}",
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

                    if resolve_entity_to_role.value != get_args_values().node_role:
                        from utils.processors import unconventional_terminate

                        unconventional_terminate(
                            message=f"Node was able to login successfully but the acccount type is not suitable for the type of instance. Account has a type suitable `for {resolve_entity_to_role}`, got {get_args_values().node_role} instead.",
                            early=True,
                        )

                    # * With this, we should also save the context by using store_auth_token().
                    store_identity_tokens(
                        (
                            AddressUUID(resolved_model.user_address),
                            JWTToken(resolved_model.jwt_token),
                        )
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
        self,
        *,
        _as: UserEntity | list[UserEntity] | None = None,
        blockchain_related: bool = False,
        return_token: bool = False,
        return_address_from_token: bool = False,
    ) -> None:
        self.__as: UserEntity | list[UserEntity] | None = _as
        self.__blockchain_related: Final[bool] = blockchain_related
        self.__return_token: bool = return_token
        self.__return_address_from_token: bool = return_address_from_token

    async def __call__(
        self,
        x_token: JWTToken
        | None = Header(..., description="The token that is inferred for validation."),
        x_certificate_token: str
        | None = Header(
            None,
            description=f"The certificate token that proves the consensus negotiation between {NodeType.ARCHIVAL_MINER_NODE.name} and {NodeType.MASTER_NODE.name}",
        ),
        database_instance: Database = Depends(get_database_instance),
    ) -> JWTToken | AddressUUID | None:

        if x_token is not None:
            token_to_user_query: Select = select([tokens.c.from_user]).where(
                (tokens.c.token == x_token) & (tokens.c.state != TokenStatus.EXPIRED)
            )

            user_address = await database_instance.fetch_val(token_to_user_query)

            if user_address is not None:  # type: ignore

                # ! I didn't use the Metadata().select() because its parameter `whereclause` prohibits selective column to return.
                # * Therefore use the general purpose sqlalchemy.select instead.
                fetch_user_role_query = select([users.c.type]).where(
                    users.c.unique_address == user_address  # type: ignore
                )

                user_role: Mapping = await database_instance.fetch_val(
                    fetch_user_role_query
                )

                # * Exception variables, for use later.
                condition_unmet_message: str = f"The role of this user is prohibited from running this method. | Allowed roles: {self.__as}"
                condition_unmet_http_code: HTTPStatus = HTTPStatus.FORBIDDEN

                user_role_sufficient: bool = False
                if isinstance(self.__as, list):
                    for each_role in self.__as:
                        if user_role is each_role:  # type: ignore
                            user_role_sufficient = True

                else:
                    if user_role is self.__as:  # type: ignore
                        user_role_sufficient = True

                if not user_role_sufficient:
                    raise HTTPException(
                        detail=condition_unmet_message,
                        status_code=condition_unmet_http_code,
                    )

                # # Contradiction between `__return_token` and `__return_address_from_token`.
                # @o For some reason, I don't want to return them both because there is like a potential redundancy upon the implementation who uses this class method.
                # - Even though I'm aware that I may have duplicated the code by querying the same thing again, I don't want it to happen from other future implementations, ie. Dashboard API.
                # * Adjustment of code will take soon and not this time as of the time of this writing due to very hectic schedule where I need to finish this as soon as possible.
                # ! Time of writing is 04/29/2022 at 12:53am.

                # - Code to execute whenthe instance of `user_role` is `UserEntity` and `_return_token` is invoked and `__return_address_from_token` is `False`.
                if (
                    self.__return_token
                    and not self.__return_address_from_token
                    and isinstance(user_role, UserEntity)
                ):
                    return x_token

                # - Code to execute whenthe instance of `user_role` is `UserEntity` and `_return_token` is not invoked and `__return_address_from_token` is `True`.
                if (
                    not self.__return_token
                    and self.__return_address_from_token
                    and isinstance(user_role, UserEntity)
                ):
                    return AddressUUID(user_address)

                if (
                    self.__return_token and self.__return_address_from_token
                ):  # ! Ignore returned instance.
                    raise HTTPException(
                        detail="Returning token and address is not possible. If you see this message, please report to the developers as this was an internal condition conflict.",
                        status_code=HTTPStatus.CONFLICT,
                    )

                # - If no other specific conditions have been specified, ensure that we return if the token has been matched.
                if user_address is not None:
                    return None

        # - This condition checks whether this operation is `blockchain_based`, and it contains `x_certificate_token`.
        if self.__blockchain_related and x_certificate_token is not None:
            certificate_token_query: Select = select([func.count()]).where(
                associated_nodes.c.certificate == x_certificate_token
            )
            certificate_count_count = await database_instance.fetch_val(
                certificate_token_query
            )

            if certificate_count_count:
                return None

        raise HTTPException(
            detail="You are unauthorized to access this endpoint.",
            status_code=HTTPStatus.UNAUTHORIZED,
        )


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

    identity: IdentityTokens | None = get_identity_tokens()

    if totp_instance is None and identity is not None:
        env_secret: str | None = env.get("AUTH_KEY", None)
        env_auth: str | None = env.get("SECRET_KEY", None)

        if env_secret is not None and env_auth is not None:
            totp_instance = PasscodeTOTP(
                base_code=[env_secret, env_auth],
                interval=TOTP_PASSCODE_REFRESH_INTERVAL,
                issuer=identity_tokens[0],
            )
            return totp_instance

    elif totp_instance is None or identity is None:
        logger.error(
            f"The environment file `{AUTH_ENV_FILE_NAME}` doesn't contain the following key `AUTH_KEY` or `SECRET_KEY`. Is the this node instance initializing? Please wait and try again."
        )
        return None

    return totp_instance


# # Passcode Generators — END
