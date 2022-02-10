"""
Logger — A customized logger that makes the uvicorn logger and the top-level logger co-exist from one another.
The logging for both may be seperate but their formatting should be consistent.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

if __name__ == "__main__":
    raise SystemExit(
        f"This {__file__} is not designed for main / entrypoint purposes! It only invokes logging capabilities to the entrypoint code."
    )

from pydantic import BaseModel
from typing import Any


class CustomInjectLoggerConfig(BaseModel):
    LOGGER_NAME: str = "folioblocks-node"
    DEFAULT_LOG_FORMAT: str = "%(levelprefix)s %(module)s:%(lineno)d (%(funcName)s) | %(asctime)s | %(message)s"
    ACCESS_LOG_FORMAT: str = '%(levelprefix)s (%(funcName)s) | %(asctime)s | Client %(client_addr)s requests "%(request_line)s" | Returned %(status_code)s'
    LOG_YEAR_FORMAT: str = "%H:%M:%S, %m-%d-%Y"


class LoggerHandler:
    @classmethod
    def init(
        cls,
        base_config: dict[str, Any],
        disable_logging: bool = False,
    ) -> dict[str, Any]:

        _custom_config = (
            CustomInjectLoggerConfig().dict()
        )  # Instantiate our variable configs.

        # * Modify the formatters' string format.
        base_config["formatters"]["access"]["fmt"] = _custom_config["ACCESS_LOG_FORMAT"]
        base_config["formatters"]["access"]["use_colors"] = True

        base_config["formatters"]["default"]["fmt"] = _custom_config[
            "DEFAULT_LOG_FORMAT"
        ]
        base_config["formatters"]["default"]["use_colors"] = True
        base_config["formatters"]["default"]["datefmt"] = _custom_config[
            "LOG_YEAR_FORMAT"
        ]

        if not disable_logging:
            # ! Since loggers do not strip off terminal colors, we have to copy the same formatters
            # * add the variable of use_colors with a value of False.

            # * Create variants.

            base_config["formatters"]["access_no_colors"] = base_config["formatters"][
                "access"
            ].copy()
            base_config["formatters"]["access_no_colors"]["use_colors"] = False

            base_config["formatters"]["default_no_colors"] = base_config["formatters"][
                "default"
            ].copy()
            base_config["formatters"]["default_no_colors"]["use_colors"] = False

            base_config["handlers"]["file_logger"] = {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "when": "midnight",
                "interval": 1,
                "filename": "../logs/node_logs.log",  # TODO: Observe and add datetime when necessary.
                "formatter": "default_no_colors",
            }

            for each_loggers in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
                if each_loggers == "uvicorn.error":
                    base_config["loggers"]["uvicorn.error"] = {
                        "handlers": ["file_logger"]
                    }
                else:
                    base_config["loggers"][each_loggers]["handlers"].append(
                        "file_logger"
                    )

        return base_config
