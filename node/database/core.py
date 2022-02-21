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
from os import _exit, system
from pathlib import Path
from sqlite3 import Connection, OperationalError, connect

from cryptography.fernet import Fernet, InvalidToken
from databases import Database
from sqlalchemy import create_engine
from utils.constants import (
    ASYNC_TARGET_LOOP,
    DATABASE_NAME,
    DATABASE_RAW_PATH,
    DATABASE_URL_PATH,
    KeyContext,
    RuntimeLoop,
)

from database.models import DeclarativeModel

logger = getLogger(ASYNC_TARGET_LOOP)


def init_db(runtime: RuntimeLoop, key: KeyContext | None = None) -> Database | None:
    """Initializes the database when the async thread is not yet initialized.

    Args:
        runtime (RuntimeLoop): The runtime context, this is evaluated from __name__.
        key (KeyContext | None, optional): The value of the key that is parsed from the argparse library. Defaults to None.

    Returns:
        Database | None: Returns the context of the database for accessing the tables. Which can be ORM-accessible.
    """
    db_instance: Database = Database(DATABASE_URL_PATH)
    sql_engine = create_engine(
        DATABASE_URL_PATH, connect_args={"check_same_thread": False}
    )

    logger.info(  # TODO: DEBUG in -ll doesn't work.
        f"SQL Engine Connector (Reference) and Async Instance for the {DATABASE_URL_PATH} has been instantiated."
    )

    if runtime == "__main__":

        # This is just an additional checking.
        if not Path(f"{Path(__file__).cwd()}/{DATABASE_NAME}").is_file() and key:
            logger.warning("Key is supplied but disregarded.")

        if Path(f"{Path(__file__).cwd()}/{DATABASE_NAME}").is_file() and key:

            con: Connection | None = None
            out_db_contents: bytes | None = None

            logger.info("Decrypting the database...")

            with open(DATABASE_RAW_PATH, "rb") as _:
                out_db_contents = _.read()

            try:
                to_decrypt_context: Fernet = Fernet(key.encode("utf-8"))
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

        elif Path(f"{Path(__file__).cwd()}/{DATABASE_NAME}").is_file() and not key:
            logger.critical("Key is required to use this program. Please try again.")
            _exit(1)

        else:
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

            logger.critical(
                f"Encryption is done. A new key has been generated. Please copy this before it disappears! | Key: {key.decode('utf-8')} | You need to relaunch this program and invoke the key in the parameter. Also, ensure that you save the key. It will not appear again! Press any to continue."
            )
            input(), system("CLS||CLEAR"), _exit(1)

    return None


def close_db(key: KeyContext) -> None:
    """
    Closes the state of the database by encrypting it back to the uninitialized state.

    Args:
        key (KeyContext): The key that is recently used for decrypting the SQLite database.

    Notes:
        - Despite wanting to be less redundant, I will make exceptions since time is so hectic for me to deal it.
    """
    logger.warn("Closing database instance by encryption...")

    with open(DATABASE_RAW_PATH, "rb") as _:
        logger.info("Reading last state of the database ...")
        recent_db_contents = _.read()

    with open(DATABASE_RAW_PATH, "wb") as _:
        logger.info("Database encryption in progress ...")

        context = Fernet(key)
        encrypted_context = context.encrypt(recent_db_contents)

        _.write(encrypted_context)

    logger.info("Database successfully closed and encrypted.")
