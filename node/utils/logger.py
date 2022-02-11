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
        f"This {__file__} is not designed for main / entrypoint purposes! It only invokes modified ogging properties to the entrypoint code."
    )

from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class CustomInjectLoggerConfig(BaseModel):
    DEFAULT_LOG_FORMAT: str = "%(levelprefix)s %(module)s:%(lineno)d (%(funcName)s) | %(asctime)s | %(message)s"
    ACCESS_LOG_FORMAT: str = '%(levelprefix)s (%(funcName)s) | %(asctime)s | Client %(client_addr)s requests "%(request_line)s" | Returned %(status_code)s'
    LOG_YEAR_FORMAT: str = "%H:%M:%S, %m-%d-%Y"


class LoggerHandler:
    @classmethod
    def init(
        cls,
        base_config: dict[str, Any],
        disable_file_logging: bool = False,
    ) -> dict[str, Any]:
        """
        A class method that modifies some of the properties of the uvicorn.config.LOGGING_CONFIG to allow colorized-output on the console while saving the output with the stripped colored in a log file.

        Args:
            base_config (dict[str, Any]): The dictionary that contains logging properties. It should contain uvicorn.config.LOGGING_CONFIG.
            disable_file_logging (bool, optional): Disables logging to the file. Defaults to False.

        Returns:
            dict[str, Any]: A modified base_config (uvicorn.logging.LOGGING_CONFIG)

        Note:
            The logging configuration by uvicorn seems to be hard to modify for a casual `logging module` enjoyer. I never knew it would take me 7-8 hours knowing where to configure and the amount of time of consideration of implementing features for my logger.

            The configuration right here is an inline file-based configuration. Inlined in a sense that I may be modifying the configuration by JSON but we are doing it inside of python instance. Note that I didn't use any python bindings or imports to comform with the typical configuration. The reason is that, since uvicorn accepts `log_config`, I might as well invoke / inject configuration so that when it was passed, it will be applied once and there will be no additional bs that I may encounter as it may emit unintended results.

            Please refer to the uvicorn logging configuration to understand how I override some of these attributes that is already configured. And please refer to the logging module as well for the formatting and other such.
        """

        _folder_handle = Path(f"{Path(__file__).cwd()}/logs")

        if not _folder_handle.exists():
            _folder_handle.mkdir(parents=True, exist_ok=False)

        _custom_config = (
            CustomInjectLoggerConfig().dict()
        )  # Load the pydantic dictionary of the custom variables.

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

        if not disable_file_logging:
            # ! Since loggers do not strip off terminal colors, we have to copy the same formatters
            # * add the variable of use_colors with a value of False.
            # * Create a variant.
            base_config["formatters"]["default_no_colors"] = base_config["formatters"][
                "default"
            ].copy()
            base_config["formatters"]["default_no_colors"]["use_colors"] = False

            # * Create a general file handler.
            base_config["handlers"]["file_logger"] = {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "when": "S",
                "interval": 30,
                "filename": f"{Path(__file__).cwd()}/logs/node_reserved.log",  # ! TODO: Add Node ID on this one when we implement the node system.
                "formatter": "default_no_colors",
            }

            # * For all loggers, set the general file handler as another handler (if there's one existing) or a new handler.
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
