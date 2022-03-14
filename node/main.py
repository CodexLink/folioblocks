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
    KeyContext,
    LoggerLevelCoverage,
    NodeRoles,
    RuntimeLoopContext,
    TokenStatus,
)
from core.dependencies import authenticate_node_client
from core.email import get_email_instance_or_initialize
from core.logger import LoggerHandler
from utils.processors import close_resources, initialize_resources_and_return_db_context

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
        RuntimeLoopContext(__name__),
        NodeRoles(parsed_args.prefer_role),
        parsed_args.key_file[0] if parsed_args.key_file is not None else None,
    ),
)

# * We need to delay this email instance, otherwise it will look for potentially non-existing .env file if this system was initially instantiated for the first time.
from core.blockchain import get_blockchain_instance_or_initialize

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
async def initialize() -> None:
    logger.warning(
        f"Step 0 (Argument Check) | Detected as {NodeRoles.MASTER.name if parsed_args.prefer_role == NodeRoles.MASTER.name else NodeRoles.SIDE.name} ..."
    )

    logger.info("Step 1 (Instance) | Connecting to local database ...")
    await database_instance.connect()
    logger.info("Step 1 (Instance) | Local database connected ...")

    if parsed_args.prefer_role == NodeRoles.MASTER.name:

        # If this was a master, check first if there are no entries for the master node account.
        master_user_count_stmt = select([func.count()]).where(
            users.c.type == NodeRoles.MASTER.name
        )

        count = await database_instance.fetch_val(master_user_count_stmt)

        # If none, we should technically initialize the email service for the self-account registration.
        if not count:
            logger.info("Step 1.2 | Immediately initialize email service...")
            await get_email_instance_or_initialize().connect()
            logger.info("Step 1.2 | Email service instantiated (by immediate).")

    # Should check for the credentials by checking through master node.

    # if

    # When log on, and its a node, store the credentials on the env only when it doesn't have an entry so that future authentications doesn't need it.

    # Also, send a code only when there's no master entry from the local SQL (FOR MASTER ONLY) via email and call it a day. This may also be done from the side node but im not sure yet. With the side node, create a unique api that emails the user to register.

    create_task(post_initialize())

    # ! NOTE: The idea for the available nodes is dangerous. But this is just the setbacks. Just use SSL for HTTPS.

    # TODO: Post-Feature (Low-Priority) | Should check for the file of the JSON if still the same as before via database with the use of stored and computed hash.


async def post_initialize() -> None:
    """
    This is basically an extension of the initialize() startup function  without blocking the instance of uvicorn.
    By continously awaiting tasks from tbe initialize() function, we can't do anything unless we left out of it or do asyncio.create_task() to get out-of-scope with initialize().

    Tasks moved from the initialize() function may adjust to concurrently to run the instance while doing other several checks.
    """
    logger.info("Attempting to authenticate ...")
    user_identity = await authenticate_node_client((parsed_args, database_instance))
    logger.info(f"Authenticated as {user_identity}.")

    # This part covers other initialization for both NodeRoles.MASTER and NodeRoles.SIDE.
    logger.info(
        f"Step 2.1 | Attempting to look {'for the master node' if parsed_args.prefer_role == NodeRoles.MASTER.name else 'at other nodes'} at host {parsed_args.host}, port {parsed_args.port}..."
    )

    if (
        parsed_args.prefer_role == NodeRoles.MASTER.name
        and not get_email_instance_or_initialize().is_connected
    ):
        logger.info("Step 2.2 | Initializing email service...")
        create_task(get_email_instance_or_initialize().connect())
        logger.info("Step 2.2 | Email service instantiated.")

        # TODO: look_for_nodes() function has been deleted.
        # await look_for_nodes()
        logger.info("Step 2.1 | Able to look for other nodes ...")

    # In the end, both NodeRoles.MASTER and NodeRoles.SIDE will initialize their local or universal (depending on the role) blockchain file.
    # Note that there are several steps that differentiates the two roles.

    logger.info("Step 3 | Initializing blockchain instance...")
    await get_blockchain_instance_or_initialize(  # type: ignore # Refer to the constructor on why I ignore this as of now.
        NodeRoles(parsed_args.prefer_role)
    ).initialize()

    # We also need to check for other parts if this instance has any other task to send with the master node. Otherwise, have to resolve that before we able to send some data.
    logger.info(
        "Step 3.2 | Attempting to sync to the blockchain state from the master node ...."
    )


@api_handler.on_event("shutdown")
async def terminate() -> None:
    """
    TODO:
        - Shutdown SQL Session (DONE)
        - Remove or finish any request or finish the consensus.
        - Put all other JWT on expiration or on blacklist if this was a master, or request logout if SIDE.
        - We may do the asyncio.gather sooner or later.
    """

    await get_blockchain_instance_or_initialize().close()  # type: ignore
    get_email_instance_or_initialize().close()
    await close_resources(parsed_args.key_file[0])

    await database_instance.disconnect()

    # TODO: Create an http.py that can be used across for the request.

    if parsed_args.prefer_role is NodeRoles.SIDE.name:
        pass

    logger.info("Wait for 3 to ensure that all processes were closed down...")
    await sleep(3)


"""
Repeated Taskswe have to do something on this one.
These are the tasks that needs to be executed at certain amount of time to evaluate the blockchain consensus mechanism. Sooner or later,
- Consensus Method (Remember, that we need the consensus dependency.)
"""

# TODO: We need to seperate some of the repeated actions based on their role.

if parsed_args.prefer_role == NodeRoles.MASTER.name:
    logger.debug(f"Several functions for the {NodeRoles.MASTER} were imported.")

    @api_handler.on_event("startup")
    @repeat_every(seconds=120, wait_first=True)
    async def jwt_invalidation() -> None:

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
                # Instead of deletion, change the state instead.
                token_to_del = (
                    tokens.update()
                    .where(tokens.c.expiration == token.expiration)
                    .values(state=TokenStatus.EXPIRED)
                )

                await database_instance.fetch_one(token_to_del)

                # Character beyond 25th will be truncated. This is just a pure random though.
                logger.info(
                    f"Token {token.token[:25]}(...) has been deleted due to expiration date {token.expiration}."
                )


@repeat_every(seconds=10)  # unconfirmed.
async def consensus_with_side_nodes() -> None:
    # TODO Understand that we need to run this either in the Class Context or in this context and invoke a particular async function to call from the get_blockchain_instance_or_initialize() or whatever.
    # This function should be compatible for both side and master.
    pass


# ! We cannot encapsulate the whole (main.py) module as there's a subprocess usage wherein there's a custom __main__ that will run this script. Doing so may cause recursion.
if __name__ == "__main__":
    uvicorn.run(
        app=ASGI_APP_TARGET,
        host=parsed_args.host,
        port=parsed_args.port,
        reload=parsed_args.local,
        log_config=logger_config,
        log_level=LoggerLevelCoverage(parsed_args.log_level).value.lower(),
    )
