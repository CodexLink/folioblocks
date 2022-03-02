"""
Utility Functions for the Database

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Any, Callable

from databases import Database
from passlib.context import CryptContext

from utils.constants import HashedData, RawData, UserType

pwd_handler = CryptContext(schemes=["bcrypt"])
db_instance: Database

# Initialize.


def hash_user_password(pwd: RawData) -> HashedData:
    return pwd_handler.hash(pwd)


def verify_user_hash(real_pwd: RawData, hashed_pwd: HashedData) -> bool:
    return pwd_handler.verify(real_pwd, hashed_pwd)


def store_db_instance(instance: Database) -> None:
    global db_instance
    db_instance = instance


def get_db_instance() -> Database:
    global db_instance
    return db_instance


def get_db(fn: Callable) -> Callable:
    global db_instance
    # db_instance: Database = get_db_instance()  # This is incomplete.

    def decorator(*args: list[Any], **kwargs: dict[Any, Any]) -> Database:
        return fn(*args, **kwargs)

    return decorator


@get_db
def ensure_authorized(
    role: UserType, id: int | None = None  # TODO.
) -> None:  # Use session ID for authentication.

    if role is UserType.AS_ADMIN:
        pass

    elif role is UserType.AS_NODE:
        pass

    else:
        pass

    return

    print("This ensures that the person is authorized.")
    # Ensure that someone that access this should be under the role of ... and should be authorized to its local.


@get_db
def ensure_past_negotiations() -> bool:
    # Maybe query or use the current session or the Node ID.
    # We need to contact the other part to ensure that there is negotiations.
    return False


# TODO: Verify custom key of something.
