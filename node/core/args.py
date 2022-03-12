"""
Argument Handler (args.py) | for the Blockchain Node and Explorer API Component Handler (main.py)
This handler (module) helps the entrypoint code to manage the given arguments. This retricts of what can be passed and what cannot. To use this, simply import it to the entrypoint code as this should not be used as a main module (See first line of code in condition.)

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

if __name__ == "__main__":
    raise SystemExit(
        f"This {__file__} (module) should not be executed as an entrypoint code! It only contains handling for the arguments when the '__main__' module is launched."
    )

from argparse import ArgumentParser
from re import Pattern, compile

from utils.processors import validate_file_keys

from core.constants import (  # TODO: To be moved later. This will be used for the options that we have. We create an on_event("startup") and create a dependency where we check if we wanted to be side node or master node. But still the checking is still needed for it to work properoly. Also, therefore, ArgParse > Evaluation of Endpoint to Launch > SQL > Node Role Check > [...].
    AUTH_ENV_FILE_NAME,
    ENUM_NAME_PATTERN,
    FOLIOBLOCKS_EPILOG,
    FOLIOBLOCKS_HELP,
    FOLIOBLOCKS_NODE_DESCRIPTION,
    FOLIOBLOCKS_NODE_TITLE,
    NODE_IP_ADDR_FLOOR,
    NODE_IP_PORT_FLOOR,
    ArgumentParameter,
    LoggerLevelCoverage,
    NodeRoles,
)

args_handler = ArgumentParser(
    prog=FOLIOBLOCKS_NODE_TITLE,
    description=FOLIOBLOCKS_NODE_DESCRIPTION,
    epilog=FOLIOBLOCKS_EPILOG,
)

# Before adding arguments, let's process and inject those IntEnums from the constants.py. We cannot use IntEnums legally because the author of argparse seems to be conflicted with the use case of the Enums.


# Prep the RegExpr.
compiled_pattern: Pattern[str] = compile(ENUM_NAME_PATTERN)
for each_enum in [LoggerLevelCoverage, NodeRoles]:
    temp_choice: list[str] = []
    re_matched: list[str] = compiled_pattern.findall(
        each_enum.__name__,
    )

    for each_value in each_enum:
        temp_choice.append(each_value.name)

    eval_enum_name: str = "".join([letters for letters in re_matched])
    locals()[f"_injected_{eval_enum_name.lower()}_choices"] = temp_choice


args_handler.add_argument(
    "-d",
    "--debug",
    action="store_true",
    help=FOLIOBLOCKS_HELP[ArgumentParameter("DEBUG")],
    required=False,
)

args_handler.add_argument(
    "-ho",
    "--host",
    default=NODE_IP_ADDR_FLOOR,
    help=FOLIOBLOCKS_HELP[ArgumentParameter("HOST")],
)

args_handler.add_argument(
    "-kf",
    "--key-file",
    action="store",
    default=AUTH_ENV_FILE_NAME,
    help=FOLIOBLOCKS_HELP[ArgumentParameter("KEY_FILE")],
    type=validate_file_keys,
)

args_handler.add_argument(
    "-l",
    "--local",
    action="store_true",
    help=FOLIOBLOCKS_HELP[ArgumentParameter("LOCAL")],
)

args_handler.add_argument(
    "-ll",
    "--log-level",
    choices=locals()["_injected_llc_choices"],
    help=FOLIOBLOCKS_HELP[ArgumentParameter("LOG_LEVEL")],
    default=LoggerLevelCoverage.INFO.value,
)

args_handler.add_argument(
    "-nlf",
    "--no-log-file",
    action="store_true",
    help=FOLIOBLOCKS_HELP[ArgumentParameter("NO_LOG_FILE")],
    required=False,
)

args_handler.add_argument(
    "-p",
    "--port",
    action="store",
    default=NODE_IP_PORT_FLOOR,
    help=FOLIOBLOCKS_HELP[ArgumentParameter("PORT")],
    type=int,
    required=False,
)

args_handler.add_argument(
    "-pr",
    "--prefer-role",
    choices=locals()["_injected_nr_choices"],
    help=FOLIOBLOCKS_HELP[ArgumentParameter("PREFER_ROLE")],
    required=True,
)
