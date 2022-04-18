"""
API — Entrypoint for the Blockchain Node and Explorer API Components.
Each API category has been seperated to ease the preparation phase, since there are two types of nodes that will play the part of the blockchain network.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""
import logging
from argparse import Namespace
from asyncio import create_task, shield, sleep
from datetime import datetime
from errno import EADDRINUSE, EADDRNOTAVAIL
from logging.config import dictConfig
from os import environ as env
from socket import AF_INET, SOCK_STREAM, error, socket
from typing import Any, Final, Mapping

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from sqlalchemy.sql.expression import Insert, Select, Update

from api.admin import admin_router
from api.dashboard import dashboard_router
from api.explorer import explorer_router
from blueprint.models import tokens, users
from blueprint.schemas import Tokens
from core.args import args_handler as ArgsHandler
from core.blockchain import get_blockchain_instance
from core.constants import (
    ASGI_APP_TARGET,
    ASYNC_TARGET_LOOP,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOWED_HEADERS,
    CORS_ALLOWED_METHODS,
    CORS_ALLOWED_ORIGINS,
    REF_MASTER_BLOCKCHAIN_ADDRESS,
    REF_MASTER_BLOCKCHAIN_PORT,
    HTTPQueueMethods,
    IdentityTokens,
    JWTToken,
    LoggerLevelCoverage,
    NodeType,
    RuntimeLoopContext,
    TokenStatus,
    URLAddress,
    UserActivityState,
)
from core.dependencies import (
    authenticate_node_client,
    get_database_instance,
    get_identity_tokens,
    get_master_node_properties,
    store_args_value,
)
from core.email import EmailService, get_email_instance
from core.logger import LoggerHandler
from utils.http import HTTPClient, get_http_client_instance
from utils.processors import (
    close_resources,
    contact_master_node,
    initialize_resources_and_return_db_context,
    look_for_archival_nodes,
    supress_exceptions_and_warnings,
    unconventional_terminate,
)

"""
# # Startup Dependencies
- A set of initialized objects that runs before the uvicorn async context. These are out-of-scope due to the nature of FastAPI uninstantiable by nature under class context.

"""
parsed_args: Namespace = ArgsHandler.parse_args()

# *Resolve some literal parameters to Enum object.
parsed_args.node_role = (
    NodeType.MASTER_NODE
    if parsed_args.node_role == NodeType.MASTER_NODE.name
    else NodeType.ARCHIVAL_MINER_NODE
)
parsed_args.log_level = LoggerLevelCoverage(parsed_args.log_level)
store_args_value(parsed_args)

"""
# About these late import of routers.
@o Since these API endpoints require evaluation from the `parsed_args`, import them after storing `parsed_args` for them to access later.
@o They need to access these so that certain endpoints will be excluded based on the `parsed_args.node_role`.
! Note that their contents will change, so better understand the condition and its output as it may contain a router or just a set of functions to call for request to the `MASTER` node.
"""

from api.node import node_router

logger_config: dict[str, Any] = LoggerHandler.init(
    base_config=uvicorn.config.LOGGING_CONFIG,  # type: ignore # ???
    disable_file_logging=parsed_args.no_log_file,
    logger_level=LoggerLevelCoverage(parsed_args.log_level),
)

dictConfig(logger_config)
logger: logging.Logger = logging.getLogger(
    ASYNC_TARGET_LOOP
)  # # Note that, uvicorn will override this in the main thread.


"""
# # API Router Setup and Initialization

- Several roles prohibits the use of other functionalities that is designed for the master nodes.

