"""
API — Entrypoint for the Blockchain Node and Explorer API Components.
Each API category has been seperated to ease the preparation phase, since there are two types of nodes that will play the part of the blockchain network.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

if __name__ != "__main__":
    raise SystemExit(
        "You cannot make this module as a submodule! This module contains all necessary functions for the startup of the system."
    )

# Libraries
import uvicorn
from fastapi import FastAPI

# Components
from node.utils.constants import NODE_IP_PORT_FLOOR
from utils.args import args_handler as ArgsHandler

# Routers, this will be inserted from the If and else in the ArgsHandler.
from apis.dashboard import dashboard_router
from apis.explorer import explorer_router
from apis.node import node_router

# Step 1: Handle the parameters first.
_parsed_args = ArgsHandler.parse_args()  # idk what type is this.
api = FastAPI()  # What should we depend on?
print(_parsed_args)

# api.include_router()

# TODO: Add the API Router or combine them later.
# uvicorn.run(instance, host="localhost", port=NODE_IP_PORT_FLOOR) # TODO: log_level = .
