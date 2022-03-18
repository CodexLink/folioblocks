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
from asyncio import create_task, get_event_loop, sleep
from datetime import datetime
from logging.config import dictConfig
from typing import Any

import uvicorn
from databases import Database
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from sqlalchemy import func, select

from api.admin import admin_router
from api.dashboard import dashboard_router
from api.entity import entity_router
from api.explorer import explorer_router
from api.node import node_router
from blueprint.models import tokens, users
from blueprint.schemas import Tokens
from core.args import args_handler as ArgsHandler
from core.constants import (
    ASGI_APP_TARGET,
    ASYNC_TARGET_LOOP,
    HTTPQueueMethods,
    JWTToken,
    LoggerLevelCoverage,
    NodeRoles,
    RuntimeLoopContext,
    TokenStatus,
    URLAddress,
)
from core.dependencies import authenticate_node_client, get_identity_tokens
from core.email import get_email_instance
from core.logger import LoggerHandler
from utils.http import get_http_client_instance
from utils.processors import (
    close_resources,
    initialize_resources_and_return_db_context,
    look_for_nodes,
)

"""
# # Startup Dependencies

A set of initialized objects that runs before the uvicorn async context. These are out-of-scope due to the nature of FastAPI uninstantiable by nature under class context.

"""
parsed_args: Namespace = ArgsHandler.parse_args()

logger_config: dict[str, Any] = LoggerHandler.init(
    base_config=uvicorn.config.LOGGING_CONFIG,  # type: ignore # ???
    disable_file_logging=parsed_args.no_log_file,
    logger_level=LoggerLevelCoverage(parsed_args.log_level),
)

dictConfig(logger_config)
logger: logging.Logger = logging.getLogger(
    ASYNC_TARGET_LOOP
)  # # Note that, uvicorn will override this in the main thread.


database_instance: Database = get_event_loop().run_until_complete(
    initialize_resources_and_return_db_context(
        runtime=RuntimeLoopContext(__name__),
        role=NodeRoles(parsed_args.prefer_role),
        auth_key=parsed_args.key_file[0] if parsed_args.key_file is not None else None,
    ),
)

# * We need to delay this email instance, otherwise it will look for potentially non-existing .env file if this system was initially instantiated for the first time.
from core.blockchain import get_blockchain_instance

"""
# # API Router Setup and Initialization

Several roles prohibits the use of other functionalities that is designed for the master nodes.

* About design:
FastAPI doesn't seem to support class-based views by nature. Even when fastapi-utils provides that capability, I dont trust its functionality anymore due to the nature of FastAPI being too far than fastapi-utils can keep up.
Meaning, that tool may be outdated. Hacking it like what I did in `CodexLink/discord-activity-badge` would take
my time more than making other features, which I still haven't done.

"""
api_handler: FastAPI = FastAPI()

api_handler.include_router(entity_router)  # # WARNING REGARDING SIDE NODE.
api_handler.include_router(node_router)  # * Email can be used here.

if parsed_args.prefer_role is not NodeRoles.SIDE:
    api_handler.include_router(admin_router)
    api_handler.include_router(dashboard_router)  # * Email can be used here.
    api_handler.include_router(explorer_router)


@api_handler.on_event("startup")
async def pre_initialize() -> None:
    logger.info(
        f"Step 0 (Argument Check) | Detected as {NodeRoles.MASTER.name if parsed_args.prefer_role == NodeRoles.MASTER.name else NodeRoles.SIDE.name} ..."
    )

    await database_instance.connect()  # Initialize the database.
    await get_http_client_instance().initialize()  # Initialize the HTTP client for such requests.

    # * NodeRoles.MASTER requires special handling for initial instance.
    if parsed_args.prefer_role == NodeRoles.MASTER.name:
        master_user_count_stmt = select([func.count()]).where(
            users.c.type == NodeRoles.MASTER.name
        )  ## Check first if there are no entries for the master node account.

        count = await database_instance.fetch_val(master_user_count_stmt)

        # * If None, we should technically initialize the email service for the self-account registration.
        if not count:
            await get_email_instance().connect(is_immediate=True)
    else:
        # TODO: Insert HTTP request through here of looking for the master node. With that, save that from the env file later on.
        pass
        # create_task(get_http_client_instance().enqueue_request())

    create_task(post_initialize())

    # TODO: Post-Feature (Low-Priority) | Should check for the file of the JSON if still the same as before via database with the use of stored and computed hash.


