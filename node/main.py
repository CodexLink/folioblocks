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
from asyncio import Task, create_task, sleep, wait
from datetime import datetime
from errno import EADDRINUSE, EADDRNOTAVAIL
from logging.config import dictConfig
from socket import AF_INET, SOCK_STREAM, error, socket
from typing import Any

import uvicorn
from aiohttp import ClientResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from api.admin import admin_router
from api.dashboard import dashboard_router
from api.explorer import explorer_router
from blueprint.models import tokens, users
from blueprint.schemas import Tokens
from core.args import args_handler as ArgsHandler
from core.blockchain import BlockchainMechanism, get_blockchain_instance
from core.constants import (
    ASGI_APP_TARGET,
    ASYNC_TARGET_LOOP,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOWED_HEADERS,
    CORS_ALLOWED_METHODS,
    CORS_ALLOWED_ORIGINS,
    MASTER_NODE_IP_ADDR,
    MASTER_NODE_IP_PORT,
    MASTER_NODE_IP_PORT_CEILING,
    MASTER_NODE_IP_PORT_FLOOR,
    MASTER_NODE_LIMIT_CONNECTED_NODES,
    REF_MASTER_BLOCKCHAIN_ADDRESS,
    REF_MASTER_BLOCKCHAIN_PORT,
    AddressUUID,
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
    set_master_node_properties,
    store_args_value,
)
from core.email import EmailService, get_email_instance
from core.logger import LoggerHandler
from utils.http import HTTPClient, get_http_client_instance
from utils.processors import (
    close_resources,
    initialize_resources_and_return_db_context,
    look_for_nodes,
    supress_exceptions_and_warnings,
    unconventional_terminate,
)

"""
# # Startup Dependencies
- A set of initialized objects that runs before the uvicorn async context. These are out-of-scope due to the nature of FastAPI uninstantiable by nature under class context.

"""
parsed_args: Namespace = ArgsHandler.parse_args()
store_args_value(parsed_args)

"""
# About these late import of routers.
@o Since these API endpoints require evaluation from the `parsed_args`, import them after storing `parsed_args` for them to access later.
@o They need to access these so that certain endpoints will be excluded based on the `parsed_args.prefer_role`.
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

Several roles prohibits the use of other functionalities that is designed for the master nodes.

* About design:
FastAPI doesn't seem to support class-based views by nature. Even when fastapi-utils provides that capability, I dont trust its functionality anymore due to the nature of FastAPI being too far than fastapi-utils can keep up.
Meaning, that tool may be outdated.` Hacking it like what I did in `CodexLink/discord-activity-badge` would take
my time more than making other features, which I still haven't done.

"""
api_handler: FastAPI = FastAPI()

api_handler.include_router(node_router)

