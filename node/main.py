"""
API — Entrypoint for the Blockchain Node and Explorer API Components.

Each API category has been seperated to ease the preparation phase, since there are two types of nodes that will play the part of the blockchain network.

This file is part of Folioblocks.

Folioblocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Folioblocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Folioblocks. If not, see <https://www.gnu.org/licenses/>.
"""

import uvicorn
from utils.constants import NODE_IP_PORT_FLOOR
from utils.args import args_handler
from fastapi import FastAPI, include_router

def prepare():
    node = FastAPI()
    node.include_router() # Add the imports here.


# Entrypoint Code
if __name__ == "__main__":
    args_handler.parse_args() # Check for the passed parameter first.

    # TODO: Add the API Router or combine them later.
    # uvicorn.run(instance, host="localhost", port=NODE_IP_PORT_FLOOR) # TODO: log_level = .

