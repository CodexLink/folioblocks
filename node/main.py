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
import uvicorn
from fastapi import FastAPI

# Components
from apis.dashboard import dashboard_router
from apis.explorer import explorer_router
from apis.node import node_router
from utils.args import args_handler as ArgsHandler
from utils.constants import NODE_IP_PORT_FLOOR, NODE_ROLE_CHOICES

parsed_args: Namespace = ArgsHandler.parse_args()
api: FastAPI = FastAPI()

if parsed_args.prefer_role != NODE_ROLE_CHOICES[0]:
    api.include_router(node_router)

else:
    api.include_router(node_router)
    api.include_router(dashboard_router)
    api.include_router(explorer_router)

# ! We cannot encapsulate the whole (main.py) module as there's a subprocess u sage where there's  custom __main__ that will run this script. Doing so may cause recursion.
if __name__ == "__main__":
    uvicorn.run(
        "__main__:api",
        host="localhost",
        port=NODE_IP_PORT_FLOOR,
        reload=parsed_args.local,
        workers=2,
        # log_level = ???
    )
