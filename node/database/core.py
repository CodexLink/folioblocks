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

from logging import Logger, getLogger
from os import _exit
from pathlib import Path
from secrets import token_hex
from sqlite3 import Connection, OperationalError, connect

from databases import Database
from sqlalchemy import create_engine
from utils.constants import (
    ASYNC_TARGET_LOOP,
    AUTH_FILE_NAME,
    BLOCKCHAIN_NAME,
    BLOCKCHAIN_RAW_PATH,
    DATABASE_NAME,
    DATABASE_RAW_PATH,
    DATABASE_URL_PATH,
    CryptFileAction,
    KeyContext,
    RuntimeLoop,
)
from utils.database import store_db_instance
from utils.exceptions import NoKeySupplied
from utils.files import acrypt_file, crypt_file

from database.models import model_metadata

logger: Logger = getLogger(ASYNC_TARGET_LOOP)


def initialize_resources(
    runtime: RuntimeLoop, auth_key: KeyContext | None = None
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

    logger.info("Initializing a database..")
    db_instance: Database = Database(DATABASE_URL_PATH)
    sql_engine = create_engine(
        DATABASE_URL_PATH, connect_args={"check_same_thread": False}
    )

    db_file_ref: Path = Path(DATABASE_RAW_PATH)
    bc_file_ref: Path = Path(BLOCKCHAIN_RAW_PATH)

    logger.info(  # TODO: DEBUG in -ll doesn't work.
        f"SQL Engine Connector (Reference) and Async Instance for the {DATABASE_URL_PATH} has been instantiated."
    )

    if runtime == "__main__":

        # This is just an additional checking.
        if (db_file_ref.is_file() and bc_file_ref.is_file()) and auth_key is not None:

            con: Connection | None = None

            logger.info("Decrypting the database...")
            crypt_file(DATABASE_RAW_PATH, auth_key, CryptFileAction.TO_DECRYPT)

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
            logger.info("Database instance has been saved for access later.")

            logger.info("Decrypting a blockchain file ...")
            crypt_file(BLOCKCHAIN_RAW_PATH, auth_key, CryptFileAction.TO_DECRYPT)
            logger.info("Blockchain file decrypted.")

            return db_instance

        # This may not be tested.
        elif (db_file_ref.is_file() and bc_file_ref.is_file()) and auth_key is None:
            logger.critical(
                f"A database exists but there's no key inside of {AUTH_FILE_NAME} or the file ({AUTH_FILE_NAME}) is missing. Have you modified it? Please check and try again."
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
            logger.info("Database context inserted ...")

            logger.info("Encrypting a new database ...")
            auth_key = crypt_file(
                DATABASE_RAW_PATH, auth_key, CryptFileAction.TO_ENCRYPT, True
            )

            if auth_key is None:
                raise NoKeySupplied(
                    initialize_resources,
                    "This part of the function should have a returned new auth key. This was not intended! Please report this issue as soon as possible!",
                )

            # Since encrypting the database also returns a new generated key, used that as a reference for the second argument.
            logger.info("Encrypting a new blockchain file ...")

            # TODO: THis will be removed later, after we finish the database and other stuff.
            with open(BLOCKCHAIN_RAW_PATH, "w") as temp_writer:
                temp_writer.write("test.")

            crypt_file(BLOCKCHAIN_RAW_PATH, auth_key, CryptFileAction.TO_ENCRYPT)

            logger.info("Encrypting resources done.")

            # Override AUTH_FILE_NAME after encryption.
            logger.info("Generating a new key environment file ...")
            with open(AUTH_FILE_NAME, "w") as env_writer:
                env_context: list[str] = [
                    f"AUTH_KEY={auth_key.decode('utf-8')}",
                    f"SECRET_KEY={token_hex(32)}",
                ]

                for each_context in env_context:
                    env_writer.write(each_context + "\n")

            logger.info("Generation of new key file is done ...")

            logger.info(
                f"Generation of resources is done! Please check the file {AUTH_FILE_NAME}. DO NOT SHARE THOSE CREDENTIALS. | You need to relaunch this program so that the program will load the generated keys from the file."
            )
            _exit(1)

    store_db_instance(db_instance)

    return db_instance


async def close_resources(key: KeyContext) -> None:
    """

    Asynchronous Database Close Function.

    Async-ed since on_event("shutdown") is under async scope and does
    NOT await non-async functions.

    Closes the state of the database by encrypting it back to the uninitialized state.

    Args:
        key (KeyContext): The key that is recently used for decrypting the SQLite database.

    """
    logger.warn("Closing database instance by encryption...")

    await acrypt_file(DATABASE_RAW_PATH, key, CryptFileAction.TO_ENCRYPT)
    await acrypt_file(BLOCKCHAIN_RAW_PATH, key, CryptFileAction.TO_ENCRYPT)

    logger.info("Database successfully closed and encrypted.")
