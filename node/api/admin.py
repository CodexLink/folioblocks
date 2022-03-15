"""
Admin API — Exclusive endpoints for allowing actions that requires authorization from higher-ups to allow users for use of the platform.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""


"""
# Further Notice
This endpoint should be used for generating users as a organization or as a node. When running this endpoint, ensure that you look for

"""

from fastapi import APIRouter

from core.constants import BaseAPI

admin_router = APIRouter(
    prefix="/admin",
    tags=[BaseAPI.ADMIN.value],
)


@admin_router.post(
    "/generate_authority",
    # tags=[NodeAPI.GENERAL_NODE_API.value],
    # response_model=NodeRegisterCredentials,
    summary="Generates token for registration of user as node or as a normal user.",
    description="An exclusive API endpoint that generates token for users to register. This should be triggered by an admin.",
)

# ! Note that two functions seperating normal user and the node user will use this endpoint!
async def generate_auth_token(
    # credentials: NodeRegisterCredentials,
    # ) -> NodeRegisterResult:
) -> None:
    """
    Use admin address, date to add, role type.
    """
    return


# ! This may be inserted from the blockchain as a proof.
# # Not sure if we ever need the deletion function.
@admin_router.get(
    "generated_tokens/",
    # tags=[NodeAPI.GENERAL_NODE_API.value],
    # response_model=NodeRegisterCredentials,
    summary="Displays tokens that is unusued for registration.",
    description="An exclusive API endpoint that shows the currently unused generated token.",
)
async def check_unused_tokens() -> None:
    return
