"""
Processor Functions (processors.py) | Set of functions that processes a particular object / entity / elements, whatever you call it.

These functions varies from handling file resources and contents of a variable.
Please note that there are no distinctions / categorization (exception for alphabetical) available for each functions, read their description to understand their uses.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from asyncio import get_event_loop
from getpass import getpass
from hashlib import sha256
from json import dump as json_export
from logging import Logger, getLogger
from os import _exit
from pathlib import Path
from secrets import token_hex
from sqlite3 import Connection, OperationalError, connect
from typing import Any

from aioconsole import ainput
from aiofiles import open as aopen
from blueprint.models import file_signatures, model_metadata
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
from core.dependencies import get_db_instance, store_db_instance
from cryptography.fernet import Fernet, InvalidToken
from databases import Database
from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy import create_engine

from utils.exceptions import NoKeySupplied, UnsatisfiedClassType

logger: Logger = getLogger(ASYNC_TARGET_LOOP)
pwd_handler: CryptContext = CryptContext(schemes=["bcrypt"])

# # File Handlers, Cryptography — START
async def crypt_file(
    *,
    filename: str,
    key: KeyContext,
    process: CryptFileAction,
    return_new_key: bool = False,
    enable_async: bool = False,
) -> bytes | None:
    """
    A Non-async function that processes a file with `to` under `filename` that uses `key` for decrypt and encrypt processes. This function exists for providing anti-redundancy over calls for preparing the files that has to be initialized for the session. This function is not compatible during async process, please refer to the acrypt_file for the implementation of async version.
    """

    if not isinstance(process, CryptFileAction):
        raise UnsatisfiedClassType(process, CryptFileAction)

    processed_content: bytes = b""
    crypt_context: Fernet | None = None
    file_content: str | bytes = ""

    # Open the file first.
    file_content = await process_crpyt_file(
        is_async=enable_async, filename=filename, mode="rb"
    )

    try:
        logger.debug(
            f"{'Async:' if enable_async else ''}{'Decrypting' if process is CryptFileAction.TO_DECRYPT else 'Encrypting'} a context..."
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
        await process_crpyt_file(
            content_to_write=processed_content,
            filename=filename,
            is_async=enable_async,
            mode="wb",
        )

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


async def process_crpyt_file(
    *,
    is_async: bool,
    filename: str,
    mode: Any,  # Cannot import Literals for the aiofiles.mode here.
    content_to_write: Any = None,
) -> str | bytes:

    # * In the near future, we can do something about this one.
    resolved_fn_name: str = "read" if mode == "rb" else "write"

    if is_async:
        async with aopen(filename, mode) as acontent_buffer:
            file_content: str | bytes = await getattr(
                acontent_buffer, resolved_fn_name
            )(content_to_write if mode == "wb" else None)
    else:
        with open(filename, mode) as content_buffer:
            file_content = getattr(content_buffer, resolved_fn_name)(
                content_to_write if mode == "wb" else None
            )

    return file_content


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
            await crypt_file(
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
            await crypt_file(
                filename=BLOCKCHAIN_RAW_PATH,
                key=auth_key,
                process=CryptFileAction.TO_DECRYPT,
            )
            logger.info("Blockchain file decrypted.")

            logger.info("Checking integration of the blockchain file...")
            # TODO
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
            auth_key = await crypt_file(
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

            await crypt_file(
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

    await crypt_file(
        filename=DATABASE_RAW_PATH,
        key=key,
        process=CryptFileAction.TO_ENCRYPT,
        enable_async=True,
    )
    await crypt_file(
        filename=BLOCKCHAIN_RAW_PATH,
        key=key,
        process=CryptFileAction.TO_ENCRYPT,
        enable_async=True,
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
                    _item_input = await handle_input_function(
                        awaited=enable_async,
                        input_hidden=hide_fields[field_idx],
                        message=f"{each_context_to_input}{delimiter} ",
                    )

                    if not _item_input:
                        logger.critical(
                            f"One of the inputs for the {generalized_context} is empty! Please try again."
                        )
                        continue

                    if isinstance(input_s, list):
                        input_s.append(_item_input)

                    break

        else:
            if isinstance(hide_fields, bool):
                input_s = await handle_input_function(
                    awaited=enable_async,
                    input_hidden=hide_fields,
                    message=f"{input_context}{delimiter} ",
                )
            else:
                logger.exception(
                    f"Assertion Error: Input hidden is not a type 'bool'. This condition scope does not expect type {type(hide_fields)}."
                )
                exit(-1)

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


async def handle_input_function(
    *, awaited: bool, input_hidden: bool, message: str
) -> str:
    """
    Technically a handler to the input that is being called by ensure_input_prompt.

    Seperated since list form and singleton parameter uses the same mechanism.

    Args:
        awaited (bool): Is the input being awaited `was async` or not?
        input_hidden (bool): Is the input hidden or not?
        message (str): The message to display incorporated with the input.
    """
    event_loop_ref = get_event_loop()

    if not input_hidden and not awaited:
        _ireturned: str = input(message)

    elif input_hidden and awaited:
        _ireturned = await event_loop_ref.run_in_executor(None, getpass, message)

    elif not input_hidden and awaited:
        _ireturned = await ainput(message)

    else:  # ! Resolves to `input_hidden` and not `awaited`.
        _ireturned = getpass(message)

    return _ireturned


# # Variable Password Crypt Han1dlers — END


# # Blockchain
# TODO: We need to import the HTTP here.
async def look_for_nodes(*, role: NodeRoles, host: IPAddress, port: IPPort) -> None:
    logger.info(
        f"Step 2.1 | Attempting to look {'for the master node' if role == NodeRoles.MASTER.name else 'at other nodes'} at host {host}, port {port}..."
    )

# TODO: Function to below is just a prototype. TO BE TESTED.
async def verify_hash_blockchain(
    *, blockchain_contents: str | bytes, db: Database = Depends(get_db_instance)
) -> bool:
    verify_hash_stmt = file_signatures.select(file_signatures.c.file == BLOCKCHAIN_NAME)
    blockchain_file_hash = await db.execute(verify_hash_stmt)

    resolve_type_contents: bytes = (
        blockchain_contents.encode("utf-8")
        if isinstance(blockchain_contents, str)
        else blockchain_contents
    )

    return sha256(resolve_type_contents).hexdigest() == blockchain_file_hash


def process_blockchain_hash_state(
    *,
    blockchain_contents: str | bytes,
    should_update: bool = False,
) -> None:

    resolved_blockchain_contents: bytes = (
        blockchain_contents.encode("utf-8")
        if isinstance(blockchain_contents, str)
        else blockchain_contents
    )

    if should_update:
        file_signatures.update().where(
            file_signatures.c.file == BLOCKCHAIN_NAME
        ).values(signature=sha256(resolved_blockchain_contents))

    else:
        file_signatures.insert().values(
            filename=BLOCKCHAIN_NAME, signature=sha256(resolved_blockchain_contents)
        )
