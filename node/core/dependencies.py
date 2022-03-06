"""
Dependencies (dependencies.py) | Contains a set of functions that is classified to run under fastapi.Depends and a sub-dependencies of `depends`.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from http import HTTPStatus

from blueprint.models import tokens, users
from blueprint.schemas import Tokens
from databases import Database
from fastapi import Depends, Header, HTTPException

from core.constants import JWTToken, UserEntity
from sqlalchemy import select

db_instance: Database


def store_db_instance(instance: Database) -> None:
    global db_instance
    db_instance = instance


def get_db_instance() -> Database:
    global db_instance
    return db_instance


# ! Note that we may need multiple roles on one argument. Explore the | flag soon.

# We can make this one as a decorator and use it from one of the functions that validates if the token or the user who holds it has a respective role.


class EnsureAuthorized:
    def __init__(self, _as: UserEntity | list[UserEntity]) -> None:
        self._as: UserEntity | list[UserEntity] = _as

    async def __call__(
        self, x_token: JWTToken = Header(...), db: Database = Depends(get_db_instance)
    ) -> None:

        if x_token:
            req_ref_token = tokens.select().where(tokens.c.token == x_token)

            ref_token = Tokens.parse_obj(await db.fetch_one(req_ref_token))

            if ref_token:

                # ! I didn't use the Metadata().select() because its parameter whereclause blocks selective column to return.
                # * Therefore use the general purpose sqlalchemy.select instead.
                user_role_ref = select([users.c.user_type]).where(
                    users.c.unique_address == ref_token.from_user
                )

                user_role = await db.fetch_val(user_role_ref)

                if isinstance(self._as, list):
                    for each_role in self._as:
                        if user_role is not each_role:
                            continue
                        return
                else:
                    if user_role is self._as:
                        return

        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="You are unauthorized to access this endpoint. Please login first.",
        )


def ensure_past_negotiations() -> bool:
    # Maybe query or use the current session or the Node ID.
    # We need to contact the other part to ensure that there is negotiations.
    return False


# TODO: Verify custom key of something.
