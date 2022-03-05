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
from datetime import datetime
from logging.config import dictConfig

import uvicorn
from databases import Database
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from api.admin import admin_router
from api.dashboard import dashboard_router
from api.entity import entity_router
from api.explorer import explorer_router
from api.node import node_router
from blueprint.models import tokens
from blueprint.schemas import Tokens
from core.args import args_handler as ArgsHandler
from core.constants import (
    ASGI_APP_TARGET,
    ASYNC_TARGET_LOOP,
    LoggerLevelCoverage,
    NodeRoles,
    TokenType,
)
from core.logger import LoggerHandler
from utils.processors import close_resources, initialize_resources

"""
# # Startup Functions

* A set of commands that runs before the fastpi.on_event("<events>").

They are required to be instantiated outside of the async context due to the
implementation not being a class-based. I don't want to have a bad time.

"""
parsed_args: Namespace = ArgsHandler.parse_args()
logger_config = LoggerHandler.init(
    base_config=uvicorn.config.LOGGING_CONFIG,
    disable_file_logging=parsed_args.no_log_file,
    logger_level=LoggerLevelCoverage(parsed_args.log_level),
)  # This only returns the logging_config that is loaded from the uvicorn instance.

# * Load the logger even when async scope is not yet initialized.
# ! Note that, uvicorn will override this as the main thread is focused on the async loop!
dictConfig(logger_config)

logger: logging.Logger = logging.getLogger(ASYNC_TARGET_LOOP)
database: Database = initialize_resources(
    __name__, parsed_args.keys[0] if parsed_args.keys is not None else None
)

"""
# # API Router Setup and Initialization

Several roles prohibits the use of other functionalities that is designed for the master nodes.

About design:
FastAPI doesn't seem to support class-based views by nature. Even when fastapi-utils provides that capability, I dont trust its functionality anymore due to the nature of FastAPI being too far than fastapi-utils can keep up.
Meaning, that tool may be outdated. Hacking it like what I did in `CodexLink/discord-activity-badge` would take
my time more than making other features, which I still haven't done.

"""
api_handler: FastAPI = FastAPI()

api_handler.include_router(entity_router)  # # WARNING REGARDING SIDE NODE.
api_handler.include_router(node_router)

if parsed_args.prefer_role is not NodeRoles.SIDE:
    api_handler.include_router(admin_router)
    api_handler.include_router(dashboard_router)
    api_handler.include_router(explorer_router)

# * Event Functions.
@api_handler.on_event("startup")
async def initialize() -> None:

    logger.info("Step 1 | Connecting to local database...")
    await database.connect()
    logger.info("Step 1 | Local database connected...")

    # Should check for the credentials by checking through master node.

    logger.info("Step 2 | Authenticating...")
    # Do something here.
    logger.info("Authenticated...")  # Require...

    if parsed_args.prefer_role is NodeRoles.MASTER:
        # Authenticate by local first.
        # Should do the node lookup.
        logger.info("Step 3 | Detected as MASTER Node, looking for node lookup.")
        # TODO: look_for_nodes() function has been deleted.
        logger.info(
            f"Attempting to look at other nodes at Port {parsed_args.port} (inside {parsed_args.host})..."
        )

        logger.info("Step 4 | Initializing Email Service...")

        logger.info("Step 4 | Email service instantiated.")

    else:  # Asserts SIDE.
        pass

    # ! NOTE: The idea for the available nodes is dangerous. But this is just the setbacks. Just use SSL for HTTPS.
    # Should check for the file of the JSON if still the same as before via database. Or should hash or rehash the file. Also set the permission to undeletable, IF POSSIBLE.


@api_handler.on_event("shutdown")
async def terminate() -> None:
    """
    TODO:
        - Shutdown SQL Session (DONE???)
        - Remove or finish any request or finish the consensus.
        - Put all other JWT on expiration or on blacklist.
        - We may do the asyncio.gather sooner or later.
    """

    await close_resources(parsed_args.keys[0])


# A set of functions to run concurrently interval.
# ! TO BE REMOVED LATER.
# @api_handler.on_event("startup")
# async def con_tasks() -> None:
#     pass


"""
Repeated Taskswe have to do something on this one.
These are the tasks that needs to be executed at certain amount of time to evaluate the blockchain consensus mechanism. Sooner or later,
TODO
- JWT Invalidation (Invalidate them if they did something or that node is inactive. This act will start when the JWT token is way past the deadline.)
- Consensus Method (Remember, that we need the consensus dependency.)
"""


@api_handler.on_event("startup")
@repeat_every(seconds=120, wait_first=True)
async def jwt_invalidation() -> None:

    token_query = tokens.select().where(tokens.c.state != TokenType.EXPIRED)
    tokens_available = await database.fetch_all(token_query)

    if not tokens_available:
        logger.warning("There are no tokens available to iterate as of the moment.")

    current_datetime: datetime = datetime.now()

    for each_tokens in tokens_available:
        token = Tokens.parse_obj(each_tokens)

        logger.debug(
            f"@ Token {token.id} | JWT Invalidation Condition | '(Should be) >' {current_datetime > token.expiration} | '(Should be) ==' {current_datetime == token.expiration} | `<' {current_datetime < token.expiration}"
        )

        if current_datetime >= token.expiration:
            token_to_del = tokens.delete().where(
                tokens.c.expiration == token.expiration
            )

            await database.execute(token_to_del)

            # Character beyond 25th will be truncated. This is just a pure random though.
            logger.info(
                f"Token {token.token[:25]}(...) has been deleted due to expiration date {token.expiration}."
            )


@repeat_every(seconds=10)  # unconfirmed.
async def consensus_with_side_nodes() -> None:
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