async def post_initialize() -> None:
    """
    - An extension of the initialize() startup function without blocking the instance of uvicorn.

    - By continously awaiting tasks from tbe initialize() function, we can't do anything unless we left out of it or do asyncio.create_task() to get out-of-scope with initialize().

    - Tasks moved from the initialize() function may adjust to concurrently run the instance while doing other several checks.
    """

    await authenticate_node_client(
        role=NodeRoles(parsed_args.prefer_role),
        instances=(parsed_args, database_instance),
    )

    if (  ## Ensure that the email services were activated.
        parsed_args.prefer_role == NodeRoles.MASTER.name
        and not get_email_instance().is_connected
    ):
        create_task(get_email_instance().connect())

        await look_for_nodes(
            role=parsed_args.prefer_role, host=parsed_args.host, port=parsed_args.port
        )

    # * In the end, both NodeRoles.MASTER and NodeRoles.SIDE will initialize their local or universal (depending on the role) blockchain file.
    create_task(
        get_blockchain_instance(role=NodeRoles(parsed_args.prefer_role)).initialize()
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
    if parsed_args.prefer_role == NodeRoles.MASTER.name:
        get_email_instance().close()  # * Shutdown email service instance.
        # Remove the token related to this master.
        token_to_invalidate_stmt = (
            tokens.update()
            .where(tokens.c.token == get_identity_tokens()[1])
            .values(state=TokenStatus.LOGGED_OUT)
        )

        await database_instance.execute(token_to_invalidate_stmt)
        logger.info(f"Master Node's token has been invalidated due to Logout session.")
    else:
        await get_http_client_instance().enqueue_request(
            url=URLAddress(
                f"http://{parsed_args.host}:{parsed_args.port}/entity/logout"
            ),
            method=HTTPQueueMethods.POST,
            headers={"X-Token": JWTToken(get_identity_tokens()[1])},
        )

    await get_http_client_instance().close()  # * Shutdown the HTTP client module.
    await get_blockchain_instance().close()  # * Shutdown the blockchain instance.
    await database_instance.disconnect()  # * Shutdown the database instance.

    await close_resources(
        key=parsed_args.key_file[0]
    )  # * When necessary services finished, close the resource to go back from their malformed structure.

    logger.info("Wait for 3 seconds to ensure that all processes closed down...")
    await sleep(3)


"""
# Repeated Tasks
-These are the tasks that needs to be executed at certain amount of time to evaluate the blockchain consensus mechanism. Sooner or later,

TODO: Consensus Method (Remember, that we need the consensus dependency or something.)
"""

if parsed_args.prefer_role == NodeRoles.MASTER.name:
    logger.debug(f"Several functions for the {NodeRoles.MASTER} were imported.")

    @api_handler.on_event("startup")
    @repeat_every(seconds=120, wait_first=True)
    async def jwt_invalidation() -> None:

        ## Query available tokens.
        token_query = tokens.select().where(tokens.c.state != TokenStatus.EXPIRED)
        tokens_available = await database_instance.fetch_all(token_query)

        if not tokens_available:
            logger.warning("There are no tokens available to iterate as of the moment.")

        current_datetime: datetime = datetime.now()

        for each_tokens in tokens_available:
            token = Tokens.parse_obj(each_tokens)

            logger.debug(
                f"@ Token {token.id} | JWT Invalidation Condition (of {current_datetime.isoformat()} vs. {token.expiration.isoformat()}) | '(Should be) >' {current_datetime > token.expiration} | '(Should be) ==' {current_datetime == token.expiration} | `<' {current_datetime < token.expiration}"
            )

            if current_datetime >= token.expiration:
                token_to_del = (
                    tokens.update()
                    .where(tokens.c.expiration == token.expiration)
                    .values(state=TokenStatus.EXPIRED)
                )  ## Change the state of the token when past through expiration.

                await database_instance.execute(token_to_del)

                logger.info(
                    f"Token {token.token[:25]}(...) has been deleted due to expiration date {token.expiration}."
                )  ## Character beyond 25th will be truncated. This is just a pure random though.


# * We cannot encapsulate the whole (main.py) module as there's a subprocess usage wherein there's a custom __main__ that will run this script. Doing so may cause recursion.
if __name__ == "__main__":
    uvicorn.run(
        app=ASGI_APP_TARGET,
        host=parsed_args.host,
        port=parsed_args.port,
        reload=parsed_args.local,
        log_config=logger_config,
        log_level=LoggerLevelCoverage(parsed_args.log_level).value.lower(),
    )