* About design:
- FastAPI doesn't seem to support class-based views by nature. Even when fastapi-utils provides that capability, I dont trust its functionality anymore due to the nature of FastAPI being too far than fastapi-utils can keep up.
- Meaning, that tool may be outdated.` Hacking it like what I did in `CodexLink/discord-activity-badge` would take
my time more than making other features, which I still haven't done.

"""
api_handler: FastAPI = FastAPI()

api_handler.include_router(node_router)

if parsed_args.node_role is NodeType.MASTER_NODE:
    from api.entity import entity_router

    api_handler.include_router(admin_router)
    api_handler.include_router(entity_router)
    api_handler.include_router(dashboard_router)
    api_handler.include_router(explorer_router)

api_handler.add_middleware(
    CORSMiddleware,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_headers=CORS_ALLOWED_HEADERS,
    allow_methods=CORS_ALLOWED_METHODS,
    allow_origins=CORS_ALLOWED_ORIGINS,
)


@api_handler.on_event("startup")
async def pre_initialize() -> None:
    logger.info(f"Role Detected as {parsed_args.node_role} ...")

    # - Validate by checking if the email service would run.
    if (
        env.get("EMAIL_SERVER_ADDRESS", None) is not None
        and env.get("EMAIL_SERVER_PWD", None) is not None
        and parsed_args.node_role is NodeType.MASTER_NODE
    ):
        await get_email_instance().connect()

    await get_http_client_instance().initialize()  # * Initialize the HTTP client for such requests.

    await initialize_resources_and_return_db_context(
        runtime=RuntimeLoopContext(__name__),
        role=NodeType(parsed_args.node_role),
        auth_key=parsed_args.key_file[0] if parsed_args.key_file is not None else None,
    )

    if parsed_args.node_role is NodeType.ARCHIVAL_MINER_NODE:
        if parsed_args.target_host is None or parsed_args.target_port is None:
            unconventional_terminate(
                message=f"Your instance (as a {parsed_args.node_role}) requires a `TARGET_HOST` as well as `TARGET_PORT` to contact the master node blockchain. Please try again with those parameters supplied.",
            )

    await get_database_instance().connect()  # * Initialize the database.
    create_task(
        post_initialize(),
        name=f"{parsed_args.node_role.name.lower()}_run_{post_initialize.__name__}",
    )  # * Create this task instead of scoping out so that the server can instantiate.


async def post_initialize() -> None:
    """
    - An extension of the initialize() startup function without blocking the instance of uvicorn.
    - By continously awaiting tasks from tbe initialize() function, we can't do anything unless we left out of it or do asyncio.create_task() to get out-of-scope with initialize().
    - Tasks moved from the initialize() function may adjust to concurrently run the instance while doing other several checks.
    """

    await authenticate_node_client(
        role=NodeType(parsed_args.node_role),
        instances=(parsed_args, get_database_instance()),
    )

    # * I don't know, I don't like to complicate this with another complex conditional checking here. Try to visualize what will happen here on some certain extreme-isolated case condition.

    if parsed_args.node_role is NodeType.ARCHIVAL_MINER_NODE:
        # @o As an `ARCHIVAL_MINER_NODE`, store the target host address and port, which will be accessed later.
        if (
            env.get("NODE_USERNAME", None) is not None
            and env.get("NODE_PWD", None) is not None
        ):
            await contact_master_node(
                master_host=parsed_args.target_host,
                master_port=parsed_args.target_port,
            )

        parsed_args.target_host, parsed_args.target_port = get_master_node_properties(
            key=REF_MASTER_BLOCKCHAIN_ADDRESS
        ), get_master_node_properties(key=REF_MASTER_BLOCKCHAIN_PORT)

    else:  # * Resolved to NodeType.MASTER_NODE.
        await look_for_archival_nodes()

    # * In the end, both NodeType.MASTER_NODE and NodeType.ARCHIVAL_MINER_NODE will initialize their local or universal (depending on the role) blockchain file.
    create_task(
        get_blockchain_instance(role=parsed_args.node_role).initialize(),
        name=f"initialize_blockchain_as_{parsed_args.node_role.name.lower()}",
    )


@api_handler.on_event("shutdown")
async def terminate() -> None:
    # Supress exceptions and warnings.
    # @o Why? Because there are some sessions and asyncio-related exceptions and warnings are technically polluting the console even though everything is resolved.
    # @o With that, it is expected that this is unethical as ignoring messages and other stuff is indeed ignorant from the errors.
    # @o But trust me, this is needed in the context of some errors that can't be handled because they are in internal and is not directly affecting components who uses it.
    supress_exceptions_and_warnings()

    identity_tokens: IdentityTokens | None = get_identity_tokens()
    http_instance: HTTPClient = get_http_client_instance()
    # blockchain_instance: BlockchainMechanism = get_blockchain_instance()

    if parsed_args.node_role is NodeType.MASTER_NODE:
        email_instance: EmailService | None = get_email_instance()

        if email_instance is not None and email_instance.is_connected:
            email_instance.close()  # * Shutdown email service instance.

        # * Remove the token related to this master, as well as, change the state of this master account to Offline.
        if identity_tokens is not None:

            master_state: Update = (
                users.update()
                .where(users.c.unique_address == identity_tokens[0])
                .values(activity=UserActivityState.OFFLINE)
            )

            await get_database_instance().execute(master_state)
            logger.info(
                f"Master Node's token has been invalidated due to Logout session."
            )

    else:
        if identity_tokens is not None:

            # - Ignore this if this node wasn't logged on.
            await shield(
                http_instance.enqueue_request(
                    url=URLAddress(
                        f"{parsed_args.target_host}:{parsed_args.target_port}/entity/logout"
                    ),
                    method=HTTPQueueMethods.POST,
                    do_not_retry=True,
                    headers={"X-Token": JWTToken(identity_tokens[1])},
                    name=f"request_logout_node_as_{parsed_args.node_role.name.lower()}",
                )
            )

    if http_instance is not None:
        await http_instance.close(
            should_destroy=True
        )  # * Shutdown the HTTP client module.

    # if isinstance(blockchain_instance, BlockchainMechanism):
    #     await wait(
    #         {create_task(blockchain_instance.close())}
    #     )  # * Shutdown the blockchain instance. We really need to finish this off before doing anything else.

    await close_resources(
        key=parsed_args.key_file[0]
    )  # * When necessary services finished, close the resource, as well as the database to go back from their malformed structure.

    logger.info("Wait for 3 seconds to ensure that all processes closed down ...")
    await sleep(3)


"""
# Repeated Tasks
-These are the tasks that needs to be executed at certain amount of time to evaluate the blockchain consensus mechanism. Sooner or later,

"""

if parsed_args.node_role is NodeType.MASTER_NODE:
    logger.warning(
        f"Several functions for the `{NodeType.MASTER_NODE.name} `were imported due to invocation of the role."
    )

    @api_handler.on_event("startup")
    @repeat_every(seconds=120, wait_first=True)
    async def jwt_invalidation_on_users() -> None:

        ## Query available tokens.
        token_query: Select = tokens.select().where(
            (tokens.c.state != TokenStatus.EXPIRED)
            & (tokens.c.expiration.isnot(None))  # type: ignore
        )
        tokens_available: list[Mapping] = await get_database_instance().fetch_all(
            token_query
        )

        if not tokens_available:
            logger.warning("There are no tokens available to iterate as of the moment.")

        current_datetime: datetime = datetime.now()

        for each_tokens in tokens_available:
            token = Tokens.parse_obj(each_tokens)

            if token.expiration is not None:
                logger.debug(
                    f"@ Token {token.id} | JWT Invalidation Condition (of {current_datetime.isoformat()} vs. {token.expiration.isoformat()}) | '(Should be) >' {current_datetime > token.expiration} | '(Should be) ==' {current_datetime == token.expiration} | `<' {current_datetime < token.expiration}"
                )

                if current_datetime >= token.expiration:
                    token_to_del: Update = (
                        tokens.update()
                        .where(tokens.c.expiration == token.expiration)
                        .values(state=TokenStatus.EXPIRED)
                    )  # # Change the state of the token when past through expiration.

                    await get_database_instance().execute(token_to_del)

                    logger.info(
                        f"Token {token.token[:25]}(...) has been deleted due to expiration date {token.expiration}."
                    )  # # Character beyond 25th will be truncated. This is just a pure random though.


