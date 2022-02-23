"""
SQLite ORM-able Database for the Node Backend API (database.py)

TODO:

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the gnu general public license as published by the free software foundation, either version 3 of the license, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. see the gnu general public license for more details.
you should have received a copy of the gnu general public license along with FolioBlocks. if not, see <https://www.gnu.org/licenses/>.
"""

if __name__ == "__main__":
    raise SystemExit(
        f"You cannot use the {__file__} as an entrypoint module! Please use the main module or import this module to the other modules."
    )

from logging import getLogger
from os import _exit
from pathlib import Path
from secrets import token_hex
from sqlite3 import Connection, OperationalError, connect

import aiofiles
from cryptography.fernet import Fernet, InvalidToken
from databases import Database
from sqlalchemy import create_engine
from utils.constants import (
    ASYNC_TARGET_LOOP,
    AUTH_FILE_NAME,
    DATABASE_NAME,
    DATABASE_RAW_PATH,
    DATABASE_URL_PATH,
    KeyContext,
    RuntimeLoop,
)

from database.models import DeclarativeModel

logger = getLogger(ASYNC_TARGET_LOOP)


def init_db(runtime: RuntimeLoop, auth_key: KeyContext | None = None) -> Database:
    """
    A non-async database initializer.

    Initializes the database when the async thread is not yet initialized.

    Args:
        runtime (RuntimeLoop): The runtime context, this is evaluated from __name__.
        keys (tuple[KeyContext, KeyContext] | None, optional): The value of the key that is parsed from the argparse library. Defaults to None.

    Returns:
        Database | None: Returns the context of the database for accessing the tables. Which can be ORM-accessible.
    """
    db_instance: Database = Database(DATABASE_URL_PATH)
    sql_engine = create_engine(
        DATABASE_URL_PATH, connect_args={"check_same_thread": False}
    )

    db_file_ref: Path[str] = Path(f"{Path(__file__).cwd()}/{DATABASE_NAME}")

    logger.info(  # TODO: DEBUG in -ll doesn't work.
        f"SQL Engine Connector (Reference) and Async Instance for the {DATABASE_URL_PATH} has been instantiated."
    )

    if runtime == "__main__":

        # This is just an additional checking.
        if db_file_ref.is_file() and auth_key is not None:

            con: Connection | None = None
            out_db_contents: bytes = b""

            logger.info("Decrypting the database...")

            with open(DATABASE_RAW_PATH, "rb") as _:
                out_db_contents = _.read()

            try:
                to_decrypt_context: Fernet = Fernet(auth_key.encode("utf-8"))
                decryptext_context = to_decrypt_context.decrypt(out_db_contents)

                logger.info("Successfully decrypted, loading the database...")

            except InvalidToken:  # No need to elaborate since its empty.
                logger.critical(
                    f"Decryption failed. The supplied key seems to be invalid! Please check your argument and try again."
                )
                _exit(1)

            with open(DATABASE_RAW_PATH, "wb") as _:
                _.write(decryptext_context)

            try:
                con = connect(DATABASE_RAW_PATH)

            except OperationalError as e:
                logger.error(
                    f"Database is potentially corrupted or missing. | Additional Info: {e}"
                )
                _exit(1)

            finally:
                logger.info("Database validation is finished.")
                if con is not None:
                    con.close()

            return db_instance

        # This may not be tested.
        elif db_file_ref.is_file() and auth_key is None:
            logger.critical(
                f"A database exists but there's no key inside of {AUTH_FILE_NAME} or the file ({AUTH_FILE_NAME}) is missing. Have you modified it? Please check and try again."
            )
            _exit(1)

        elif not db_file_ref.is_file() and auth_key is not None:
            logger.critical(
                "Hold up! You seem to have a key but don't have a database. Have you modified the directory? If so, please put the database back (encrypted) and try again. Otherwise, delete the key and try again if you are attempting to create a new instance."
            )
            _exit(1)

        else:
            # if db_file_ref.is
            logger.warning(
                f"Database does not exists. Creating a new database {DATABASE_NAME}..."
            )

            DeclarativeModel.metadata.create_all(sql_engine)

            logger.info("Encrypting the new database...")

            in_memory_db_contents: bytes = b""

            with open(DATABASE_RAW_PATH, "rb") as _:
                in_memory_db_contents = _.read()

            with open(DATABASE_RAW_PATH, "wb") as _:
                key = Fernet.generate_key()
                context = Fernet(key)
                encrypted_context = context.encrypt(in_memory_db_contents)  # TODO: ???
                _.write(encrypted_context)

            in_memory_db_contents = b""  # Erase right after.

            # Override AUTH_FILE_NAME after encryption.
            with open(AUTH_FILE_NAME, "w") as env_writer:
                env_context: list[str] = [
                    f"AUTH_KEY={key.decode('utf-8')}",
                    f"SECRET_KEY={token_hex(32)}",
                ]

                for each_context in env_context:
                    env_writer.write(each_context + "\n")

            logger.info(
                f"Encryption is done and a new set of keys has been generated. Please check the file {AUTH_FILE_NAME}. DO NOT SHARE THOSE CREDENTIALS. | You need to relaunch this program so that the program will load the generated keys from the file."
            )
            _exit(1)

    return db_instance


async def close_db(key: KeyContext) -> None:
    """

    Asynchronous Database Close Function.

    Async-ed since on_event("shutdown") is under async scope and does
    NOT await non-async functions.

    Closes the state of the database by encrypting it back to the uninitialized state.

    Args:
        key (KeyContext): The key that is recently used for decrypting the SQLite database.

    Notes:
        - Despite wanting to be less redundant, I will make exceptions since time is so hectic for me to deal it.
    """
    logger.warn("Closing database instance by encryption...")

    async with aiofiles.open(DATABASE_RAW_PATH, "rb") as _:
        logger.info("Reading last state of the database ...")
        recent_db_contents = await _.read()

    async with aiofiles.open(DATABASE_RAW_PATH, "wb") as _:
        logger.info("Database encryption in progress ...")

        context = Fernet(key)
        encrypted_context = context.encrypt(recent_db_contents)

        await _.write(encrypted_context)

    logger.info("Database successfully closed and encrypted.")
