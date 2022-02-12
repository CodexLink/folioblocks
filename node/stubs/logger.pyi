from pydantic import BaseModel
from typing import Any

class CustomInjectLoggerConfig(BaseModel):
    DEFAULT_LOG_FORMAT: str
    ACCESS_LOG_FORMAT: str
    LOG_YEAR_FORMAT: str

class LoggerHandler:
    @classmethod
    def init(cls, base_config: dict[str, Any], disable_file_logging: bool = ...) -> dict[str, Any]: ...