if parsed_args.prefer_role == NodeType.MASTER_NODE.name:
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
    logger.info(
        f"Step 0 (Argument Check) | Detected as {NodeType.MASTER_NODE.name if parsed_args.prefer_role == NodeType.MASTER_NODE.name else NodeType.ARCHIVAL_MINER_NODE.name} ..."
    )

    await get_http_client_instance().initialize()  # * Initialize the HTTP client for such requests.

    await initialize_resources_and_return_db_context(
        runtime=RuntimeLoopContext(__name__),
        role=NodeType(parsed_args.prefer_role),
        auth_key=parsed_args.key_file[0] if parsed_args.key_file is not None else None,
    )

    # TODO: Insert HTTP request through here of looking for the master node. With that, save that from the env file later on.
    if parsed_args.prefer_role == NodeType.ARCHIVAL_MINER_NODE.name:
        for master_node_port_candidate in range(
            MASTER_NODE_IP_PORT_FLOOR, MASTER_NODE_IP_PORT_CEILING + 1
        ):
            evaluated_master_port: int = (
                MASTER_NODE_IP_PORT + master_node_port_candidate
            )
            master_node_response, _ = await wait(
                {
                    get_http_client_instance().enqueue_request(
                        url=URLAddress(
                            f"http://{MASTER_NODE_IP_ADDR}:{evaluated_master_port}/explorer/chain"
                        ),
                        method=HTTPQueueMethods.GET,
                        await_result_immediate=True,
                        name=f"validate_master_node_conn_iter_{master_node_port_candidate}",
                    )
                }
            )

            try:
                stored_response: Task = master_node_response.pop().result()
                if not isinstance(stored_response, ClientResponse):
                    raise KeyError  # @o Since we are displaying the message, raise `KeyError` to hit the log to display.

                # - Since we do understand that it may be a `MASTER` node, then save its URL then attempt to negotiate by logging to them later.

                set_master_node_properties(
                    key=REF_MASTER_BLOCKCHAIN_ADDRESS, context=MASTER_NODE_IP_ADDR
                )
                set_master_node_properties(
                    key=REF_MASTER_BLOCKCHAIN_PORT, context=evaluated_master_port
                )

                logger.info(
                    f"Master node found at {MASTER_NODE_IP_ADDR}:{evaluated_master_port}! (Assumption after response)"
                )

                break

            except KeyError:
                logger.error(
                    f"Response for the {MASTER_NODE_IP_ADDR}:{evaluated_master_port} has returned okay but contains nothing (client response), continuing to find the right address ..."
                )
                continue

        # @o When we didn't get anything, then terminate.
        if not get_master_node_properties(all=True).__len__():
            unconventional_terminate(
                message=f"Multiple retries of establishing connection to the master node IP address '{MASTER_NODE_IP_ADDR}', within the range of port {MASTER_NODE_IP_PORT + MASTER_NODE_IP_PORT_FLOOR} to {MASTER_NODE_IP_PORT + MASTER_NODE_IP_PORT_CEILING} were failed! Please check the IP address of the master node and try again.",
            )

    await get_database_instance().connect()  # * Initialize the database.

    create_task(post_initialize())

    # TODO: Post-Feature (Low-Priority) | Should check for the file of the JSON if still the same as before via database with the use of stored and computed hash.


async def post_initialize() -> None:
    """
    - An extension of the initialize() startup function without blocking the instance of uvicorn.

    - By continously awaiting tasks from tbe initialize() function, we can't do anything unless we left out of it or do asyncio.create_task() to get out-of-scope with initialize().

    - Tasks moved from the initialize() function may adjust to concurrently run the instance while doing other several checks.
    """

    if parsed_args.prefer_role == NodeType.ARCHIVAL_MINER_NODE.name:
        parsed_args.host, parsed_args.port = get_master_node_properties(
            key="MASTER_NODE_ADDRESS"
        ), get_master_node_properties(key="MASTER_NODE_PORT")

    await authenticate_node_client(
        role=NodeType(parsed_args.prefer_role),
        instances=(parsed_args, get_database_instance()),
    )

    if (  ## Ensure that the email services were activated.
        parsed_args.prefer_role == NodeType.MASTER_NODE.name
    ):
        await look_for_nodes(
            role=parsed_args.prefer_role, host=parsed_args.host, port=parsed_args.port
        )

    # * In the end, both NodeType.MASTER_NODE and NodeType.ARCHIVAL_MINER_NODE will initialize their local or universal (depending on the role) blockchain file.
    create_task(
        get_blockchain_instance(role=NodeType(parsed_args.prefer_role)).initialize()
    )

    # * We also need to check for other parts if this instance has any other task to send with the master node. Otherwise, have to resolve that before we able to send some data.
    logger.info(
        "Step 3.2 | Attempting to sync to the blockchain state from the master node ...."
    )


