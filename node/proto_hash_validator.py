from asyncio import run as asyncio_run_loop
from asyncio import sleep
from base64 import urlsafe_b64encode
from datetime import datetime
from hashlib import sha256
from logging import Logger, getLogger
from logging.config import dictConfig
from typing import Any, Final
from pydantic import ValidationError

import uvicorn
from aioconsole import ainput
from aiohttp import ClientResponse
from cryptography.fernet import Fernet, InvalidToken
from orjson import JSONDecodeError, dumps as orjson_dumps
from orjson import loads as orjson_loads

from blueprint.schemas import (
    AdditionalContextTransaction,
    GroupTransaction,
    StudentLogTransaction,
)
from core.constants import (
    ASYNC_TARGET_LOOP,
    TRANSACTION_PAYLOAD_FROM_ADDRESS_CHAR_CUTOFF_INDEX,
    TRANSACTION_PAYLOAD_MAX_CHAR_COUNT,
    TRANSACTION_PAYLOAD_MIN_CHAR_COUNT,
    TRANSACTION_PAYLOAD_TIMESTAMP_FORMAT_AS_KEY,
    HTTPQueueMethods,
    LoggerLevelCoverage,
    TransactionContextMappingType,
    URLAddress,
)
from utils.http import HTTPClient
from utils.logger import LoggerHandler

logger_config: dict[str, Any] = LoggerHandler.init(
    base_config=uvicorn.config.LOGGING_CONFIG,  # type: ignore # ???
    disable_file_logging=False,
    logger_level=LoggerLevelCoverage.INFO,
)


dictConfig(logger_config)
logger: Logger = getLogger(ASYNC_TARGET_LOOP)
# # Constants
BACKEND_TX_BASE_ENDPOINT: Final[
    str
] = "folioblocks.southeastasia.azurecontainer.io/explorer/transaction"


