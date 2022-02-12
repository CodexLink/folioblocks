from argparse import Namespace
from fastapi import FastAPI
from typing import Any

parsed_args: Namespace
logger_config: Any
logger: Any
api_handler: FastAPI

async def system_checks() -> None: ...
async def test_logging() -> None: ...
