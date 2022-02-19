"""
SQLite ORM-able Database for the Node Backend API (database.py)

TODO:

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the gnu general public license as published by the free software foundation, either version 3 of the license, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. see the gnu general public license for more details.
you should have received a copy of the gnu general public license along with FolioBlocks. if not, see <https://www.gnu.org/licenses/>.
"""

if __name__ == "__main__":
    raise SystemExit(
        f"You cannot use the {__file__}as an entrypoint module! Please use the main module or import this module to the other modules."
    )

from databases import Database
from sqlalchemy import create_engine
from logging import getLogger
from utils.constants import ASYNC_TARGET_LOOP
from utils.constants import DATABASE_URL_PATH
from database.models import DeclarativeModel
from pathlib import Path

logger = getLogger(ASYNC_TARGET_LOOP)

sql_engine = create_engine(DATABASE_URL_PATH, connect_args={"check_same_thread": False})
logger.info(f"SQL Engine for the {DATABASE_URL_PATH} has been created.")


db_instance = Database(DATABASE_URL_PATH)
logger.info(f"Async database instance to {DATABASE_URL_PATH} has been instantiated.")


# TODO: Is the database existing? If not then create and then a new key as well.