@api_handler.on_event("shutdown")
async def terminate() -> None:
    """
    TODO: Ensure on services like blockchain, remove or finish any request or finish the consensus.
    """
    # Supress exceptions and warnings.
    # @o Why? Because there are some sessions and asyncio-related exceptions and warnings are technically polluting the console even though everything is resolved.
    # @o With that, it is expected that this is unethical as ignoring messages and other stuff is indeed ignorant from the errors.
    # @o But trust me, this is needed in the context of some errors that can't be handled because they are in internal and is not directly affecting components who uses it.

    supress_exceptions_and_warnings()
    identity_tokens: IdentityTokens | None = get_identity_tokens()
    http_instance: HTTPClient = get_http_client_instance()
    # blockchain_instance: BlockchainMechanism = get_blockchain_instance()

    if parsed_args.prefer_role == NodeType.MASTER_NODE.name:
        email_instance: EmailService | None = get_email_instance()

        if email_instance is not None and email_instance.is_connected:
            email_instance.close()  # * Shutdown email service instance.
        # Remove the token related to this master, as well as, change the state of this master account to Offline.

        if identity_tokens is not None:
            token_to_invalidate_stmt = (
                tokens.update()
                .where(tokens.c.token == identity_tokens[1])
                .values(state=TokenStatus.LOGGED_OUT)
            )
            users.update().where(users.c.unique_address == identity_tokens[0]).values(
                activity=UserActivityState.OFFLINE
            )

            await get_database_instance().execute(token_to_invalidate_stmt)
            logger.info(
                f"Master Node's token has been invalidated due to Logout session."
            )
    else:
        if identity_tokens is not None:
            # - Ignore this if this node wasn't even logged on.

            await http_instance.enqueue_request(
                url=URLAddress(
                    f"http://{parsed_args.host}:{parsed_args.port}/entity/logout"
                ),
                method=HTTPQueueMethods.POST,
                headers={"X-Token": JWTToken(identity_tokens[1])},
            )

    if http_instance is not None:
        await http_instance.close(
            should_destroy=True
        )  # * Shutdown the HTTP client module.

    # if blockchain_instance is not None:
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

TODO: Consensus Method (Remember, that we need the consensus dependency or something.)
"""

if parsed_args.prefer_role == NodeType.MASTER_NODE.name:
    logger.warning(
        f"Several functions for the `{NodeType.MASTER_NODE} `were imported due to invocation of the role."
    )

    @api_handler.on_event("startup")
    @repeat_every(seconds=120, wait_first=True)
    async def jwt_invalidation() -> None:

        ## Query available tokens.
        token_query = tokens.select().where(tokens.c.state != TokenStatus.EXPIRED)
        tokens_available = await get_database_instance().fetch_all(token_query)

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
                    token_to_del = (
                        tokens.update()
                        .where(tokens.c.expiration == token.expiration)
                        .values(state=TokenStatus.EXPIRED)
                    )  ## Change the state of the token when past through expiration.

                    await get_database_instance().execute(token_to_del)

                    logger.info(
                        f"Token {token.token[:25]}(...) has been deleted due to expiration date {token.expiration}."
                    )  ## Character beyond 25th will be truncated. This is just a pure random though.


# * We cannot encapsulate the whole (main.py) module as there's a subprocess usage wherein there's a custom __main__ that will run this script. Doing so may cause recursion.
if __name__ == "__main__":
    # @o Assumes that this instance is instantiated along side `MASTER` node.
    # - It is recommended to choose other ports if this was instantiated outside of `MASTER` scope.

    if parsed_args.port == MASTER_NODE_IP_PORT:
        check_port_socket = socket(AF_INET, SOCK_STREAM)

        for each_port in range(0, MASTER_NODE_LIMIT_CONNECTED_NODES):
            iter_evaluated_port = MASTER_NODE_IP_PORT + each_port

            try:
                logger.info(f"Checking port {iter_evaluated_port} if available ...")
                check_port_socket.bind((MASTER_NODE_IP_ADDR, iter_evaluated_port))
                check_port_socket.close()

            except error as e:
                check_port_socket.close()  # * Close the socket to perform the next port.
                if e.errno == EADDRINUSE or e.errno == EADDRNOTAVAIL:
                    logger.info(f"Port {iter_evaluated_port} is already in used.")
                    continue

                else:
                    logger.info(f"Port {iter_evaluated_port} is available!")
                    parsed_args.port = iter_evaluated_port

                break

            finally:
                check_port_socket.close()

    uvicorn.run(
        app=ASGI_APP_TARGET,
        host=parsed_args.host,
        port=parsed_args.port,
        reload=parsed_args.local,
        log_config=logger_config,
        log_level=LoggerLevelCoverage(parsed_args.log_level).value.lower(),
    )
