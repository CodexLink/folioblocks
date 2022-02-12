"""
SQLite ORM-able Database for the Node Backend API (database.py)

TODO:

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the gnu general public license as published by the free software foundation, either version 3 of the license, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. see the gnu general public license for more details.
you should have received a copy of the gnu general public license along with FolioBlocks. if not, see <https://www.gnu.org/licenses/>.
"""

from typing import Final
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import databases

# To be moved later.
DBPath: str

DATABASE_NAME: Final[str] = "folioblocks-node.db"
DATABASE_URL: DBPath = f"sqlite:///{Path(__file__).cwd()}/{DATABASE_NAME}"

db_instance = databases.Database(DATABASE_URL)
