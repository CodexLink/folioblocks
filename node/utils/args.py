
"""
Argument Handler (args.py) | for the Blockchain Node and Explorer API Component Handler (main.py)

This handler (module) helps the entrypoint code to manage the given arguments. This retricts of what can be passed and what cannot. To use this, simply import it to the entrypoint code as this should not be used as a main module (See first line of code in condition.)

This file is part of Folioblocks.

Folioblocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Folioblocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Folioblocks. If not, see <https://www.gnu.org/licenses/>.
"""

if __name__ == "__main__":
    raise SystemExit(f"This {__file__} (module) should not be executed as an entrypoint code! It only contains handling for the arguments when the '__main__' module is launched.")

from argparse import ArgumentParser # TODO: To be moved later. This will be used for the options that we have. We create an on_event("startup") and create a dependency where we check if we wanted to be side node or master node. But still the checking is still needed for it to work properoly. Also, therefore, ArgParse > Evaluation of Endpoint to Launch > SQL > Node Role Check > [...].
from utils.constants import FOLIOBLOCKS_NODE_TITLE, FOLIOBLOCKS_NODE_DESCRIPTION, FOLIOBLOCKS_EPILOG, FOLIOBLOCKS_HELP, NODE_ROLE_CHOICES

args_handler = ArgumentParser(
    prog=FOLIOBLOCKS_NODE_TITLE,
    description=FOLIOBLOCKS_NODE_DESCRIPTION,
    epilog=FOLIOBLOCKS_EPILOG
)

args_handler.add_argument(
    "-nl",
    "--no-logs",
    action="store_false",
    help=FOLIOBLOCKS_HELP["NO_LOG_FILE"],
    required=False
)

args_handler.add_argument(
    "-pr",
    "--prefer-role",
    choices=NODE_ROLE_CHOICES,
    help=FOLIOBLOCKS_HELP["PREFER_ROLE"],
    required=True
)

args_handler.add_argument(
    "-p",
    "--port",
    action="store",
    help=FOLIOBLOCKS_HELP["PORT"],
    type=int,
    required=False
)