class HashContentValidator(HTTPClient):
    def __init__(self) -> None:
        self.selection: int = 0
        self.expected_hash: str = ""
        self.tx_hash: str = ""
        self.generated_model: AdditionalContextTransaction | GroupTransaction | None = (
            None
        )

        # # Initialize the HTTPClient, which is an Async.
        super().__init__()

    async def runthrough(self) -> None:
        await self.initialize()

        while True:
            self.tx_hash = await ainput("Input the Transaction Hash: ")

            if len(self.tx_hash) != 64:
                logger.error(
                    "Transaction hash should be exactly 64 characters! Exiting ..."
                )
                await self.close(should_destroy=True)
                exit(1)

            logger.info("Should I Decrypt [0] or Encrypt [1]? (Or C to Cancel)")

            self.selection = await ainput("|> ")

            if self.selection == "C" or self.selection == "c":
                logger.warning("Process cancelled.")
                await self.close(should_destroy=True)
                exit(0)

            elif self.selection == "0" or self.selection == "1":
                logger.info(
                    f"Hash to compare against this transaction (note that you selected {'encryption' if self.selection == 1 else 'decryption'})"
                )
                self.expected_hash = await ainput("|> ")

                # ! We need to supply some inputs.
                if self.selection == "1":
                    extra_remarks_inputs = [
                        "Address Origin",
                        "Title",
                        "Description",
                        "Inserter",
                        "Timestamp",
                    ]
                    document_log_inputs = [
                        "Address Origin",
                        "Name",
                        "Description",
                        "Role",
                        "File (Unique Identifier, Get the URL of the file and get the parameter)",
                        "Duration Start",
                        "Duration End (Type 'None' as-is if there's none)",
                        "Validated By",
                        "Timestamp",
                    ]
                    list_of_inputs = (
                        []
                    )  # ! Just a storage, this phase of data is not friendly against other objects.

                    while True:
                        choice: str = ""
                        was_additional_type: bool = False  # ? If false, its evaluated as document / logs, otherwise its extra / remarks.

                        logger.warning(
                            "Was this content a document / log [1] or extra / remarks [2]? (CTRL + C to Cancel.)"
                        )

                        if choice == "1":
                            logger.info("Chosen Extra / Remarks Model.")
                            was_additional_type = True

                        elif choice == "2":
                            logger.info("Chosen Document / Log Model.")
                            was_additional_type = (
                                False  # * Redundant, just making it sure.
                            )

                        else:
                            logger.error("Invalid input.")
                            continue

                        for idx, each_field in enumerate(
                            document_log_inputs
                            if was_additional_type
                            else extra_remarks_inputs
                        ):
                            logger.info(each_field)
                            user_input = await ainput(f"({idx}) |> ")

                            list_of_inputs.append(user_input)

                        break

                    logger.info("Building the model.")
                    try:
                        context_dict: dict  # ! Type annotation.
                        if was_additional_type:
                            context_dict = {
                                "address_origin": list_of_inputs[0],
                                "title": list_of_inputs[1],
                                "description": list_of_inputs[2],
                                "inserter": list_of_inputs[3],
                                "timestamp": datetime,
                            }
                        else:
                            context_dict = {
                                "address_origin": list_of_inputs[0],
                                "name": list_of_inputs[1],
                                "description": list_of_inputs[2],
                                "role": list_of_inputs[3],
                                "file": list_of_inputs[4],
                                "duration_start": list_of_inputs[5],
                                "duration_end": list_of_inputs[6]
                                if list_of_inputs[6] is not None
                                else None,
                                "validated_by": list_of_inputs[7],
                                "timestamp": list_of_inputs[8],
                            }

                        built_model_from_input: AdditionalContextTransaction | StudentLogTransaction = globals()[
                            AdditionalContextTransaction.__name__
                            if was_additional_type
                            else StudentLogTransaction.__name__
                        ](
                            context_dict
                        )

                        # - Get the hash of this built model, and compare it against the given hash.
                        built_model_hash: str = sha256(
                            orjson_dumps(built_model_from_input.dict())
                        ).hexdigest()
                        logger.info(f"Built model hash is {built_model_hash}")

                        if built_model_hash == self.expected_hash:
                            logger.info(
                                f"Built model hash and expected hash were MATCH | Built Model: {built_model_hash}, Expected Hash: {self.expected_hash}"
                            )
                        else:
                            logger.info(
                                f"Built model hash and expected hash did not MATCH | Built Model: {built_model_hash}, Expected Hash: {self.expected_hash}"
                            )
                            exit(1)

                    except (ValidationError, ValueError) as e:
                        logger.critical(
                            "There was an error while building the model. Please ensure your input and try again. | Info: {e}"
                        )

                logger.info(f"Processing the transaction hash {self.tx_hash}.")
                break

            else:
                logger.error("Invalid input.")

        tx_request: ClientResponse = await self.enqueue_request(
            url=URLAddress(f"{BACKEND_TX_BASE_ENDPOINT}/{self.tx_hash}"),
            await_result_immediate=True,
            data=None,
            headers=None,
            do_not_retry=False,
            method=HTTPQueueMethods.GET,
            retry_attempts=99,
            return_on_error=False,
            use_secure_protocol=True,
        )

        logger.info(
            f"Result: {'OK' if tx_request.ok else 'NOT OKAY. Please check your transaction hash and try again.'}"
        )

        if not tx_request.ok:
            exit(1)

        requested_tx_payload: str = await tx_request.json()

        logger.info(
            f"Transaction Context Payload Result: {requested_tx_payload['transaction']['payload']} | Transaction Action Number: {requested_tx_payload['transaction']['action']}"  # type: ignore
        )

        # ! Resolve the the transaction addresses as transaction action value is part of the key.
        # @o The length allocation for the address has to be dynamically adjusted based on the transaction action.
        tx_action: int = (
            TRANSACTION_PAYLOAD_MIN_CHAR_COUNT  # ? Value is 11.
            if len(str(requested_tx_payload["transaction"]["action"])) == 2  # type: ignore
            else TRANSACTION_PAYLOAD_MAX_CHAR_COUNT  # ? Value is 12.
        )

        # # Construct the key.
        constructed_key_to_decrypt: bytes = (
            str(requested_tx_payload["transaction"]["action"])  # type: ignore
            + requested_tx_payload["transaction"]["from_address"][  # type: ignore
                :TRANSACTION_PAYLOAD_FROM_ADDRESS_CHAR_CUTOFF_INDEX  # ! Value is 7.
            ]
            + requested_tx_payload["transaction"]["to_address"][-tx_action:]  # type: ignore
            + datetime.fromisoformat(requested_tx_payload["transaction"]["timestamp"]).strftime(  # type: ignore
                TRANSACTION_PAYLOAD_TIMESTAMP_FORMAT_AS_KEY
            )  # ! Value is '%m%y%d%H%M%S'.
        ).encode("utf-8")

        payload_key: bytes = urlsafe_b64encode(constructed_key_to_decrypt)
        logger.info(f"Payload key generated.")

        try:
            # # 5
            payload_processor: Fernet = Fernet(payload_key)
            logger.info("Payload key accepted from the content processor.")

            processed_content: bytes = payload_processor.decrypt(
                requested_tx_payload["transaction"]["payload"]["context"].encode(  # type: ignore
                    "utf-8"
                )
            )

            try:
                loaded_processed_content: dict = orjson_loads(processed_content)
                logger.info(
                    f"Content Decrypted.",
                )

                built_model: GroupTransaction = GroupTransaction(
                    content_type=TransactionContextMappingType(requested_tx_payload["transaction"]["payload"]["content_type"]),  # type: ignore
                    context=globals()[
                        StudentLogTransaction.__name__
                        if requested_tx_payload["transaction"]["payload"][  # type: ignore
                            "content_type"  # type: ignore
                        ]
                        == 2
                        else AdditionalContextTransaction.__name__
                    ](**loaded_processed_content),
                )

                dict_model_json: bytes = orjson_dumps(built_model.dict())
                logger.info("User Transaction Model has been rebuilt.")

                hash_of_dict_model: str = sha256(dict_model_json).hexdigest()
                logger.info("User Transaction Hash Calculated.")

                if self.expected_hash == hash_of_dict_model:
                    logger.info(
                        f"Given hash and computed hash from rebuilt model WERE MATCHED!\n\nCalculated (from Rebuilt Model) Hash: {hash_of_dict_model}\nGiven Hash: {self.expected_hash}\n"
                    )
                    exit(0)

                else:
                    logger.critical(
                        f"Given hash and computed hash from rebuilt model WERE NOT MATCHED! Please check your hash input and try again. | Calculated Hash: {hash_of_dict_model}, Given Hash: {self.expected_hash}"
                    )
                    exit(1)

            except KeyError:
                logger.critical(
                    "This transaction may not be a user transaction! Internal transaction cannot be validated due to its decrypted content, exposing some truths. Please run the script and try again."
                )
                await self.close(should_destroy=True)
                exit(1)

            except JSONDecodeError as e:
                logger.critical(f"There was an error during JSON decoding. | Info: {e}")

        except InvalidToken as e:
            logger.critical(
                f"Invalid token. Check the backend code and try again. | Additional Info: {e}"
            )

        finally:
            await self.close(should_destroy=True)  # ! Close the connection.
            await sleep(3)


tester_instance = HashContentValidator()
asyncio_run_loop(tester_instance.runthrough())
