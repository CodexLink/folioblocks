"""
Context Validators (validators.py) | For several functions that require validity without disrupting the context of a certain file.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from utils.constants import ASYNC_TARGET_LOOP, KeyContext, FERNET_KEY_LENGTH
from pathlib import Path

from logging import getLogger


def validate_key(context: KeyContext | None) -> KeyContext | None:
    file_ref = f"{Path(__file__).cwd()}/{context}"

    # Validate if the given context is a path first.
    if Path(file_ref).is_file():
        from dotenv import find_dotenv, load_dotenv
        from os import environ as env

        load_dotenv(find_dotenv(filename=file_ref))

        key: str | None = env.get("AUTH_KEY", None)
        if key is not None:
            return key

        raise Exception("Error: The key supplied is invalid.")

    # We are sure that this may be the key.
    elif context is not None and context.__len__() == FERNET_KEY_LENGTH:
        return context

    elif context is not None and context.__len__() != FERNET_KEY_LENGTH:
        exit(
            "Error: Supplied value for the key is not a valid key or a filename containing a key.",
        )

    else:
        return None
