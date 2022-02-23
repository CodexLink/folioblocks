"""
Context Validators (validators.py) | For several functions that require validity without disrupting the context of a certain file.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from pathlib import Path

from utils.constants import FERNET_KEY_LENGTH, SECRET_KEY_LENGTH, KeyContext


def validate_file_keys(
    context: KeyContext | None,
) -> tuple[KeyContext, KeyContext] | None:
    file_ref = f"{Path(__file__).cwd()}/{context}"

    # Validate if the given context is a path first.
    if Path(file_ref).is_file():

        from os import environ as env

        from dotenv import find_dotenv, load_dotenv

        try:
            # Redundant, but ensure.
            load_dotenv(
                find_dotenv(filename=Path(file_ref), raise_error_if_not_found=True)
            )

        except OSError:
            exit(
                f"The file {file_ref} may not be a valid .env file or is missing. Please check your arguments or the file."
            )

        a_key: str | None = env.get("AUTH_KEY", None)
        s_key: str | None = env.get("SECRET_KEY", None)

        # Validate the AUTH_KEY and SECRET_KEY.
        if (
            a_key is not None
            and a_key.__len__() == FERNET_KEY_LENGTH
            or s_key is not None
            and s_key.__len__() == SECRET_KEY_LENGTH
        ):

            return a_key, s_key

        else:
            exit(
                f"Error: One of the keys either has an invalid value or is missing. Have you modified your {file_ref}? Please check and try again."
            )

    else:
        return None
