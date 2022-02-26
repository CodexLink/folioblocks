"""
Utility Functions for File Operations

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""


from logging import Logger, getLogger
from os import _exit
from typing import Callable

import aiofiles
from cryptography.fernet import Fernet, InvalidToken

from utils.constants import ASYNC_TARGET_LOOP, CryptFileAction, KeyContext
from utils.exceptions import NoKeySupplied, UnsatisfiedClassType

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

# ! I cannot resolve this one as of now.
def assert_instance(f: Callable) -> Callable:
    def deco(*args: list[str]) -> Callable:  # TODO
        # Assert 'to' have CryptFileAction. I prefer isinstance instead of enum.Enum.__members__.

        if not isinstance(args[2], CryptFileAction):  # Can be better.
            raise UnsatisfiedClassType(args[2], CryptFileAction)

        return f(*args)

    return deco


@assert_instance
def crypt_file(
    filename: str,
    key: KeyContext | None,
    process: CryptFileAction,
    return_new_key: bool = False,
) -> bytes | None:
    """
    A Non-async function that processes a file with `to` under `filename` that uses `key` for decrypt and encrypt processes. This function exists for providing anti-redundancy over calls for preparing the files that has to be initialized for the session. This function is not compatible during async process, please refer to the acrypt_file for the implementation of async version.
    """

    file_content: bytes = b""
    processed_content: bytes = b""

    # Open the file first.
    with open(filename, "rb") as content_buffer:
        file_content = content_buffer.read()

    try:
        logger.info(
            f"{'Decrypting' if process is CryptFileAction.TO_DECRYPT else 'Encrypting'} a context..."
        )
        if process is CryptFileAction.TO_DECRYPT:

            if key is None:
                raise NoKeySupplied(crypt_file, "Decryption doesn't have a key.")

            crypt_context: Fernet = Fernet(key.encode("utf-8"))

        else:
            if key is None:
                key = Fernet.generate_key()
            crypt_context = Fernet(key)

        processed_content = getattr(
            crypt_context,
            "decrypt" if process is CryptFileAction.TO_DECRYPT else "encrypt",
        )(file_content)

        # Then write to the file for the final effect.
        with open(filename, "wb") as content_buffer:
            content_buffer.write(processed_content)

        logger.info(
            f"Successfully {'decrypted' if process is CryptFileAction.TO_DECRYPT else 'encrypted'} a context."
        )

        if return_new_key:
            return key

    except InvalidToken:
        logger.critical(
            f"{'Decryption' if process is CryptFileAction.TO_DECRYPT else 'Encryption'} failed. Please check your argument and try again. This may be a developer's problem, please report the issue at the repository (CodexLink/folioblocks)."
        )
        _exit(1)


@assert_instance
async def acrypt_file(
    afilename: str,
    akey: KeyContext | None,
    aprocess: CryptFileAction,
    return_new_key: bool = False,
) -> bytes | None:
    """
    An async version of the crypt_file method (declared on top). This function exists for preventing the async loop from getting blocked on CPU-bound instructions. This function will use aiofiles instead of conventional open() method for writing and reading files. Please refer to the crypt_file() for more information about the context of this function.

    """
    afile_content: bytes = b""
    aprocessed_content: bytes = b""

    # Open the file first.
    async with aiofiles.open(afilename, "rb") as acontent_buffer:
        afile_content = await acontent_buffer.read()

    try:
        logger.info(
            f"Async: {'Decrypting' if aprocess is CryptFileAction.TO_DECRYPT else 'Encrypting'} a context..."
        )
        if aprocess.TO_DECRYPT:

            if akey is None:
                raise NoKeySupplied(
                    acrypt_file, "Async: Decryption doesn't have a key."
                )

            acrypt_context: Fernet = Fernet(akey.encode("utf-8"))

        else:
            if akey is None:
                akey = Fernet.generate_key()
            acrypt_context = Fernet(akey)

        aprocessed_content = getattr(
            acrypt_context,
            "decrypt" if aprocess is CryptFileAction.TO_DECRYPT else "encrypt",
        )(afile_content)

        # Then write to the file for the final effect.
        async with aiofiles.open(afilename, "wb") as content_buffer:
            await content_buffer.write(aprocessed_content)

        logger.info(
            f"Async: Successfully {'decrypted' if aprocess is CryptFileAction.TO_DECRYPT else 'encrypted'} a context."
        )

        if return_new_key:
            return akey

    except InvalidToken:
        logger.critical(
            f"Async: {'Decryption' if aprocess is CryptFileAction.TO_DECRYPT else 'Encryption'} failed. Please check your argument and try again. This may be a developer's problem, please report the issue at the repository (CodexLink/folioblocks)."
        )
        _exit(1)
