from fastapi import FastAPI as FastAPI
from pydantic import BaseModel as BaseModel
from typing import Any, Final

DBPath: str
DATABASE_NAME: Final[str]
DATABASE_URL: DBPath
db_instance: Any