# * We cannot encapsulate the whole (main.py) module as there's a subprocess instantiated wherein there's a custom `__main__` that will run this script. Avoiding this technique will cause recursion.
if __name__ == "__main__":
    post_check_prefix_msg: Final[str] = "[ POSTCHECK ] |"
    port_socket_checker = socket(AF_INET, SOCK_STREAM)
    logger.info(f"{post_check_prefix_msg} Socket port checker initialized.")

    try:
        logger.info(
            f"{post_check_prefix_msg} Checking if this port {parsed_args.node_port} (at {parsed_args.node_host}) is available for allocation ..."
        )
        port_socket_checker.bind((parsed_args.node_host, parsed_args.node_port))
        port_socket_checker.close()

    except error as e:
        if e.errno == EADDRINUSE or e.errno == EADDRNOTAVAIL:
            unconventional_terminate(
                message=f"{post_check_prefix_msg} Port {parsed_args.node_port} (at {parsed_args.node_host}) is already in used or is not available. Please check your IP address and your port and try again.",
                early=True,
            )

    finally:
        port_socket_checker.close()

    logger.info(
        f"{post_check_prefix_msg} Port {parsed_args.node_port} (at {parsed_args.node_host}) is available for instantiation!"
    )

    uvicorn.run(
        app=ASGI_APP_TARGET,
        host=parsed_args.node_host,
        port=parsed_args.node_port,
        log_config=logger_config,
        log_level=parsed_args.log_level.value.lower(),
    )
