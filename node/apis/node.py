"""
API — Explorer and Node API for the Master Node.

This file is part of Folioblocks.

Folioblocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Folioblocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Folioblocks. If not, see <https://www.gnu.org/licenses/>.
"""

# Libraries
from fastapi import Depends, FastAPI, Query, Router
from typing import Any, Dict, Final
from utils.constantsi import NodeAPITags
# from secrets import token_hex

node_router = APIRouter(
    prefix="/node",
    tags=["Node API"],
    responses= {404: {"description": "Not Found."}} # TODO: Handle more than Not Found.
)



@node.get(
    "/config",
    tags=[
    ]
):
async def fetch_node_config():
    pass

@node.post(
    "/register"
)
async def register_node():
    pass

@node.get(
    "/login"
)
async def login_node():
    pass

@node.get(
    "/info"
)
async def chain_info(): # Includes, time_estimates, mining_status, consensus.
    pass

@node.post(
    "/negotiate"
)
async def pre_post_negotiate(): # Actions should be, receive_block, send_hash_block (During this, one of the assert processes will be executed.)
    pass

@node.put(
    "/negotiate"
)
async def process_negotiate(): # Actions should be updating data for the master node to communicate.
    pass

