"""
API — Entrypoint for the Blockchain Node and Explorer API Components.
Each API category has been seperated to ease the preparation phase, since there are two types of nodes that will play the part of the blockchain network.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

# Libraries
from argparse import Namespace
import logging
from logging.config import dictConfig
from databases import Database
import uvicorn
from fastapi import FastAPI

# Components
from api.endpoints.dashboard import dashboard_router
from api.endpoints.explorer import explorer_router
from api.endpoints.node import node_router
from database.core import close_db
from utils.logger import LoggerHandler
from utils.args import args_handler as ArgsHandler
from utils.constants import ASYNC_TARGET_LOOP, NODE_IP_PORT_FLOOR, NodeRoles
from fastapi_utils.tasks import repeat_every
from database.core import init_db


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
)  # This only returns the logging_config that is loaded from the uvicorn instance.

# * Load the logger even when async scope is not yet initialized.
# ! Note that, uvicorn will override this as the main thread is focused on the async loop!
dictConfig(logger_config)

logger: logging.Logger = logging.getLogger(ASYNC_TARGET_LOOP)
database: Database = init_db(__name__, parsed_args.key)


"""
# # API Router Setup

Several roles prohibits the use of other functionalities that is designed for the master nodes.

"""
api_handler: FastAPI = FastAPI(debug=parsed_args.debug)

if parsed_args.prefer_role is not NodeRoles.SIDE:
    api_handler.include_router(dashboard_router)
    api_handler.include_router(explorer_router)

api_handler.include_router(node_router)


# * Event Functions | I cannot find or hack a method that can run on the top-level from the low-level.
# * They specify that I cannot do that.


@api_handler.on_event("startup")
async def initialize() -> None:

    logger.info("Step 1 | Connecting to database...")
    # await core.db_instance.connect()

    # Should check for the credentials.
    # Should contain the node lookup.
    # Should check for the database. Create if it doesn't exists.
    # Ensure permissions of the file. Also note, that on shutdown it should be protected.

    # ! NOTE: The idea for the available nodes is dangerous. But this is just the setbacks. Just use SSL for HTTPS.

    # Should check for the file of the JSON if still the same as before via database. Or should hash or rehash the file. Also set the permission to undeletable, IF POSSIBLE.
    pass


@api_handler.on_event("shutdown")
async def terminate() -> None:

    logger.warn("Waiting for other processes to finish.")  # TODO.

    # ! Do other synchronous stuffs.
    close_db(parsed_args.key)


# A set of functions to run concurrently interval.
@api_handler.on_event("startup")
async def con_tasks() -> None:
    await test(), await test_a()


"""
Repeated Tasks
These are the tasks that needs to be executed at certain amount of time to evaluate the blockchain consensus mechanism. Sooner or later, we have to do something on this one.
TODO
- JWT Invalidation (Invalidate them if they did something or that node is inactive. This act will start when the JWT token is way past the deadline.)
- Consensus Method (Remember, that we need the consensus dependency.)
"""


@repeat_every(seconds=2)
async def test():
    logger.critical("From every internval seconds of 2.")


@repeat_every(seconds=5)
async def test_a():
    logger.warning("From every internval seconds of 5.")


# ! We cannot encapsulate the whole (main.py) module as there's a subprocess usage wherein there's a custom __main__ that will run this script. Doing so may cause recursion.
if __name__ == "__main__":
    uvicorn.run(
        "__main__:api_handler",
        host="localhost",
        port=NODE_IP_PORT_FLOOR,
        reload=parsed_args.local,
        log_config=logger_config,
        log_level=parsed_args.log_level.lower(),
    )
