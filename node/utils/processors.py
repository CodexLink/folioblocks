"""
Processor Functions (processors.py) | Set of functions that processes a particular object / entity / elements, whatever you call it.

These functions varies from handling file resources and contents of a variable.
Please note that there are no distinctions / categorization (exception for alphabetical) available for each functions, read their description to understand their uses.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from getpass import getpass
from json import dump as json_export
from logging import Logger, getLogger
from os import _exit
from pathlib import Path
from secrets import token_hex
from sqlite3 import Connection, OperationalError, connect
from typing import Any

import aiofiles
from aioconsole import ainput
from blueprint.models import model_metadata
from blueprint.schemas import Block
from core.constants import (
    ASYNC_TARGET_LOOP,
    AUTH_ENV_FILE_NAME,
    BLOCKCHAIN_NAME,
    BLOCKCHAIN_RAW_PATH,
    DATABASE_NAME,
    DATABASE_RAW_PATH,
    DATABASE_URL_PATH,
    FERNET_KEY_LENGTH,
    SECRET_KEY_LENGTH,
    CredentialContext,
    CryptFileAction,
    HashedData,
    IPAddress,
    IPPort,
    KeyContext,
    NodeRoles,
    RawData,
    RuntimeLoopContext,
)
from core.dependencies import store_db_instance
from cryptography.fernet import Fernet, InvalidToken
from databases import Database
from passlib.context import CryptContext
from sqlalchemy import create_engine

from utils.exceptions import NoKeySupplied, UnsatisfiedClassType

logger: Logger = getLogger(ASYNC_TARGET_LOOP)
pwd_handler: CryptContext = CryptContext(schemes=["bcrypt"])

# # File Handlers, Cryptography — START
async def acrypt_file(
    *,
    afilename: str,
    akey: KeyContext,
    aprocess: CryptFileAction,
    return_new_key: bool = False,
) -> bytes | None:
    """
    An async version of the crypt_file method (declared on top). This function exists for preventing the async loop from getting blocked on CPU-bound instructions. This function will use aiofiles instead of conventional open() method for writing and reading files. Please refer to the crypt_file() for more information about the context of this function.

    """

    if not isinstance(aprocess, CryptFileAction):
        raise UnsatisfiedClassType(aprocess, CryptFileAction)

    afile_content: bytes = b""
    aprocessed_content: bytes = b""

    # Open the file first.
    async with aiofiles.open(afilename, "rb") as acontent_buffer:
        afile_content = await acontent_buffer.read()

    try:
        logger.debug(
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

        logger.debug(
            f"Async: Successfully {'decrypted' if aprocess is CryptFileAction.TO_DECRYPT else 'encrypted'} a context."
        )

        if return_new_key:
            return akey

    except InvalidToken:
        logger.critical(
            f"Async: {'Decryption' if aprocess is CryptFileAction.TO_DECRYPT else 'Encryption'} failed. Please check your argument and try again. This may be a developer's problem, please report the issue at the repository (CodexLink/folioblocks)."
        )
        _exit(1)


def crypt_file(
    *,
    filename: str,
    key: KeyContext | None,
    process: CryptFileAction,
    return_new_key: bool = False,
) -> bytes | None:
    """
    A Non-async function that processes a file with `to` under `filename` that uses `key` for decrypt and encrypt processes. This function exists for providing anti-redundancy over calls for preparing the files that has to be initialized for the session. This function is not compatible during async process, please refer to the acrypt_file for the implementation of async version.
    """

    if not isinstance(process, CryptFileAction):
        raise UnsatisfiedClassType(process, CryptFileAction)

    file_content: bytes = b""
    processed_content: bytes = b""
    crypt_context: Fernet | None = None

    # Open the file first.
    with open(filename, "rb") as content_buffer:
        file_content = content_buffer.read()

    try:
        logger.debug(
            f"{'Decrypting' if process is CryptFileAction.TO_DECRYPT else 'Encrypting'} a context..."
        )
        if process is CryptFileAction.TO_DECRYPT:

            if key is None:
                raise NoKeySupplied(crypt_file, "Decryption doesn't have a key.")

            if isinstance(key, str):
                crypt_context = Fernet(key.encode("utf-8"))

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

        if return_new_key and isinstance(key, bytes):
            return key

    except InvalidToken:
        logger.critical(
            f"{'Decryption' if process is CryptFileAction.TO_DECRYPT else 'Encryption'} failed. Please check your argument and try again. This may be a developer's problem, please report the issue at the repository (CodexLink/folioblocks)."
        )
        _exit(1)


# # File Handlers, Cryptography — END

# # File Resource Initializers and Validators, Blockchain and Database — START
async def initialize_resources_and_return_db_context(
    *,
    runtime: RuntimeLoopContext,
    role: NodeRoles,
    auth_key: KeyContext = None,
) -> Database:
    """
    A non-async initializer for both database and blockchain files.

    Intializes the file by decryption when async thread is not yet initialized.
    For new instance, generate a new file end encrypt them to return an ID that can be decrypt later.

    Args:
        runtime (RuntimeLoop): The runtime context, this is evaluated from __name__.
        keys (tuple[KeyContext, KeyContext] | None, optional): The value of the key that is parsed from the argparse library. Defaults to None.

    Returns:
        Database | None: Returns the context of the database for accessing the tables. Which can be ORM-accessible.
    """

    logger.info("Initializing a database...")
    db_instance: Database = Database(DATABASE_URL_PATH)
    sql_engine = create_engine(
        DATABASE_URL_PATH, connect_args={"check_same_thread": False}
    )

    db_file_ref: Path = Path(DATABASE_RAW_PATH)
    bc_file_ref: Path = Path(BLOCKCHAIN_RAW_PATH)

    logger.debug(
        f"SQL Engine Connector (Reference) and Async Instance for the {DATABASE_URL_PATH} has been instantiated."
    )

    if runtime == "__main__":

        # This is just an additional checking.
        if (db_file_ref.is_file() and bc_file_ref.is_file()) and auth_key is not None:

            con: Connection | None = None

            logger.info("Decrypting the database...")
            crypt_file(
                filename=DATABASE_RAW_PATH,
                key=auth_key,
                process=CryptFileAction.TO_DECRYPT,
            )

            try:
                con = connect(DATABASE_RAW_PATH)

            except OperationalError as e:
                logger.error(
                    f"Database is potentially corrupted or missing. | Additional Info: {e}"
                )
                _exit(1)

            finally:
                logger.info("Database decrypted.")
                if con is not None:
                    con.close()

            store_db_instance(db_instance)
            logger.debug("Database instance has been saved for access later.")

            logger.info("Decrypting a blockchain file ...")
            crypt_file(
                filename=BLOCKCHAIN_RAW_PATH,
                key=auth_key,
                process=CryptFileAction.TO_DECRYPT,
            )
            logger.info("Blockchain file decrypted.")

            return db_instance

        # This may not be tested.
        elif (db_file_ref.is_file() and bc_file_ref.is_file()) and auth_key is None:
            logger.critical(
                f"A database exists but there's no key inside of {AUTH_ENV_FILE_NAME} or the file ({AUTH_ENV_FILE_NAME}) is missing. Have you modified it? Please check and try again."
            )
            _exit(1)

        elif (
            not db_file_ref.is_file() or bc_file_ref.is_file()
        ) and auth_key is not None:
            logger.critical(
                "Hold up! You seem to have a key but don't have a database or the blockchain. Have you modified the directory? If so, please put the database back (encrypted) and try again. Otherwise, delete the key and try again if you are attempting to create a new instance."
            )
            _exit(1)

        else:
            logger.warning(
                f"Database and blockchain file does not exists. Creating a new database with a file name {DATABASE_NAME} and blockchain file named as {BLOCKCHAIN_NAME}"
            )

            model_metadata.create_all(sql_engine)
            logger.info("Database structure applied...")

            logger.warning(
                f"The system detects the invocation of a role as a {NodeRoles.MASTER.name}, please create a "
            )

            logger.info("Encrypting a new database ...")
            auth_key = crypt_file(
                filename=DATABASE_RAW_PATH,
                key=auth_key,
                process=CryptFileAction.TO_ENCRYPT,
                return_new_key=True,
            )

            if auth_key is None:
                raise NoKeySupplied(
                    initialize_resources_and_return_db_context,
                    "This part of the function should have a returned new auth key. This was not intended! Please report this issue as soon as possible!",
                )

            # Since encrypting the database also returns a new generated key, used that as a reference for the second argument.
            logger.info("Encrypting a new blockchain file ...")

            with open(BLOCKCHAIN_RAW_PATH, "w") as temp_writer:

                initial_json_context: dict[str, list[Any]] = {"chain": []}
                json_export(initial_json_context, temp_writer)

            crypt_file(
                filename=BLOCKCHAIN_RAW_PATH,
                key=auth_key,
                process=CryptFileAction.TO_ENCRYPT,
            )

            logger.info("Encrypting resources done.")

            if role is NodeRoles.MASTER:
                logger.warning(
                    f"The system detects the invocation of role as a {NodeRoles.MASTER.name}. Please insert email address and password for the email services."
                )
                logger.warning(
                    "Please ENSURE that credentials are correct. Don't worry, it will be hashed along with the `auth_key` that is generated here."
                )

            credentials: list[CredentialContext] = await ensure_input_prompt(
                input_context=["Email Address", "Email Password"],
                hide_fields=[False, True],
                generalized_context="Server email credentials",
                additional_context="There's no going back once proceeded.",
            )

            # Override AUTH_FILE_NAME after encryption.
            logger.info("Generating a new key environment file ...")
            with open(AUTH_ENV_FILE_NAME, "w") as env_writer:
                env_context: list[str] = [
                    f"AUTH_KEY={auth_key.decode('utf-8')}",
                    f"SECRET_KEY={token_hex(32)}",
                    f"EMAIL_SERVER_ADDRESS={credentials[0]}",
                    f"EMAIL_SERVER_PWD={credentials[1]}",
                ]

                for each_context in env_context:
                    env_writer.write(each_context + "\n")

            logger.info("Generation of new key file is done ...")

            logger.info(
                f"Generation of resources is done! Please check the file {AUTH_ENV_FILE_NAME}. DO NOT SHARE THOSE CREDENTIALS. | You need to relaunch this program so that the program will load the generated keys from the file."
            )
            _exit(1)

    store_db_instance(db_instance)
    return db_instance


async def close_resources(*, key: KeyContext) -> None:
    """
    Asynchronous Database Close Function.

    Async-ed since on_event("shutdown") is under async scope and does
    NOT await non-async functions.
    Closes the state of the database by encrypting it back to the uninitialized state.

    Args:
        key (KeyContext): The key that is recently used for decrypting the SQLite database.

    """
    logger.warn("Closing database and blockchain files by encryption...")

    await acrypt_file(
        afilename=DATABASE_RAW_PATH, akey=key, aprocess=CryptFileAction.TO_ENCRYPT
    )
    await acrypt_file(
        afilename=BLOCKCHAIN_RAW_PATH, akey=key, aprocess=CryptFileAction.TO_ENCRYPT
    )

    logger.info("Database and blockchain successfully closed and encrypted.")


def validate_file_keys(
    context: KeyContext | None,
) -> tuple[KeyContext, KeyContext]:

    file_ref = f"{Path(__file__).cwd()}/{context}"
    # Validate if the given context is a path first.
    if Path(file_ref).is_file():

        from os import environ as env

        from dotenv import find_dotenv, load_dotenv

        try:
            # Redundant, but ensure.
            load_dotenv(
                find_dotenv(filename=str(Path(file_ref)), raise_error_if_not_found=True)
            )

        except OSError:
            exit(
                f"The file {file_ref} may not be a valid .env file or is missing. Please check your arguments or the file."
            )

        a_key: KeyContext = env.get("AUTH_KEY", None)
        s_key: KeyContext = env.get("SECRET_KEY", None)

        # Validate the (AUTH_KEY and SECRET_KEY)'s length.
        if (
            a_key is not None
            and a_key.__len__() == FERNET_KEY_LENGTH
            or s_key is not None
            and s_key.__len__() == SECRET_KEY_LENGTH
        ):

            return a_key, s_key

        raise NoKeySupplied(
            validate_file_keys,
            f"Error: One of the keys either has an invalid value or is missing. Have you modified your {file_ref}? Please check and try again.",
        )


# # File Resource Initializers and Validators, Blockchain and Database — END

# # Variable Password Crypt Handlers — START
def hash_context(*, pwd: RawData) -> HashedData:
    return pwd_handler.hash(pwd)


def verify_hash_context(*, real_pwd: RawData, hashed_pwd: HashedData) -> bool:
    return pwd_handler.verify(real_pwd, hashed_pwd)


async def ensure_input_prompt(
    *,
    input_context: list[Any] | Any,
    hide_fields: list[bool] | bool,
    generalized_context: str,
    additional_context: str | None = None,
    enable_async: bool = False,
    delimiter: str = ":",
) -> Any:

    # * Assert in list form for all readable type.
    assert_lvalue: int = len(
        input_context if isinstance(input_context, list) else [input_context]
    )
    assert_rvalue: int = len(
        hide_fields if isinstance(input_context, list) else [hide_fields]  # type: ignore # ??? | Resolve the `Sized` incompatibility with bool.
    )

    assert (
        assert_lvalue == assert_rvalue
    ), f"The `input_context` (length of {assert_lvalue}) and the `hide_fields` (length of {assert_rvalue}) were unequal! This is a developer issue, please report as possible."

    while True:
        input_s: list[str] | str = (
            "" or []
        )  # TODO: Not a prio but have to fix its typing later.
        if isinstance(input_context, list) and isinstance(hide_fields, list):
            for field_idx, each_context_to_input in enumerate(input_context):
                while True:
                    _input = (
                        (
                            input(f"{each_context_to_input}{delimiter} ")
                            if not enable_async
                            else await ainput(f"{each_context_to_input}{delimiter} ")
                        )
                        if not hide_fields[field_idx]
                        else getpass(f"{each_context_to_input}{delimiter} ")
                    )

                    if not _input:
                        logger.critical(
                            f"One of the inputs for the {generalized_context} is empty! Please try again."
                        )
                        continue

                    if isinstance(input_s, list):
                        input_s.append(_input)

                    break

        else:
            input_s = (
                (
                    input(f"{input_context}{delimiter} ")
                    if not enable_async
                    else await ainput(f"{input_context}{delimiter} ")
                )
                if not hide_fields
                else getpass(str(f"{input_context}{delimiter} "))
            )

            if not input_s:
                logger.critical(
                    f"The input for the {generalized_context} is empty! Please try again."
                )
                continue

        logger.warning(
            f"Are you sure you this is the right{(' ' + generalized_context) if generalized_context is not None else ''}? {additional_context}"
        )

        ensure: str = input(
            f"[Press any key to continue / N or n to re-type {generalized_context}] > "
        )

        if ensure == "n" or ensure == "N":
            continue

        return input_s


# # Variable Password Crypt Handlers — END


# # Blockchain
# TODO: We need to import the HTTP here.
async def look_for_nodes(*, role: NodeRoles, host: IPAddress, port: IPPort) -> None:
    logger.info(
        f"Step 2.1 | Attempting to look {'for the master node' if role == NodeRoles.MASTER.name else 'at other nodes'} at host {host}, port {port}..."
    )
