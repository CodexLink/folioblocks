"""
Dependencies (dependencies.py) | Contains a set of functions that is classified to run under fastapi.Depends and a sub-dependencies of `depends`.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from databases import Database
from core.constants import UserEntity, JWTToken
from fastapi import Header, Depends, HTTPException
from http import HTTPStatus
from blueprint.models import tokens
from blueprint.schemas import Tokens
from blueprint.models import users

db_instance: Database


def store_db_instance(instance: Database) -> None:
    global db_instance
    db_instance = instance


def get_db_instance() -> Database:
    global db_instance
    return db_instance


# ! Note that we may need multiple roles on one argument. Explore the | flag soon.

# We can make this one as a decorator and use it from one of the functions that validates if the token or the user who holds it has a respective role.

# * Cl
# async def ensure_authorized_as_admin

# async def ensure_authorized_as_node

# async def ensure_authorized


async def ensure_authorized(
    # role: UserEntity | None = None,
    x_token: JWTToken = Header(...),
    db: Database = Depends(get_db_instance),
) -> None:

    # print(role)

    if x_token:
        req_ref_token = tokens.select().where(tokens.c.token == x_token)
        ref_token = Tokens.parse_obj(await db.fetch_one(req_ref_token))

        if ref_token:
            user_ref = users.select().where(
                users.c.unique_address == ref_token.from_user
            )
            user = await db.fetch_one(user_ref)

            if user:
                return

    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="You are unauthorized to access this endpoint. Please login first.",
    )

    # Ensure that someone that access this should be under the role of ... and should be authorized to its local.


def ensure_past_negotiations() -> bool:
    # Maybe query or use the current session or the Node ID.
    # We need to contact the other part to ensure that there is negotiations.
    return False


# TODO: Verify custom key of something.
