from argparse import Namespace
from asyncio import create_task, gather, get_event_loop, sleep
from base64 import urlsafe_b64encode
from copy import deepcopy
from datetime import datetime, timedelta
from hashlib import sha256
from http import HTTPStatus
from logging import Logger, getLogger
from pathlib import Path
from secrets import token_hex, token_urlsafe
from sqlite3 import IntegrityError
from sys import maxsize as MAX_INT_PYTHON
from time import time
from typing import Any, Final, Mapping
from uuid import uuid4

from aiofiles import open as aopen
from aiohttp import ClientResponse
from blueprint.models import (
    associated_nodes,
    associations,
    consensus_negotiation,
    file_signatures,
    tx_content_mappings,
    users,
)
from blueprint.schemas import (
    AdditionalContextTransaction,
    AgnosticCredentialValidator,
    ApplicantLogTransaction,
    ApplicantUserBaseTransaction,
    ApplicantUserTransaction,
    ArchivalMinerNodeInformation,
    Block,
    BlockOverview,
    ConsensusSuccessPayload,
    GroupTransaction,
    HashableBlock,
    NodeCertificateTransaction,
    NodeConfirmMineConsensusTransaction,
    NodeConsensusInformation,
    NodeGenesisTransaction,
    NodeMasterInformation,
    NodeMineConsensusSuccessProofTransaction,
    NodeRegisterTransaction,
    NodeSyncTransaction,
    NodeTransaction,
    OrganizationIdentityValidator,
    OrganizationUserBaseFields,
    OrganizationUserBaseTransaction,
    OrganizationUserTransaction,
    Transaction,
    TransactionSignatures,
)
from cryptography.fernet import Fernet
from databases import Database
from fastapi import HTTPException
from frozendict import frozendict
from orjson import dumps as export_to_json
from orjson import loads as import_raw_json_to_dict
from pydantic import BaseModel, EmailStr
from pydantic import ValidationError as PydanticValidationError
from pympler.asizeof import asizeof
from sqlalchemy import select
from sqlalchemy.sql.expression import Insert, Select, Update
from starlette.datastructures import UploadFile as StarletteUploadFile
from utils.email import EmailService, get_email_instance
from utils.http import HTTPClient, get_http_client_instance
from utils.processors import (
    hash_context,
    unconventional_terminate,
    validate_organization_existence,
    validate_transaction_mapping_exists,
    validate_user_existence,
)

from core.consensus import ConsensusMechanism
from core.constants import (
    ADDRESS_UUID_KEY_PREFIX,
    ASYNC_TARGET_LOOP,
    BLOCK_HASH_LENGTH,
    BLOCKCHAIN_BLOCK_TIMER_IN_SECONDS,
    BLOCKCHAIN_GENESIS_MAX_CHAR_DATA,
    BLOCKCHAIN_GENESIS_MIN_CHAR_DATA,
    BLOCKCHAIN_HASH_BLOCK_DIFFICULTY,
    BLOCKCHAIN_MINIMUM_TRANSACTIONS_TO_BLOCK,
    BLOCKCHAIN_NAME,
    BLOCKCHAIN_NEGOTIATION_ID_LENGTH,
    BLOCKCHAIN_RAW_PATH,
    BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS,
    BLOCKCHAIN_SECONDS_TO_MINE_FROM_ARCHIVAL_MINER,
    BLOCKCHAIN_TRANSACTION_COUNT_PER_NODE,
    BLOCKCHAIN_WAIT_TIME_REFRESH_FOR_TRANSACTION,
    INFINITE_TIMER,
    REF_MASTER_BLOCKCHAIN_ADDRESS,
    REF_MASTER_BLOCKCHAIN_PORT,
    USER_FILES_FOLDER_NAME,
    AddressUUID,
    AssociatedNodeStatus,
    BlockchainContentType,
    BlockchainFileContext,
    BlockchainIOAction,
    BlockchainPayload,
    ConsensusNegotiationStatus,
    HashUUID,
    HTTPQueueMethods,
    IdentityTokens,
    NodeTransactionInternalActions,
    NodeType,
    RandomUUID,
    RawBlockchainPayload,
    RawData,
    SourceNodeOrigin,
    TransactionActions,
    TransactionContextMappingType,
    URLAddress,
    UserEntity,
    random_generator,
)
from core.decorators import ensure_blockchain_ready, restrict_call
from core.dependencies import (
    generate_uuid_user,
    get_args_values,
    get_database_instance,
    get_identity_tokens,
    get_master_node_properties,
)

logger: Logger = getLogger(ASYNC_TARGET_LOOP)


class BlockchainMechanism(ConsensusMechanism):
    def __init__(
        self,
        *,
        block_timer_seconds: int,
        auth_tokens: IdentityTokens,
        node_role: NodeType,
    ) -> None:

        # # Containers
        self.confirming_block_container: list[
            Block
        ] = (
            []
        )  # * A container that contains generated blocks that were sent from the `ARCHIVAL_MINER_NODE`. It is used to verify the block given from the archival miner nodes, wherein specific attributes are being compared to ensure that the block received is not altered.
        self.hashed_block_container: list[
            Block
        ] = (
            []
        )  # * A container that contains hashed blocks from the `ARCHIVAL_MINER_NODE`. It is stored from this container to ensure that the order of blocks is properly managed.
        self.__transaction_container: list[
            Transaction
        ] = (
            []
        )  # * A container that contains a set of transactions that is going to be invoked from a generated block.
        self.__unsent_block_container: list[
            Block
        ] = (
            []
        )  # * A container that contains geenrated blocks that were unsuccessfully sent to the archival miner node candidates. It is being used only when there's a connection disruption between each other.

        # # Counters
        self.main_block_id: int = 1  # * The ID of the block that allocatable and appendable from the blockchain.
        self.leading_block_id: int = 0  # * The current block ID that is available to assign from a block. It initially refers to the value of `self.main_block_id`, wherein this leads to ensure that while the master node waits for `self.main_block_id` to return, it will render other blocks to avoid congestion.
        self.__cached_total_transactions: int = 0

        # # Instances
        self.__database_instance: Database = get_database_instance()
        self.__http_instance: HTTPClient = get_http_client_instance()
        self.__email_service: EmailService = get_email_instance()
        self.node_identity = auth_tokens  # - Equivalent to get_identity_tokens()

        # # Required Variables for the Blockchain Operaetion.
        self.node_role: NodeType = node_role
        self.__auth_token: IdentityTokens = auth_tokens

        # # Timer Containers
        self.block_timer_seconds: Final[int] = block_timer_seconds
        self.__hashing_duration: timedelta = timedelta(seconds=0)
        self.__consensus_sleep_date_expiration: datetime = datetime.now()

        # # State and Variable References
        self.blockchain_ready: bool = False  # * This bool property is used for determining if the blockchain is ready to take its request from its master or side nodes.
        self.__new_master_instance: bool = False  # * This bool property will be used whenever when the context of the blockchain file is empty or not. Sets to true when its empty.
        self.__node_ready: bool = False  # * This bool property is used for determining if this node is ready in terms of participating from the master node, this is where the consensus will be used.
        self.__sleeping_from_consensus: bool = False  # * This bool property is used for determining if the node is under consensus sleep or not. This property is used as a dependency to state whether the node is ready or is the blockchain for other operations.

        super().__init__(
            role=node_role,
            ref_database_instance=self.__database_instance,
            ref_http_instance=self.__http_instance,
            ref_node_identity_instance=self.node_identity,
        )

    async def initialize(self) -> None:
        """# A method that initialize resources needed for the blockchain system to work."""

        # - Load the blockchain for both nodes.
        self.__chain: frozendict = (
            await self.__process_blockchain_file_to_current_state(
                operation=BlockchainIOAction.TO_READ
            )
        )

        if self.node_role is NodeType.MASTER_NODE:
            if self.__new_master_instance:
                for _ in range(0, BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS):
                    await self.__create_genesis_block()  # * We can only afford to do per block since async will not detect other variable changes. I think we don't have a variable classifier that is meant to change dramatically without determined time. And that is 'volatile'.

                # @o When on initial instance, we need to handle the property for the blockchain system to run. Otherwise we just lock out the system even we already created.
                self.blockchain_ready = True
                self.__new_master_instance = False

                logger.info(
                    "Genesis block generation has been finished! Blockchain system ready."
                )

            else:
                self.blockchain_ready = True
                logger.info("Blockchain system is ready.")

            create_task(
                self.__block_timer_executor(),
                name=f"{BlockchainMechanism.__name__}_{self.node_role.name}_instance_{self.__block_timer_executor.__name__}",
            )

            print("final", self.__chain)

        else:
            if self.node_identity is not None:
                existing_certificate = await self._get_consensus_certificate()

                if not existing_certificate:
                    logger.warning(
                        f"Association certificate token does not exists! Fetching a certificate by establishing connection with the {NodeType.MASTER_NODE.name} blockchain."
                    )
                    while True:
                        consensus_establish_ref: float | None = await self.establish_node_certification()  # type: ignore # ! ConsensusMechanism has established this method.

                        if isinstance(consensus_establish_ref, float):
                            self.__consensus_calculate_sleep_time(
                                hashing_duration=consensus_establish_ref, add_on=True
                            )
                            break

                        logger.error(
                            f"Establishment to the {NodeType.MASTER_NODE.name} failed, cannot continue other blockchain operations, retrying after 10 seconds ..."
                        )
                        await sleep(10)

                else:
                    logger.info(
                        "Association certificate token exists. Ignoring establishment from the `MASTER_NODE`."
                    )

            logger.info(
                f"Running the update method to validate the local hash of the blockchain against the {NodeType.MASTER_NODE.name} blockchain."
            )

            # - We update the blockchain upstream.
            await self.__update_chain()

            # - And, we sleep initially. Bypassing this is impossible even on instance restart. The master node knows when's the time you are sleeping and when is not.
            # - Though, if there's a possibility that the archival miner node has started with delay, the master node respects that (by looking at the public/private state of this node).
            await self.__consensus_sleeping_phase()

    @restrict_call(on=NodeType.MASTER_NODE)
    async def insert_external_transaction(
        self,
        action: TransactionActions,
        from_address: AddressUUID,
        to_address: AddressUUID | None,
        data: GroupTransaction,
    ) -> HTTPException | None:
        """
        @o A method that is callable outside scope that can create a transaction as well as the entity from the database, if possible. It handles the content to render from the transaction as this will be used for content viewing later from the frontend.

        ### Args:
                * action (TransactionActions): An enum that describes the cause of instantiation of this transaction.
                * from_address (AddressUUID): A unique identifier that instantiated this transaction.
                * to_address (AddressUUID): A unique identifier that is being referred from the content of this transaction.
                * data (ApplicantLogTransaction | OrganizationTransaction | AdditionalContextTransaction): A pydantic model that is qualified for this method to work. Otherwise it will result in error.

        ### Returns:
                * bool: Returns `True` or `False` depending whether this function success or fails on execution of resolving the transaction for block minin.

        ### Note:
                * For `NodeTransactions`, it was already handled from the method `self._insert_transaction`. It doesn't need extra parameters since those contains internal actions that doesn't need extra handling as they were displayed on Explorer API.
        """

        # @o I don't know how to type this one.
        supported_models: Final[list[Any]] = [
            ApplicantLogTransaction,
            ApplicantUserTransaction,
            OrganizationUserBaseTransaction,
            AdditionalContextTransaction,
        ]

        # - Check if data is a pydantic model instance.
        # @o If data is an `instance` from one of the elements of `supported_structures` AND `action` provided is under the scope of `TransactionActions`. AND `from_address` as well as `to_address` contains something like a string. Proceed.
        if (
            any(isinstance(data.context, each_model) for each_model in supported_models)
            and action in TransactionActions
            and isinstance(from_address, str)
            and isinstance(to_address, str | None)
        ):

            # @o Declared to gather meesage and status regarding potential exception.
            exception_message: str | None = None  # * Reflects to log while sending the detail message from the HTTPException.
            exception_status: HTTPStatus | None = None

            # - [2] Verify if action (TransactionAction) to TransactionContextMappingType is viable.
            # # [4]

            # - For transactions that require generation of `user` under Organization or as an Applicant.
            if action in [
                TransactionActions.INSTITUTION_ORG_GENERATE_APPLICANT,
                TransactionActions.ORGANIZATION_USER_REGISTER,
            ] and (
                isinstance(
                    data.context,
                    ApplicantUserTransaction | OrganizationUserTransaction,
                )
            ):
                # @d While we do understand that exposing the context as a whole, specifically with the credentials involved, it is going to be a huge loophole.
                # @d With that, we need to seperate this transaction with `Internal` and `External`.

                # ! Where,
                # @o XXXInternal -> Contains fields that is classified as credentials.
                # @o XXXExternal -> Contains fields that does not contain anything sensitive as it only describes something out of context.

                # @o Since `XXXInternal` subclasses `XXXExternal`, we only need `Internal` and break down until we get to the `XXXExternal`.

                # #  ADD CONDITION FOR TRANSACTION MAPPING.

                # - Validate conditions before user generation.
                # - Validate if there's an existing association/organzization for the new applicant to refer.

                # @d Type-hints.
                association_referred: bool = False

                validate_user: bool
                existing_association: Mapping | None
                # - Validate the existence of the user based on the sensitive information.
                # ! I cannot deduce this and combine its functionality from the method `validate_source_and_origin_associates.` since that method focuses on validating the address and the token given by the sender.

                if to_address is not None:
                    exception_message = f"Target address should not exist for creating new applicants as well as creating a new organization user."
                    exception_status = HTTPStatus.NOT_ACCEPTABLE

                else:

                    # - Validate if this user already exists.
                    validate_user = await validate_user_existence(
                        user_identity=AgnosticCredentialValidator(
                            first_name=data.context.first_name,
                            last_name=data.context.last_name,
                            username=data.context.username,
                            email=data.context.email,
                        )
                    )

                    if validate_user:
                        exception_message = "There was an existing user from the credentials given! Please try with another credentials. Or contact your administration regarding your credentails."
                        exception_status = HTTPStatus.CONFLICT

                    else:

                        # - Validate the existence of an associate/organization.
                        # ! This maybe the same as from the method `validate_source_and_origin_associates` but that method is focused on validating the source and the target via address and token.
                        # * Plus, an API endpoint for registration runs on this scope.

                        # @o Observe there's a multiple `isinstance`.
                        # @o For the `OrganizationUserTransacion`, we need both of the arguments.
                        # @o However, in the case of ApplicantUserTransaction`, we only need the institution reference.

                        # # Note regarding repetitive declaration of `association_address` and `institution`.
                        # @context `assocation_address` exists due to its nature of other variables required upon registration with a new organization. Incorporating `institution` and along with other variables `associate_` indicates descrepancy between what's existing and what's not.
                        # @context Even though it was a design issue, I insists it, because again, there's an entity that still wasn't in the database and what's not.

                        # @o `association_address` is used for when there's a temporary reference that needs to be validated, and there's an `institution` that indicates reference that are resolved/validated.
                        existing_association = await validate_organization_existence(
                            org_identity=OrganizationIdentityValidator(
                                association_address=data.context.association_address if isinstance(data.context, OrganizationUserTransaction) else from_address,  # type: ignore # * We cannot use the field `inserter` on the payload because the `from_address` was already resolved before executing this method.
                                association_name=data.context.association_name
                                if isinstance(data.context, OrganizationUserTransaction)
                                else None,
                                association_group_type=data.context.association_group_type
                                if isinstance(data.context, OrganizationUserTransaction)
                                else None,
                            ),
                            scoped_to_applicants=isinstance(
                                data.context, ApplicantUserTransaction
                            ),
                        )

                        if (
                            action is TransactionActions.ORGANIZATION_USER_REGISTER
                            and isinstance(data.context, OrganizationUserTransaction)
                        ):

                            # - For the case of registering with the associate/organization, sometimes user can register with associate/organization reference existing and otherwise.
                            # - With that, we need to handle the part where if the associate/organization doesn't exist then create a new one. Otherwise, refer its self from that associate/organization.

                            # - Condition for creating a new associate/organization wherein there's no referrable address.
                            if (
                                data.context.association_address is None
                                and data.context.association_group_type is not None
                                and data.context.association_name is not None
                                and existing_association is None
                            ):
                                generated_org_address: Final[AddressUUID] = AddressUUID(
                                    f"{ADDRESS_UUID_KEY_PREFIX}:{uuid4().hex}"
                                )

                                # - Create an associate/organization when name is only provided assuming its a new instance.
                                new_association_query: Insert = (
                                    associations.insert().values(
                                        address=generated_org_address,
                                        name=data.context.association_name,
                                        group=data.context.association_group_type,
                                    )
                                )
                                await self.__database_instance.execute(
                                    new_association_query
                                )

                                data.context.association_address = generated_org_address  # type: ignore
                                data.context.institution = data.context.association_address  # type: ignore

                            # - Condition for assigning a user (that will be generated later) from this address.
                            elif (
                                data.context.association_address is not None
                                and data.context.association_group_type is None
                                and data.context.association_name is None
                                and existing_association is not None
                            ):
                                association_referred = True  # * We need this to avoid polluting blockchain content as a receipt.
                            else:
                                exception_message = "The supplied parameter for the `association` address reference does not exist or the payload contains a certain fields that shouldn't exist based on condition."
                                exception_status = HTTPStatus.NOT_FOUND

                                # ! To avoid complexity, just return here instead of going outer scope which is difficult.
                                return HTTPException(
                                    detail=exception_message,
                                    status_code=exception_status,
                                )
                        else:
                            # * Since we already resolved the `source_address`, assign the `inserter` referring to the source address of the payload.
                            data.context.institution = existing_association  # type: ignore
                            data.context.inserter = from_address  # type: ignore

                        # # Note regarding multiple type: ignore comments.
                        # @o The reason for this is to remove unnecessary errors regarding restructuring a model.
                        # @o I can solve it by re-implementing the use resolve variables but the problem here is that, this is the only case (condition) where `<nothing>` appears. I can't burn more time for that.

                        # * Resolve temporary variables and retain it old reference for other methods to resolve against.

                        # - When all of the checks are done, then create the user.
                        try:
                            new_uuid: AddressUUID = AddressUUID(generate_uuid_user())
                            insert_user_query: Insert = users.insert().values(
                                unique_address=new_uuid,
                                avatar=None,
                                description=data.context.description,
                                skills=data.context.skills
                                if isinstance(data.context, ApplicantUserTransaction)
                                else None,
                                first_name=data.context.first_name,  # type: ignore
                                last_name=data.context.last_name,  # type: ignore
                                association=data.context.institution,  # type: ignore
                                username=data.context.username,  # type: ignore
                                password=hash_context(pwd=RawData(data.context.password)),  # type: ignore
                                email=data.context.email,  # type: ignore
                                type=UserEntity.ORGANIZATION_DASHBOARD_USER
                                if isinstance(data.context, OrganizationUserTransaction)
                                else UserEntity.APPLICANT_DASHBOARD_USER,
                            )

                            # ! Since this query contains None for `to_address` we need to fill it because the method `resolve_transaction_context` needs it.
                            await self.__database_instance.execute(insert_user_query)

                            # * Resolve fields with missing data.
                            to_address = new_uuid
                            data.context.identity = new_uuid  # type: ignore

                            create_task(
                                self.__email_service.send(
                                    content=f"<html><body><h1>Hello from Folioblocks::Users!</h1><p>Thank you for registering as a <b>`{UserEntity.ORGANIZATION_DASHBOARD_USER.value if isinstance(data.context, OrganizationUserTransaction) else UserEntity.APPLICANT_DASHBOARD_USER.value}`</b>!<br><br>Your Address: <b>{new_uuid}</b><br>Association Address: <b>{data.context.association_address if isinstance(data.context, OrganizationUserTransaction) else data.context.institution}</b><br><br>Remember, if you are a `<b><i>{UserEntity.APPLICANT_DASHBOARD_USER.value}</b></i>`, please be responsible on taking applications from all over the companies associated from the system. Take once and evaluate before proceeding to the next one.<br><br>For the `<b><i>{UserEntity.ORGANIZATION_DASHBOARD_USER.value}</b></i>` please be responsible as any data you insert cannot be modified as they are stored from blockchain. <br><br>Should any questions should be delivered from this email. Thank you and enjoy our service!</p><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",  # type: ignore
                                    subject="Hello from Folioblocks::Users!",
                                    to=data.context.email,  # type: ignore
                                ),
                                name=f"{get_email_instance.__name__}_send_register_welcome_user",
                            )

                        except IntegrityError as e:
                            exception_message = f"There was an error during account generation. This may likely be a cause of duplication or unique-ness issue. Please check your credentials and try again. | Info: {e}"
                            exception_status = HTTPStatus.INTERNAL_SERVER_ERROR

                        # - After all that, its time to resolve these context for the `External` model. (For the blockchain to record).

                        # - We need to resolve these models due to its contents containing more information regarding the user. We do not need those in the blockchain so we have deduce it by resolving it.
                        # ! There is a note regarding replace an existing model with a new one, causing multiple type: ignore, please check the note for more information.

                        if isinstance(data.context, ApplicantUserTransaction):
                            data.context = ApplicantUserBaseTransaction(
                                **data.context.dict()  # type: ignore
                            )

                        if isinstance(data.context, OrganizationUserTransaction):
                            if association_referred:
                                data.context = OrganizationUserBaseFields(
                                    **data.context.dict()
                                )
                            else:
                                data.context = OrganizationUserBaseTransaction(
                                    **data.context.dict()
                                )

                        print("FINAL PAYLOAD", data.context, data.context.dict())

            # - For the invocation of log for the Applicant under enum `ApplicantLogTransaction`.
            # @o This needs special handling due to the fact that it may contain an actual file.
            # ! There's a need of special handling from the API endpoint receiver due to its nature of using content-type: `multipart/form-data`. Therefore, this method expects to have an `ApplicantLogTransaction`.
            elif (
                action is TransactionActions.INSTITUTION_ORG_REFER_NEW_DOCUMENT
                and isinstance(data.context, ApplicantLogTransaction)
                and isinstance(to_address, str)
            ):
                if (
                    await validate_transaction_mapping_exists(
                        user_address=AddressUUID(to_address),
                        content_type=TransactionContextMappingType.APPLICANT_BASE,
                    )
                    is True
                ):

                    # - `fastapi.UploadFile` and `starlette.datastructures.StarletteUploadFile` is not the same. Even though we used `fastapi.UploadFile` for both schema and from the API, it gets derived to `starlette.datastructures.UploadFile`.
                    if isinstance(data.context.file, StarletteUploadFile):
                        # @o We combine the current time under isoformat string + given filename + referred user address in full length.

                        # ! We need to create our own key because we are going to access these files.
                        # * Since this project is under repository, we will keep it this way.
                        # * In actual real world, we ain't gonna be doing this.

                        # @o Create the key based from the Transaction Action (2 characters) + the user address (`target` or `to`), truncated the first 3 characters and the last 14 characters of the target address + datetime in custom format, please see the variable `current_date` below.
                        # # Documentation regarding custom format: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

                        timestamp: datetime = datetime.now()
                        current_date: str = timestamp.strftime(
                            "%y%m%d%H%M%S"
                        )  # @o datetime.now() produces "datetime.datetime(2022, 4, 16, 19, 45, 36, 724779)" and when called with datetime.now().isoformat() produces "2022-04-16T19:45:36.724779'", when we used datetime.now().strftime() with parameters "%y%m%d%H%M%S", will produce "'220416194536'"

                        encrypter_key: bytes = f"{str(action.value)}{to_address[3:-14]}{current_date}".encode(
                            "utf-8"
                        )

                        print("key", encrypter_key)
                        file_encrypter: Fernet = Fernet(
                            urlsafe_b64encode(encrypter_key)
                        )

                        user_file_storage_ref: Path = Path(USER_FILES_FOLDER_NAME)
                        temp_filename: str = f"{user_file_storage_ref}/{timestamp.isoformat()}{data.context.file.filename}{to_address}".replace(
                            ":", "_"
                        )

                        if (
                            not user_file_storage_ref.is_dir()
                            or not user_file_storage_ref.exists()
                        ):
                            logger.debug("User file storage not found. Creating it.")
                            user_file_storage_ref.mkdir()

                        async with aopen(
                            temp_filename,
                            "wb",
                        ) as file_writer:
                            raw_context: bytes | str = await data.context.file.read()
                            encrypted_context: bytes = file_encrypter.encrypt(
                                raw_context.encode("utf-8")
                                if isinstance(raw_context, str)
                                else raw_context
                            )

                            await file_writer.write(encrypted_context)

                        # - Since we got the file and encrypted it, get the SHA256 of the payload.
                        # - And replace it on the field of the `data.context.file` so that we will get a reference when we refer from it.
                        data.context.file = HashUUID(
                            sha256(
                                raw_context.encode("utf-8")
                                if isinstance(raw_context, str)
                                else raw_context
                            ).hexdigest()
                        )

                        # - After hashing, rename the file to the hash so that it can be referred later.
                        try:
                            Path(temp_filename).rename(
                                f"{user_file_storage_ref}/{to_address[3:]}{data.context.file}"
                            )

                        # - Even though Path.rename() overrides file, in windows, it does not. Therefore resolve by replacing that file before attempting to rename it.
                        except FileExistsError:
                            Path(temp_filename).replace(
                                f"{user_file_storage_ref}/{data.context.file}"
                            )

                else:
                    exception_message = f"Cannot find transaction map for the address {to_address} with the content type {TransactionContextMappingType.APPLICANT_BASE}."

            # - For the `extra` fields of both `ApplicantTransaction` and `OrganizationTransaction`.
            # # [2]
            elif action in [
                TransactionActions.ORGANIZATION_REFER_EXTRA_INFO,
                TransactionActions.INSTITUTION_ORG_APPLICANT_REFER_EXTRA_INFO,
            ] and isinstance(data.context, AdditionalContextTransaction):

                # - Why?
                # @o We only need to verify the addresses contents, which was done from the API endpoint, there's nothing much going on in the case of `TransactionActions`.
                logger.debug(
                    f"Accepted at {TransactionActions.ORGANIZATION_REFER_EXTRA_INFO} or {TransactionActions.INSTITUTION_ORG_APPLICANT_REFER_EXTRA_INFO} by doing nothing due to there's nothing to process."
                )

            else:
                exception_message = "All of the condition specified did not hit. Are you sure your combination of data is right? Please check the declaration and try again."
                exception_status = HTTPStatus.INTERNAL_SERVER_ERROR

            if not isinstance(exception_message, str) and not isinstance(
                exception_status, HTTPStatus
            ):

                # - To ensure that this method will be processed the same way as `NodeTransaction`, we need to create a `GroupTransaction` for this.
                transaction_context: dict | HTTPException = (
                    await self.__resolve_transaction_payload(
                        action=action,
                        from_address=from_address,
                        to_address=to_address,
                        payload=data,
                        is_internal_payload=False,
                    )
                )

                # * Append the transaction mapping here.
                if not isinstance(transaction_context, HTTPException):
                    insert_transaction_content_map_query: Insert = (
                        tx_content_mappings.insert().values(
                            address_ref=to_address,
                            block_no_ref=self.leading_block_id,
                            tx_ref=transaction_context["tx_hash"],
                            content_type=data.content_type,
                            timestamp=datetime.now(),
                        )
                    )

                    await self.__database_instance.execute(
                        insert_transaction_content_map_query
                    )

                    return None

                else:
                    # - We cannot raise the `HTTPException` yet, store its contents and raise it later.
                    exception_message = transaction_context.detail
                    exception_status = HTTPStatus(transaction_context.status_code)

                get_from_address_email_query: Select = select([users.c.email]).where(
                    users.c.unique_address == from_address
                )

                from_address_email = await self.__database_instance.fetch_val(
                    get_from_address_email_query
                )

                if from_address_email is not None and data.content_type is not None:
                    create_task(
                        self.__email_service.send(
                            content=f"<html><body><h1>Notification from Folioblocks!</h1><p>There was an error from your inputs. The transaction regarding {data.content_type.name} has been disregarded. Please try your actions again.</p><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
                            subject="Error Transaction from Folioblock!",
                            to=EmailStr(from_address_email),  # type: ignore
                        ),
                        name="send_email_invalid_address_notification",
                    )
                    exception_message = "There was an error on processing this request. `from_address` exists which was able to be contacted through."
                    exception_status = HTTPStatus.INTERNAL_SERVER_ERROR
                else:
                    exception_message = "There was an error on processing this request. `from_address` exists but fails to contact them via email."
                    exception_status = HTTPStatus.INTERNAL_SERVER_ERROR

            else:
                return HTTPException(
                    detail=exception_message,
                    status_code=exception_status
                    if isinstance(exception_status, HTTPStatus)
                    else HTTPStatus.INTERNAL_SERVER_ERROR,
                )

            logger.critical(exception_message)
            return HTTPException(detail=exception_message, status_code=exception_status)

        else:
            exception_message = f"{'Sender' if from_address is None else 'Receiver'} address seem to be invalid. Please check your input and try again. This transaction will be disregarded. also, there was a missing or invalid value inserted from the following parameters: `action`, `from_address` and `data`. `action` requires to have a value of an Enum `{TransactionActions}`, `from_address` should contain a valid {str} and `data` should be wrapped in a pydantic model ({BaseModel})! Please encapsulate your `data` to one of the following pydantic models: {[each_model.__name__ for each_model in supported_models]}."
            exception_status = HTTPStatus.UNPROCESSABLE_ENTITY

        return HTTPException(detail=exception_message, status_code=exception_status)

    @restrict_call(on=NodeType.MASTER_NODE)
    async def insert_internal_transaction(
        self, action: TransactionActions, data: NodeTransaction
    ) -> None:

        if not isinstance(data, NodeTransaction) or action not in TransactionActions:
            logger.error(
                f"Parameters for the `action` and `data` is invalid. Please ensure that `data` is instance of `{NodeTransaction}` and `action` has an enum member candidate to `{TransactionActions}`"
            )
            return None

        # @o Since we can see some patterns for the Node-based Transaction's Enum Members (TransactionActions), instead of explicitly declaring them, we are going to use classify them by matching their prefixes.
        if not action.name.startswith("NODE_GENERAL_"):
            logger.error(
                "The parameter `action` is invalid. Please invoke `TransactionActions` with enum members prefixes starts with `NODE_GENERAL_`."
            )
            return None

        # - Resolve addresses.
        resolved_from_address: str
        resolved_to_address: str | None

        # - Resolve `from_address` as well as the `to_address`.
        if isinstance(data.context, NodeRegisterTransaction):
            resolved_from_address, resolved_to_address = (
                data.context.new_address,
                data.context.acceptor_address,
            )

        elif isinstance(data.context, NodeGenesisTransaction):
            # ! Even though we know that it would be the instance, respecfully respect the model variable xd.
            resolved_from_address, resolved_to_address = (
                data.context.generator_address,
                None,
            )

        elif isinstance(data.context, NodeCertificateTransaction | NodeSyncTransaction):
            resolved_from_address, resolved_to_address = (
                self.node_identity[0],
                data.context.requestor_address,
            )

        elif isinstance(data.context, NodeConfirmMineConsensusTransaction):
            resolved_from_address, resolved_to_address = (
                data.context.master_address,
                data.context.miner_address,
            )

        elif isinstance(data.context, NodeMineConsensusSuccessProofTransaction):
            resolved_from_address, resolved_to_address = (
                data.context.receiver_address,
                data.context.miner_address,
            )

        else:
            resolved_from_address, resolved_to_address = self.node_identity[0], None

        if await self.__resolve_transaction_payload(
            action=action,
            from_address=AddressUUID(
                resolved_to_address
                if resolved_to_address is not None
                else self.node_identity[0]
            ),
            to_address=AddressUUID(resolved_from_address),
            is_internal_payload=True,
            payload=data,
        ):
            return

        unconventional_terminate(message="Cannot resolve transaction.")

    @ensure_blockchain_ready()
    def get_blockchain_public_state(self) -> NodeMasterInformation | None:
        if self.node_role is NodeType.MASTER_NODE:

            # # This may not be okay.
            return NodeMasterInformation(
                chain_block_timer=self.block_timer_seconds,
                total_blocks=len(self.__chain["chain"])
                if self.__chain is not None
                else 0,
                total_transactions=self.__cached_total_transactions,
            )
        logger.warning(
            f"This client node requests for the `public_state` when their role is {self.node_role.name}! | Expects: {NodeType.MASTER_NODE.name}."
        )
        return None

    @ensure_blockchain_ready()
    def get_blockchain_private_state(self) -> NodeConsensusInformation:
        last_block: Block | None = self.__get_last_block()

        return NodeConsensusInformation(
            consensus_timer_expiration=self.__consensus_sleep_date_expiration,
            is_hashing=not self.blockchain_ready,
            is_sleeping=self.__node_ready and self.blockchain_ready,
            last_mined_block=last_block.id if last_block is not None else 0,
            node_role=self.node_role,
            owner=self.__auth_token[0],
        )

    async def get_chain_hash(self) -> HashUUID:
        fetch_chain_hash_query = select([file_signatures.c.hash_signature]).where(
            file_signatures.c.filename == BLOCKCHAIN_NAME
        )

        return HashUUID(
            await self.__database_instance.fetch_val(fetch_chain_hash_query)
        )

    async def get_chain(self) -> str:
        # At this state of the system, the blockchain file is currently unlocked. Therefore give it.

        # Adjust function for forcing to save new data when fetched.
        async with aopen(BLOCKCHAIN_NAME, "r") as chain_reader:
            data: str = await chain_reader.read()

        return data

    @restrict_call(on=NodeType.ARCHIVAL_MINER_NODE)
    async def hash_and_store_given_block(
        self,
        *,
        block: Block,
        from_origin: SourceNodeOrigin,
        master_address_ref: AddressUUID | None = None,
    ) -> None:
        if from_origin is not SourceNodeOrigin.FROM_MASTER and (
            master_address_ref is None or not isinstance(master_address_ref, str)
        ):
            logger.error(
                f"The provided value for the parameters seem to be invalid. This is an implementation-error, please contact the administration regarding this issue."
            )
            return None

        logger.warning(
            f"Waiting for {BLOCKCHAIN_SECONDS_TO_MINE_FROM_ARCHIVAL_MINER} seconds to consume all necessary requests from the {NodeType.MASTER_NODE} API-side before deadlocking-self to hash the block."
        )
        await sleep(BLOCKCHAIN_SECONDS_TO_MINE_FROM_ARCHIVAL_MINER)

        mined_block: Block | None = await self.__hash_block_processor(
            block=block, return_hashed=True
        )

        if not isinstance(mined_block, Block):
            logger.info(
                f"Block given is {type(mined_block)} This should not occur as a {self.node_role.name}, please contact the developer regarding this issue."
            )
            return None

        logger.info(
            f"Block #{block.id} is detected as a payload delivery for the consensus of being selected with the condition of sleep expiration. (Proof-of-Elapsed-Time) from the `{NodeType.MASTER_NODE.name}`. Sending back the hashed/mined block."
        )

        parsed_args: Namespace = get_args_values()
        master_origin_source_host, master_origin_source_port = (
            parsed_args.target_host,
            parsed_args.target_port,
        )

        recorded_consensus_negotiation_query: Select = select(
            [consensus_negotiation.c.consensus_negotiation_id]
        ).where(
            (consensus_negotiation.c.block_no_ref == mined_block.id)
            & (consensus_negotiation.c.peer_address == master_address_ref)
        )

        recorded_consensus_negotiation = await self.__database_instance.fetch_one(
            recorded_consensus_negotiation_query
        )

        if recorded_consensus_negotiation is not None:
            self.__consensus_sleep_date_expiration = (
                datetime.now() + self.__hashing_duration
            )

            payload_to_master: ClientResponse = await self.__http_instance.enqueue_request(
                url=URLAddress(
                    f"{master_origin_source_host}:{master_origin_source_port}/node/receive_hashed_block"
                ),
                method=HTTPQueueMethods.POST,
                headers={
                    "x-certificate-token": await self._get_consensus_certificate(),
                    "x-token": self.node_identity[1],
                },
                data={
                    "consensus_negotiation_id": recorded_consensus_negotiation.consensus_negotiation_id,  # type: ignore # - For some reason it doesn't detect the mapping.
                    "miner_address": self.node_identity[0],
                    "block": import_raw_json_to_dict(
                        export_to_json(mined_block.dict())
                    ),
                    "consensus_sleep_expiration": self.__consensus_sleep_date_expiration.isoformat(),
                },
                retry_attempts=100,
                name=f"send_hashed_payload_at_{NodeType.MASTER_NODE.name.lower()}_block_{mined_block.id}",
            )

            if payload_to_master.ok:
                payload_master_response_ref = ConsensusSuccessPayload(
                    **await payload_to_master.json()
                )
                # - Update the Consensus Negotiation ID.
                update_completed_consensus_negotiation_query: Update = (
                    consensus_negotiation.update()
                    .where(
                        (
                            consensus_negotiation.c.consensus_negotiation_id
                            == recorded_consensus_negotiation.consensus_negotiation_id  # type: ignore
                        )
                        & (
                            consensus_negotiation.c.status
                            == ConsensusNegotiationStatus.COMPLETED
                        )
                    )
                    .values(status=ConsensusNegotiationStatus.COMPLETED)
                )

                await get_database_instance().execute(
                    update_completed_consensus_negotiation_query
                )

                logger.info(f"Consensus Negotiation ID {recorded_consensus_negotiation.consensus_negotiation_id} with the peer (receiver) address {master_address_ref} has been labelled as {ConsensusNegotiationStatus.COMPLETED.name}!")  # type: ignore

                # - Sum the mined_timer sleep phase + given random sleep timer.
                self.__consensus_calculate_sleep_time(
                    hashing_duration=payload_master_response_ref.addon_consensus_sleep_seconds,
                    add_on=True,
                )

                # - Run the consensus sleeping phase.
                await self.__consensus_sleeping_phase()

            else:
                if payload_to_master.status == HTTPStatus.INTERNAL_SERVER_ERROR:
                    logger.critical(
                        "There was an error from the server regarding block processing. This is probably a master server-side issue. Please report to the administrator to get this fixed."
                    )
                else:
                    logger.error(
                        "There was an unexpected error from keeping this request to be sent or received from other server. This may be an unidentifable cause of an issue. This may stop the service, please try again."
                    )
                    return None
        else:
            logger.error(
                f"There were no recorded negotiation from the Block ID {block.id} with the peer address {master_address_ref}. This is a developer-issue regarding logic error. Please report to them as possible to fix."
            )
            return None

    # # This method may be modified for the development of Explorer API.
    @ensure_blockchain_ready()
    async def preview_blocks(self, limit_to: int) -> list[BlockOverview] | None:
        if self.__chain is not None:
            candidate_blocks: list[BlockOverview] = deepcopy(
                self.__chain["chain"][len(self.__chain["chain"]) - limit_to :]
            )
            resolved_candidate_blocks: list[BlockOverview] | list = []

            for block in candidate_blocks:
                parsed_block: dict = dict(block)
                # - [1] Push validator outside.
                parsed_block["validator"] = parsed_block["contents"]["validator"]

                # -  [2] Remove the contents scope.
                del parsed_block["contents"]

                # - [3] Remove hash context.
                del parsed_block["hash_block"]
                del parsed_block["prev_hash_block"]

                # - [4] Assign this to the indexed block.
                resolved_candidate_blocks.append(BlockOverview.parse_obj(parsed_block))

            # * Once done, return the list.
            resolved_candidate_blocks.reverse()
            return resolved_candidate_blocks

        return None

    # # This method may be modified for the development of Explorer API.
    @ensure_blockchain_ready()
    async def preview_transactions(self, limit_to: int) -> list[Transaction] | None:
        if self.__chain is not None:
            pass

    async def append_block(self, *, context: Block, follow_up: bool) -> None:
        """
        A method that is callad whenever a new block is ready to be inserted from the blockchain, both in-memory and to the file.

        Args:
                context (Block | Transaction): The context of the block as is.
                auth_context (IdentityTokens): Authentication attribute, not sure what to do on this one yet.

        TODO
        * Implement security of some sort, use `auth_context` or something. | We may use this and compute its hash for comparing context and also length.
        """
        if self.__chain is not None:
            block_context: dict = context.dict()
            block_context["contents"] = frozendict(block_context["contents"])

            # @o If a certain block has been inserted in a way that it is way over far or less than the current self.cached_block_id, then disregard this block.
            if block_context["id"] != self.main_block_id:
                logger.error(
                    f"This block #{block_context['id']} is way too far or behind than the one that is saved in the local blockchain file. Will attempt to fetch a new blockchain file from the MASTER_NODE node. This block will be DISREGARDED."
                )
                return

            # - Apply immutability on other `dict` objects from the block context.
            # @o As per the approach indicated from the `self.__process_serialize_to_blockchain_file`. We are going to do this in descending form.

            if len(block_context["contents"]["transactions"]):

                # # Iteration method is the same as from the method `self.__process_deserialize_to_load_blockchain_in_memory'.
                # @o I cannot DRY this one out due to its nature of the condition.
                # @o Also to reduce the fatigue of going through method after method, I will retain this one since it is confusing to read, it needs the context as a whole or otherwise it will be disregarded.
                for transaction_idx, transaction_data in enumerate(
                    block_context["contents"]["transactions"]
                ):

                    # - [1] Apply immutability on the transactions -> `payload`
                    block_context["contents"]["transactions"][transaction_idx][
                        "payload"
                    ] = frozendict(transaction_data["payload"])

                    # - [2] Apply immutability on the transactions -> `signatures`
                    block_context["contents"]["transactions"][transaction_idx][
                        "signatures"
                    ] = frozendict(transaction_data["signatures"])

                    # - [3] Apply immutability on the transaction/s set.
                    block_context["contents"]["transactions"][
                        transaction_idx
                    ] = frozendict(transaction_data)

                    # @o Increment transaction by one as it was loaded in memory.
                    self.__cached_total_transactions += 1

                # - [4] Apply immutability on the contents, contaning a set of transaction/s.
                block_context["contents"] = frozendict(block_context["contents"])

            # - [5] Apply immutability from the whole block and then append it.
            self.__chain["chain"].append(frozendict(block_context))

            # ! Hit the next block for the allocation as we finished processing a block!
            self.main_block_id += 1

            await self.__process_blockchain_file_to_current_state(
                operation=BlockchainIOAction.TO_WRITE
            )
            logger.info(f"Block #{context.id} has been appended from the blockchain!")

            # - The way this was handled may turn this method into a recursive method, but we will stop it with a `follow_up` switch, preventing it to run this method, call-after-call.
            if len(self.hashed_block_container) and follow_up:
                logger.info(
                    f"Detected a {len(self.hashed_block_container)} hashed block/s from the container."
                )

                for each_hashed_block in self.hashed_block_container:
                    if each_hashed_block.id == self.main_block_id:
                        logger.info(
                            f"Follow-up appending block #{each_hashed_block} from the chain ..."
                        )
                        await self.append_block(
                            context=each_hashed_block, follow_up=True
                        )

                logger.info("Follow-up chaining is finished!")

        else:
            unconventional_terminate(
                message="There's no 'chain' from the root dictionary of blockchain! This is a developer-implementation issue, please report to the developers as soon as possible!",
            )

    @restrict_call(on=NodeType.MASTER_NODE)
    async def __block_timer_executor(self) -> None:
        logger.info(
            f"Block timer has been executed. Refreshes at {self.block_timer_seconds} seconds."
        )

        while True:
            logger.warning(
                f"Sleeping for {self.block_timer_seconds} seconds while collecting real-time transactions."
            )

            # - Sleep first due to block timer.
            await sleep(self.block_timer_seconds)

            # - Queue for other (`ARCHIVAL_MINER_NODE`) nodes to see who can hash the block.
            available_node_info: tuple[
                int, ArchivalMinerNodeInformation
            ] | None = await self.__get_available_archival_miner_nodes()

            # @o When there's no miner active, sleep for a while and requeue again.
            if available_node_info is None:
                continue

            # @o Added for type-hints.
            generated_block: Block | None = None

            # @o When there's a miner, do a closed-loop process.

            # @o To save some processing time, we need to have a sufficient transactions before we process them to a block.
            # - Wait until a number of sufficient transactions were received.
            # - Since we already have a node, do not let this one go.

            required_transactions: int = (
                BLOCKCHAIN_MINIMUM_TRANSACTIONS_TO_BLOCK
                if not available_node_info[0]
                else (
                    BLOCKCHAIN_MINIMUM_TRANSACTIONS_TO_BLOCK
                    + (available_node_info[0] * BLOCKCHAIN_TRANSACTION_COUNT_PER_NODE)
                )
            )

            if (len(self.__transaction_container) >= required_transactions) and not len(
                self.__unsent_block_container
            ):
                logger.info(
                    f"Number of required transactions were sufficient! There are {len(self.__transaction_container)} transactions that will be converted to a block for processing."
                )

                # - Create a block from all of the transactions.
                generated_block = await self.__create_block()

            elif len(self.__unsent_block_container):
                logger.info(
                    f"Block {self.__unsent_block_container[0]} has been left-out from hashing due to previous miner unable to respond in time. Using this block for the hashing process instead."
                )

                generated_block = self.__unsent_block_container.pop(0)

            else:
                logger.warning(
                    f"There isn't enough transactions to create a block (currently have {len(self.__transaction_container)} transaction/s, requires {required_transactions} transaction/s). Awaiting for new transactions in {BLOCKCHAIN_WAIT_TIME_REFRESH_FOR_TRANSACTION} seconds."
                )

                await sleep(BLOCKCHAIN_WAIT_TIME_REFRESH_FOR_TRANSACTION)
                continue

            # - Create a Consensus Negotiation ID out of `urlsafe_b64encode`.
            # @o Create a Consensus Negotiation ID for the nodes to remember that this happened.
            # @o Even though we already have the certification token, we still need this one to track current negotiations between nodes.

            if generated_block is not None:
                generated_consensus_negotiation_id: str = token_urlsafe(
                    BLOCKCHAIN_NEGOTIATION_ID_LENGTH
                )

                attempt_deliver_payload: ClientResponse = await self.__http_instance.enqueue_request(
                    url=URLAddress(
                        f"{available_node_info[1].source_host}:{available_node_info[1].source_port}/node/receive_raw_block"
                    ),
                    method=HTTPQueueMethods.POST,
                    await_result_immediate=True,
                    headers={
                        "x-certificate-token": await self._get_consensus_certificate(
                            address_ref=available_node_info[1].miner_address
                        ),
                        "x-hash": await self.get_chain_hash(),
                        "x-token": self.node_identity[1],
                    },
                    data={
                        # - Load the dictionary version and export it via `orjson` and import it again to get dictionary for the aiohttp to process on request.
                        "block": import_raw_json_to_dict(
                            export_to_json(generated_block.dict())
                        ),
                        "master_address": self.node_identity[0],
                        "consensus_negotiation_id": generated_consensus_negotiation_id,
                    },
                    retry_attempts=100,
                    name=f"send_raw_payload_at_{NodeType.ARCHIVAL_MINER_NODE.name.lower()}_{available_node_info[1].miner_address[-6:]}",
                )

                if attempt_deliver_payload.ok:
                    # - Save this consensus negotiation ID as well for the retrieval verification of the hashed/mined block.
                    save_in_progress_negotiation_query: Insert = (
                        consensus_negotiation.insert().values(
                            block_no_ref=generated_block.id,
                            consensus_negotiation_id=generated_consensus_negotiation_id,
                            peer_address=self.node_identity[0],
                            status=ConsensusNegotiationStatus.ON_PROGRESS,
                        )
                    )

                    # - And remember that this node was in the state of `CURRENTLY_HASHING`.
                    set_miner_state_as_hashing_query: Update = (
                        associated_nodes.update()
                        .where(
                            associated_nodes.c.user_address
                            == available_node_info[1].miner_address
                        )
                        .values(status=AssociatedNodeStatus.CURRENTLY_HASHING)
                    )

                    await gather(
                        self.__database_instance.execute(
                            save_in_progress_negotiation_query
                        ),
                        self.__database_instance.execute(
                            set_miner_state_as_hashing_query
                        ),
                    )

                    # - Store this for a while for the verification upon receiving a hashed/mined block.
                    # @o We will be using this to refer from the hashed block that will be sent by a archival miner node.
                    self.confirming_block_container.append(generated_block)

                    # - And save the negotiation consensus where a block getting hashed has been confirmed.
                    # - Basically this transaction shows who won from hashing a block.
                    await self.insert_internal_transaction(
                        action=TransactionActions.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START,
                        data=NodeTransaction(
                            action=NodeTransactionInternalActions.CONSENSUS,
                            context=NodeConfirmMineConsensusTransaction(
                                consensus_negotiation_id=RandomUUID(
                                    generated_consensus_negotiation_id
                                ),
                                master_address=self.node_identity[0],
                                miner_address=available_node_info[1].miner_address,
                            ),
                        ),
                    )

                    logger.info(
                        f"Block {generated_block.id} has been sent and is in process of hashing! (By Miner Node: {available_node_info[1].miner_address})"
                    )
                    continue

                else:
                    logger.warning(
                        "After multiple retries, the generated block will be stored and will find other archival miner node candidate who doesn't disconnect."
                    )
                    self.__unsent_block_container.append(generated_block)

                    # * Have to eliminate the potential of colliding with other blocks.
                    self.__unsent_block_container.sort(
                        key=lambda block_context: block_context.id
                    )

                    continue

            logger.error(
                f"Cannot proceed when block generated returned {generated_block}!"
            )

    def __consensus_calculate_sleep_time(
        self, *, hashing_duration: int | float, add_on: bool
    ) -> None:

        if not self.__new_master_instance:

            if add_on:
                self.__hashing_duration += timedelta(seconds=hashing_duration)
            else:
                self.__hashing_duration = timedelta(seconds=hashing_duration)

            logger.info(f"Consensus sleep timer were set to {self.__hashing_duration}.")
            return

        logger.error("Unable to set the consensus timer.")

    async def __consensus_sleeping_phase(self) -> None:
        if not self.__new_master_instance:
            self.__sleeping_from_consensus = True

            logger.info(
                f"Sleeping for {self.__hashing_duration.total_seconds()} seconds. Waking up after {datetime.now() + self.__hashing_duration}."
            )

            await sleep(self.__hashing_duration.total_seconds())
            self.__sleeping_from_consensus = False

            # * When done, ensure that the node's sate is changed.
            self.__set_node_state()

            logger.info(
                "Woke up from the consensus timer! Ready to take blocks to hash."
            )
            return

        logger.info(
            f"Consensus timer ignored due to condition (ie. new instance, blockchain state not ready or otherwise."
        )

    async def __create_block(self) -> Block | None:
        # @o When building a block, we first have to consider that there are some properties were undefined. The nonce, block_size_bytes, and hash_block.
        # @o With this, we need to seperate the contents of the block, providing a way from the inside of the block to be hashable and identifiable for hash verification.
        # ! Several properties have to be seperated due to their nature of being able to overide the computed hash block.

        last_block: Block | None = self.__get_last_block()

        if last_block is not None:
            if last_block.id >= self.leading_block_id:
                logger.critical(
                    f"Cannot create a block! Last block is greater than or equal to the ID of the currently (leading) cached available-to-allocate block. | Last Block ID: {last_block.id} | Currently Cached: {self.main_block_id}"
                )
                return None
        else:
            logger.warning(
                f"This new block will be the first block from this blockchain."
            )

        shadow_transaction_container = deepcopy(self.__transaction_container)
        self.__transaction_container.clear()

        _block: Block = Block(
            id=self.leading_block_id,
            block_size_bytes=None,  # * To be resolved on the later process.
            hash_block=None,  # ! Unsolvable, mine_block will handle it.
            prev_hash_block=HashUUID(
                last_block.hash_block
                if last_block is not None and last_block.hash_block is not None
                else "0" * BLOCK_HASH_LENGTH
            ),
            contents=HashableBlock(
                nonce=None,  # - This was determined during the process of hashing.
                validator=self.node_identity[0],
                transactions=shadow_transaction_container,
                timestamp=datetime.now(),
            ),
        )

        _block.block_size_bytes = asizeof(_block.contents.json())

        logger.info(
            f"Block #{_block.id} with a size of ({_block.block_size_bytes} bytes) has been created."
        )

        return _block

    @restrict_call(on=NodeType.MASTER_NODE)
    async def __create_genesis_block(self) -> None:
        """
        Generates a block, hash it and append it within the context of the blockchain, for both the file and the in-memory.
        """

        # * Create a transaction for the generation of the genesis block.
        await self.insert_internal_transaction(
            action=TransactionActions.NODE_GENERAL_GENESIS_BLOCK_INIT,
            data=NodeTransaction(
                action=NodeTransactionInternalActions.INIT,
                context=NodeGenesisTransaction(
                    block_genesis_no=self.main_block_id,
                    data=HashUUID(
                        token_hex(
                            random_generator.randint(
                                BLOCKCHAIN_GENESIS_MIN_CHAR_DATA,
                                BLOCKCHAIN_GENESIS_MAX_CHAR_DATA,
                            )
                        )
                    ),
                    generator_address=self.node_identity[0],
                    time_initiated=datetime.now(),
                ),
            ),
        ),

        generated_block_w_genesis: Block | None = await self.__create_block()

        if isinstance(generated_block_w_genesis, Block):
            await self.__hash_block_processor(
                block=generated_block_w_genesis, return_hashed=False
            )
        else:
            logger.critical("There was an error while generating a genesis block.")

        return None

    async def __get_available_archival_miner_nodes(
        self,
    ) -> tuple[int, ArchivalMinerNodeInformation] | None:

        available_nodes_query = select(
            [
                associated_nodes.c.user_address,
                associated_nodes.c.source_address,
                associated_nodes.c.source_port,
            ]
        ).where(associated_nodes.c.status == AssociatedNodeStatus.CURRENTLY_AVAILABLE)

        available_nodes: list[Mapping] = await self.__database_instance.fetch_all(
            available_nodes_query
        )

        random_generator.shuffle(
            available_nodes
        )  # ! Note that this does not create a new copy of the referred object, but rather mutates the referred object!

        if not len(available_nodes):
            logger.info(
                f"There are no available nodes to hash the block. Retrying again the after interval of the block timer. ({self.block_timer_seconds} seconds)"
            )
            return None

        logger.info(f"{len(available_nodes)} Archival Miner Node Candidate/s found!")

        for candidate_idx, each_candidate in enumerate(available_nodes):
            try:
                candidate_response: ClientResponse = await self.__http_instance.enqueue_request(
                    url=URLAddress(
                        f"{each_candidate['source_address']}:{each_candidate['source_port']}/node/info"
                    ),
                    method=HTTPQueueMethods.GET,
                    await_result_immediate=True,
                    do_not_retry=True,
                    name=f"contact_archival_node_candidate_{each_candidate['user_address'][-6:]}",
                )

                if candidate_response.ok:
                    parsed_candidate_state_info = await candidate_response.json()
                    resolved_candidate_state_info = parsed_candidate_state_info[
                        "properties"
                    ]

                    logger.info(
                        f"Archival Miner Candidate {resolved_candidate_state_info['owner']} has responded from the block hashing request!"
                    )

                    last_selected_node_consensus_sleep_datetime_query: Select = select(
                        [associated_nodes.c.consensus_sleep_expiration]
                    ).where(
                        associated_nodes.c.user_address
                        == resolved_candidate_state_info["owner"]
                    )

                    # - Use backend time referene instead of relying from the archival miner instead.
                    # * This implementation is surely fool-proof.
                    selected_node_last_consensus_sleep_datetime = (
                        await self.__database_instance.fetch_one(
                            last_selected_node_consensus_sleep_datetime_query
                        )
                    )

                    # @o Type-hint.
                    resolved_last_consensus_sleep_datetime: datetime
                    if selected_node_last_consensus_sleep_datetime.consensus_sleep_expiration is None:  # type: ignore
                        resolved_last_consensus_sleep_datetime = datetime.now()
                    else:
                        resolved_last_consensus_sleep_datetime = (
                            selected_node_last_consensus_sleep_datetime.consensus_sleep_expiration  # type: ignore
                        )

                    if (
                        not resolved_candidate_state_info["is_hashing"]
                        and NodeType(resolved_candidate_state_info["node_role"])
                        is NodeType.ARCHIVAL_MINER_NODE
                        and (datetime.now() >= resolved_last_consensus_sleep_datetime)
                    ):
                        return (
                            len(available_nodes),
                            ArchivalMinerNodeInformation(
                                candidate_no=candidate_idx,
                                miner_address=resolved_candidate_state_info["owner"],
                                source_host=URLAddress(
                                    each_candidate["source_address"]
                                ),
                                source_port=each_candidate["source_port"],
                            ),
                        )  # type: ignore # * I don't know how to type this.

                    logger.warning(
                        f"Archival Miner Candidate {resolved_candidate_state_info['owner']} may be sleeping from consensus."
                    )

            except AttributeError:
                logger.error("An error occured in the middle of the process.")
                continue

        logger.warning(
            f"All archival miner nodes seem to be busy. Attempting to find available nodes after the interval of the block timer. ({self.block_timer_seconds} seconds)"
        )
        return None

    def __get_last_block(self) -> Block | None:
        # ! This return seems confusing but I have to sacrafice for my own sake of readability.
        # @o First we access the list by calling the key 'chain'.
        # @o Since we got to the list, we might wanna get the last block by slicing the list with the use of its own length - 1 to get the last block.
        # @o But before we do that, ensure that last item has a content. Accessing the last item with the use of index while it doesn't contain anything will result in `IndexError`.

        if len(self.__chain["chain"]):
            last_block_ref = Block.parse_obj(
                self.__chain["chain"][len(self.__chain["chain"]) - 1 :][0]
            )
            logger.debug(
                f"Last block has been fetched. Context | ID: {last_block_ref.id}, Hash: {last_block_ref.hash_block}, Date: {last_block_ref.contents.timestamp.isoformat()}"
            )

            return last_block_ref

        logger.warning("There's no block inside blockchain.")

    async def __get_content_data(
        self,
        *,
        data_type: BlockchainContentType,
        recently: bool = False,
        size: int = 5,
        content_id: str | None = None,
    ) -> None:

        # ! If we wanted to fetch everything then don't add size and put recently to False.

        return

    # # Cannot do keyword arguments here as per stated on excerpt: https://stackoverflow.com/questions/23946895/requests-in-asyncio-keyword-arguments
    async def __hash_block(self, block: Block) -> Block:
        # If success, then return the hash of the block based from the difficulty.
        self.blockchain_ready = False
        prev: float = time()
        nth: int = 1

        logger.info(f"Attempting to hash a Block #{block.id} ...")

        while True:
            # https://stackoverflow.com/questions/869229/why-is-looping-over-range-in-python-faster-than-using-a-while-loop, not sure if this works here as well.

            block.contents.nonce = random_generator.randint(0, MAX_INT_PYTHON)
            computed_hash: HashUUID = HashUUID(
                sha256(block.json().encode("utf-8")).hexdigest()
            )

            if (
                computed_hash[:BLOCKCHAIN_HASH_BLOCK_DIFFICULTY]
                == "0" * BLOCKCHAIN_HASH_BLOCK_DIFFICULTY
            ):
                block.hash_block = computed_hash
                logger.info(
                    f"Block #{block.id} with a nonce value of {block.contents.nonce} has a resulting hash value of `{computed_hash}`, which has been mined for {time() - prev} under {nth} iteration/s!"
                )
                self.__consensus_calculate_sleep_time(
                    hashing_duration=time() - prev, add_on=False
                )
                self.blockchain_ready = True
                return block

            nth += 1

    async def __hash_block_processor(
        self, *, block: Block, return_hashed: bool
    ) -> Block | None:
        block_hashing_processor = await (
            get_event_loop().run_in_executor(
                None,
                self.__hash_block,
                block,
            )
        )

        mined_block: Block = await block_hashing_processor

        logger.info(f"Block {block.id} has been mined.")
        await self.append_block(context=mined_block, follow_up=False)

        return mined_block if return_hashed else None

    # Overwrites existing buffer from the frozendict if consensus has been established.
    async def __process_blockchain_file_to_current_state(
        self,
        *,
        operation: BlockchainIOAction,
        context_from_update: BlockchainPayload | tuple = tuple(),
        bypass_from_update: bool = False,
    ) -> frozendict:  # type: ignore # ! Both final conditions return `frozendict` already.

        if operation not in BlockchainIOAction:
            unconventional_terminate(
                message=f"Supplied value at 'operation' is not a valid enum! Got {operation} ({type(operation)}) instead. This is an internal error.",
            )
            await sleep(INFINITE_TIMER)

        async with aopen(
            BLOCKCHAIN_RAW_PATH,
            "w" if operation is BlockchainIOAction.TO_WRITE else "r",
        ) as content_buffer:

            if operation is BlockchainIOAction.TO_WRITE:
                if not bypass_from_update and not len(context_from_update):
                    byte_json_content: bytes = export_to_json(
                        self.__chain,
                        default=self.__process_serialize_to_blockchain_file,
                    )

                    logger.debug(
                        f"Updating blockchain file's hash signature on database. | Targets: {BLOCKCHAIN_RAW_PATH}"
                    )
                    new_blockchain_hash: str = sha256(byte_json_content).hexdigest()

                    await self.__update_chain_hash(new_hash=new_blockchain_hash)
                    await content_buffer.write(byte_json_content.decode("utf-8"))

                    logger.debug(
                        f"Blockchain's file signature has been changed! | Current Hash: {new_blockchain_hash}"
                    )
                else:
                    logger.warning("Bypass from the update method has been declared.")
                    await self.__update_chain_hash(new_hash=context_from_update[0])
                    await content_buffer.write(context_from_update[1])

                return self.__chain

            else:
                raw_data = await content_buffer.read()
                partial_deserialized_data = import_raw_json_to_dict(raw_data)
                deserialized_data = (
                    self.__process_deserialize_to_load_blockchain_in_memory(
                        partial_deserialized_data
                    )
                )

                if deserialized_data is None:
                    unconventional_terminate(
                        message="Houston, we have a problem! We cannot deserialize from the JSON file. This is most likely someone modified the blockchain file! Please report this to the administrators and ensure that the backup has been added."
                    )  # * Resolves to condition 'deserialized_data is None'.
                    await sleep(INFINITE_TIMER)

                else:
                    logger.info(
                        f"Chain has been loaded from the file to the in-memory!"
                    )
                    return deserialized_data

    def __process_deserialize_to_load_blockchain_in_memory(
        self, context: RawBlockchainPayload, update: bool = False
    ) -> frozendict | None:
        """
        A method that deserializes the universally readable (JSON) format from the blockchain file into an immutable dictionary (frozendict) containing a series of pydantic objects.

        Args:
                context (dict[str, Any]): The consumable data (type-compatible) that is loaded by the orjson.

        Returns:
                frozendict: Returns the immutable version of the given `context`.
        """

        # - Check if there's a context inside of the JSON. If there's none then create a n of genesis blocks.
        # @o New instances is indicated when this node doesn't contain any blocks on load. To avoid consensus timer on new instance, we have this switch to ensure that new blocks on fetch has been processed. As well as not flagged itself as fraudalent when there is a missing amount of genesis blocks.

        self.__new_master_instance = (  # # Redundant condition checking but better.
            context is not None  # - [1] Check if the variable contains something.
            and "chain" in context  # - [2] And it contains a key named as 'chain'.
            and isinstance(
                context["chain"], list
            )  # - [3] 'chain' key contains a 'list' object.
            and not len(context["chain"])  # - [4] And it contains nothing.
        )

        # *  Ensure that the wrapped object is 'dict' regardless of their recent forms.
        if isinstance(context, dict):
            if update:
                self.__cached_total_transactions = 0  # ! This means that we are resetting count back to zero because we are loading a new blockchain file.

            required_genesis_blocks: int = BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS  # ! We need to validate that there should be a set of required gensis blocks. If there are insufficient, then this blockchain as a whole is fraudalent.

            for block_idx, block_data in enumerate(context["chain"]):
                genesis_transaction_identifier: bool = False  # ! Additional switch to identify at least one genesis transaction per block.

                # @o For every block, we have to deserialize (1) the block itself, (2) contents of the block, which contains the transactions, (3) the payload as well as the (4) the signatures of the transactions.
                # - We are going to do this in reverse. Since doing this in ascending would prohibit due to existing cast of `frozendict` to each field.

                # - Check if there's a transaction first.
                if len(context["chain"][block_idx]["contents"]["transactions"]):

                    # # Iteration method is the same as from the method `self._append_block'. Refer to that method for more information on why I can't DRY this.
                    for transaction_idx, each_transaction in enumerate(
                        block_data["contents"]["transactions"]
                    ):

                        # - We assume that this will turn into an Enum member.
                        if (
                            TransactionActions(
                                context["chain"][block_idx]["contents"]["transactions"][
                                    transaction_idx
                                ]["action"]
                            )
                            == TransactionActions.NODE_GENERAL_GENESIS_BLOCK_INIT
                        ):
                            genesis_transaction_identifier = True

                        # - Inside transaction, it contains another `dict` objects, such as the paload and signature.
                        # @o We need to cast that as well to ensure that there are no override ability for all types of objects.
                        context["chain"][block_idx]["contents"]["transactions"][
                            transaction_idx
                        ]["payload"] = frozendict(each_transaction["payload"])

                        context["chain"][block_idx]["contents"]["transactions"][
                            transaction_idx
                        ]["signatures"] = frozendict(each_transaction["signatures"])

                        # - When done on the set of transactions, cast the immutability of the whole `transaction`.
                        context["chain"][block_idx]["contents"]["transactions"][
                            transaction_idx
                        ] = frozendict(
                            block_data["contents"]["transactions"][transaction_idx]
                        )

                        self.__cached_total_transactions += 1

                # - Add immutability to the `contents`, which encapsulates the whole set of `transactions`.
                context["chain"][block_idx]["contents"] = frozendict(
                    block_data["contents"]
                )

                # - Then, make the whole block immutable and insert it as reference from the blockchain.
                context["chain"][block_idx] = frozendict(block_data)

                # - Additional Checking
                # @o Check backward reference from the current block to recent block.
                if block_idx:  # ! Mind the zero-based list access.
                    if (
                        block_data["prev_hash_block"]
                        != context["chain"][block_idx - 1]["hash_block"]
                    ):
                        logger.critical(
                            f"Block #{block_data['id']}'s backward reference to Block #{block_data['id'] - 1} is invalid! | Expects (from Current Block): {block_data['hash_block']}, got {context['chain'][block_idx - 1]['prev_hash_block']} instead."
                        )

                        logger.critical(
                            "Due to potential fraudalent local blockchain file, please wait for the `MASTER_NODE` node to acknowledge your replacement of blockchain file."
                        )
                        self.blockchain_ready = False

                        # # Create a task that waits for it to do something to fetch a valid blockchain file.

                    logger.info(
                        f"Block #{block_data['id']} backward reference to Block# {block_data['id'] - 1} is valid!"
                    )
                else:
                    logger.debug(
                        f"Block #{block_data['id']} doesn't have a prev or leading block to compare reference, probably the latest block."
                    )
                    print(
                        block_data["prev_hash_block"],
                        context["chain"][block_idx - 1]["hash_block"],
                    )

                # - If cached_block_id is equal to dict_data["id"]. Then increment it easily.
                if self.main_block_id == block_data["id"]:
                    self.main_block_id += 1
                    logger.debug(
                        f"Block has a valid recent reference. | Currently (Incremented) Cached ID: {self.main_block_id}, Recent Block ID (Decremented by 1): {block_data['id']}"
                    )

                # - However, when its not equal then then something is wrong.
                else:
                    unconventional_terminate(
                        message=f"Blockchain is currently unchained! (Currently Cached: {self.main_block_id} | Block ID: {block_data['id']}) Some blocks are missing or is modified. This a developer-issue.",
                    )
                    return None

                if genesis_transaction_identifier and required_genesis_blocks:
                    required_genesis_blocks -= 1

            if (
                required_genesis_blocks
                and self.node_role is NodeType.MASTER_NODE
                and not self.__new_master_instance
            ):
                unconventional_terminate(
                    message=f"This node's blockchain contains a potential fraudalent blocks! Though with the intention of using {NodeType.ARCHIVAL_MINER_NODE.name} for the possibility of finding the longest chain to recover, this may not be possible as of now. Please load any backup and replace the files then try again."
                )

            elif (
                required_genesis_blocks
                and self.node_role is NodeType.ARCHIVAL_MINER_NODE
            ):
                logger.error(
                    "This node's blockchain may be incomplete from the previous update, note that it will get updated after communicating with the master node."
                )
            else:
                logger.info(
                    f"The blockchain context from the file (via deserialiation) has been loaded in-memory and is secured by immutability! | Next Block ID is Block #{self.main_block_id}."
                )

                # - On load, ensure that this was the same as `self.main_block_id`.
                self.leading_block_id = self.main_block_id

            self.blockchain_ready = True
            return frozendict(context)

        unconventional_terminate(
            message=f"The given `context` is not a valid dictionary object! | Received: {context} ({type(context)}). This is a logic error, please report to the developers as soon as possible.",
        )

    def __process_serialize_to_blockchain_file(self, o: frozendict) -> dict[str, Any]:
        """
        A method that serializes the python objects to a much more universally-readable JSON format to the blockchain file.

        Args:
                o (frozendict): The whole chain, wrapped in frozendict.

        Raises:
                TypeError: Cast TypeError when the constraint from the `o` is not followed.

        Returns:
                dict[str, Any]: Returns the JSON form of the blockchain that is in-memory.

        Note:
        TODO By this point, I still haven't consider for scalability and its impact from processing such data.
        * Until there's an impact, I will implement in-memory caching to reduce processing time and insert only data that is missing from the data pool.
        """

        if isinstance(o, frozendict):  # * Cast mutability on the whole chain.
            _o = dict(deepcopy(o))
            for block_idx, each_block in enumerate(_o["chain"]):

                # * Then cast mutability from the whole block of the chain.
                _o["chain"][block_idx] = dict(each_block)

                # * Cast mutability to the content of the whole block of the chain.
                _o["chain"][block_idx]["contents"] = dict(each_block["contents"])

                if len(_o["chain"][block_idx]["contents"]["transactions"]):
                    for transaction_idx, each_transactions in enumerate(
                        _o["chain"][block_idx]["contents"]["transactions"]
                    ):

                        # * Cast mutability on the whole transaction.
                        _o["chain"][block_idx]["contents"]["transactions"][
                            transaction_idx
                        ] = dict(each_transactions)

                        # * Cast mutability of the transaction's payload.
                        _o["chain"][block_idx]["contents"]["transactions"][
                            transaction_idx
                        ]["payload"] = dict(each_transactions["payload"])

                        # * Cast mutability of the transaction's signatures.
                        _o["chain"][block_idx]["contents"]["transactions"][
                            transaction_idx
                        ]["signatures"] = dict(each_transactions["signatures"])

            return _o

        raise TypeError

    async def __resolve_transaction_payload(
        self,
        *,
        action: TransactionActions,
        payload: GroupTransaction | NodeTransaction,
        from_address: AddressUUID,
        to_address: AddressUUID | None,
        is_internal_payload: bool,  # @o Even though I can logically assume its a `Node-based transaction` when `to_address` is None, it is not possible since some `Node-based transactions` actually has a point to `address`.
    ) -> dict | HTTPException:

        error_message: str | None = (
            None  # * Just a variable that is used for returning error messages.
        )

        if not isinstance(payload, GroupTransaction | NodeTransaction):

            error_message = f"The payload is not a valid pydantic object (got '{payload.__class__.__name__}'). Please refer to function signature for more information. This should not happen, report this issue to the  developer to resolve as possible."

            logger.error(error_message)
            return HTTPException(
                detail=error_message, status_code=HTTPStatus.UNPROCESSABLE_ENTITY
            )

        # @o Declare type-hint from here
        encrypter_key: bytes

        # - Prepare the context encrypter.
        # @d Cases for both internal transactions and user transaction contains different key.
        # @o For the case of user transaction, create our own key wherein we can remember that later.
        # @d For the case of internal transaction (Required Models of `NodeTransactions` under `context` or models with prefixes `Node`), there's no need of fetching these transactions back, therefore we can create a random key and push it.

        timestamp: str = datetime.now().strftime("%m%y%d%H%M%S")
        if is_internal_payload:
            encrypter_key = Fernet.generate_key()

        else:  # * Resolves to `NOT` an internal payload.

            # - Create a custom key.
            # @d Constraints: Should be comprised of 32-character of an urlsafe_base64 encoded.
            # @d Some models
            # @d With that, our key should consist of the following:

            # - TransactionActions value enum + 7 starting characters of `from_address` + 12 last characters of `to_address` + datetime.now() under custom format of the following: "%m%y%d%H%M%S". It consists of 12 characters.

            # ! Example
            # - a = datetime.fromisoformat("2022-04-16T20:53:11.012440") -> datetime.datetime(2022, 4, 16, 20, 53, 11, 12440)
            # - a.strftime("%m%y%d%H%M%S") -> '042216205311'
            # - len(a) -> 12

            if to_address is not None:
                resolved_slicer_to_address: int = (
                    11 if len(str(action.value)) == 2 else 12
                )  # @o Enum shouldn't go past 99+ items.

                constructed_context_to_key: bytes = (
                    str(action.value)
                    + from_address[:7]
                    + to_address[-resolved_slicer_to_address:]
                    + timestamp
                ).encode("utf-8")
                encrypter_key = urlsafe_b64encode(constructed_context_to_key)

            else:
                error_message = "Payload is not a internal transaction but `to_address` field is empty! This is an implementation error, please contact the developer regarding this issue."

                logger.error(error_message)
                return HTTPException(
                    detail=error_message, status_code=HTTPStatus.UNPROCESSABLE_ENTITY
                )

        encrypter_payload: Fernet = Fernet(encrypter_key)
        logger.debug(
            f"A key has been generated for the following action `{action.name}`. | Info: {encrypter_key.decode('utf-8')}"
        )

        payload_to_encrypt: GroupTransaction | NodeTransaction = deepcopy(payload)

        # - Hash the content of the payload.
        if not isinstance(payload_to_encrypt.context, str):
            payload_to_encrypt.context = HashUUID(
                (
                    encrypter_payload.encrypt(
                        export_to_json(
                            payload_to_encrypt.context.dict(),
                        )
                    )
                ).decode("utf-8")
            )

        print(
            "\n\n\n\n\n",
            payload_to_encrypt.dict(),
            type(payload_to_encrypt),
            end="\n\n\n\n",
        )

        # - Build the transaction
        try:
            built_internal_transaction: Transaction = Transaction(
                tx_hash=None,  # @o Evaluated as `None` for now.
                action=action,
                payload=globals()[
                    payload_to_encrypt.__class__.__name__
                ](  # - Dynamically instantiate the pydantic model via string.
                    **payload_to_encrypt.dict()
                ),
                signatures=TransactionSignatures(
                    raw=HashUUID(sha256(export_to_json(payload.dict())).hexdigest()),
                    encrypted=HashUUID(
                        sha256(export_to_json(payload_to_encrypt.dict())).hexdigest()
                    ),
                ),
                from_address=AddressUUID(self.node_identity[0])
                if isinstance(payload_to_encrypt, NodeTransaction)
                else AddressUUID(from_address),
                to_address=AddressUUID(to_address) if to_address is not None else None,
            )

        except PydanticValidationError as e:
            error_message = (
                f"There was an error during payload transformation. Info: {e}"
            )

            return HTTPException(
                detail=error_message, status_code=HTTPStatus.UNPROCESSABLE_ENTITY
            )

        # @o Since we now have a copy of the 'premature' transaction, we calculate its hash for the `tx_hash`.
        premature_transaction_copy: dict = built_internal_transaction.dict()

        # @o We don't want to influence `tx_hash` from this even though its a `NoneType`.
        del premature_transaction_copy["tx_hash"]

        # - Calculate the hash based on the content of the deepcopied `built_transaction`.
        premature_calc_sha256: str = sha256(
            export_to_json(premature_transaction_copy)
        ).hexdigest()

        # @o After calculation, invoke this new hash from the `tx_hash` of the `built_transaction`.
        built_internal_transaction.tx_hash = HashUUID(premature_calc_sha256)

        is_duplicate: bool = False
        # @o Then we attempt to resolve by sorting it back and removing any potential duplicates.
        for each_stored_transaction in self.__transaction_container:
            if built_internal_transaction is each_stored_transaction:
                is_duplicate = True
                break

        # @o Append the new transaction.
        if not is_duplicate:
            self.__transaction_container.append(built_internal_transaction)

            logger.info(
                f"Transaction `{built_internal_transaction.tx_hash}` has been created and is on-queue for new blocks!"
            )

            # - For user-based transactions, the method 'self.insert_external_transaction' waits for this method to finish for its transaction to get mapped from the blockchain. With that, let's return necessary contents.

            return {
                "tx_hash": built_internal_transaction.tx_hash,
                "address_ref": to_address,
                "timestamp": timestamp,
            }
        else:
            return HTTPException(
                detail=f"A duplicate transaction regarding {built_internal_transaction.action} has been detected. The system will disregard this transaction as it already exists.",
                status_code=HTTPStatus.CONFLICT,
            )

    async def __search_for(self, *, type: str, uid: AddressUUID | str) -> None:
        return

    def __set_node_state(self) -> None:
        self.__node_ready = (
            True
            if not self.__sleeping_from_consensus and self.blockchain_ready
            else False
        )

    @restrict_call(on=NodeType.ARCHIVAL_MINER_NODE)
    async def __update_chain(self) -> None:
        """
        A private method to call to validate the node's blockchain file from the master's blockchain file.

        # Notes:
        - This should only be called from the following conditions:
                @o Negotiating with the master to update its current chain.
                @o On initilization of the instance.

        """
        # Before attempting to do that, check for the hash first.

        master_node_props = get_master_node_properties()

        while True:

            # - Fetch from the master first by checking the hash, let the endpoint compare it.

            master_hash_valid_response: ClientResponse = await self.__http_instance.enqueue_request(
                url=URLAddress(
                    f"{master_node_props[REF_MASTER_BLOCKCHAIN_ADDRESS]}:{master_node_props[REF_MASTER_BLOCKCHAIN_PORT]}/node/verify_chain_hash"  # type: ignore
                ),
                method=HTTPQueueMethods.POST,
                await_result_immediate=True,
                headers={
                    "x-token": self.node_identity[1],
                    "x-certificate-token": await self._get_consensus_certificate(),
                    "x-hash": await self.get_chain_hash(),
                },
                do_not_retry=True,
                name="verify_local_hash_with_master_node",
            )

            if not master_hash_valid_response.ok:
                # - If that's the case then fetch the blockchain file.
                upstream_chain_content: ClientResponse = await self.__http_instance.enqueue_request(
                    url=URLAddress(
                        f"{master_node_props[REF_MASTER_BLOCKCHAIN_ADDRESS]}:{master_node_props[REF_MASTER_BLOCKCHAIN_PORT]}/node/pull_chain_upstream"  # type: ignore
                    ),
                    method=HTTPQueueMethods.POST,
                    await_result_immediate=True,
                    headers={
                        "x-token": self.node_identity[1],
                        "x-certificate-token": await self._get_consensus_certificate(),
                    },
                    name="fetch_upstream_from_master_node",
                )

                # - For some reason, in my implementation, I also returned the hash with respect to the content.
                if upstream_chain_content.ok:
                    dict_blockchain_content = await upstream_chain_content.json()

                    in_memory_chain: frozendict | None = (
                        self.__process_deserialize_to_load_blockchain_in_memory(
                            import_raw_json_to_dict(dict_blockchain_content["content"])
                        )
                    )

                    if not isinstance(in_memory_chain, frozendict):
                        logger.error(
                            "There was an error loading the blockchain from file to in-memory."
                        )
                        await sleep(INFINITE_TIMER)

                    else:
                        self.__chain = in_memory_chain

                    # ! Once we inject the new payload after fetch, then write it from the file.

                    await self.__process_blockchain_file_to_current_state(
                        operation=BlockchainIOAction.TO_WRITE,
                        context_from_update=(
                            HashUUID(dict_blockchain_content["current_hash"]),
                            BlockchainFileContext(dict_blockchain_content["content"]),
                        ),
                        bypass_from_update=True,
                    )

                    logger.info(
                        f"Blockchain has been updated from upstream! Ready for blockchain operation from the {NodeType.MASTER_NODE.name}."
                    )
                else:
                    logger.warning(
                        f"Update or hash validation processing is not successful due to condition unmet from HTTP status. Re-attempting in 5 seconds ..."
                    )
                    await sleep(5)
                    continue

            else:
                # - When the hash is fine, then standby and wait for the consensus timer.
                logger.info(
                    f"Hash is currently the same as the upstream. Awaiting for orders from the `{NodeType.MASTER_NODE.name}`."
                )
                break

            self.blockchain_ready = True
            return

    async def __update_chain_hash(self, *, new_hash: str) -> None:
        blockchain_hash_update_query: Update = (
            file_signatures.update()
            .where(file_signatures.c.filename == BLOCKCHAIN_NAME)
            .values(hash_signature=new_hash)
        )

        await self.__database_instance.execute(blockchain_hash_update_query)


# # This approach was (not completely) taken from stackoverflow.
# * Please refer to the node/core/email.py for more information.
blockchain_service: BlockchainMechanism | None = None


def get_blockchain_instance(
    *,
    role: NodeType | None = None,
) -> BlockchainMechanism | None:

    global blockchain_service
    token_ref: IdentityTokens | None = get_identity_tokens()

    logger.debug("Initializing or returning blockchain instance ...")

    if role and blockchain_service is None and token_ref is not None:
        # # Note that this will create an issue later when we tried ARCHIVAL_MINER_NODE node mode later on.
        blockchain_service = BlockchainMechanism(
            block_timer_seconds=BLOCKCHAIN_BLOCK_TIMER_IN_SECONDS,
            auth_tokens=token_ref,
            node_role=role,
        )

    # If there are no resulting objective, then we can log this as an error, otherwise return the object.
    if blockchain_service is None:
        logger.critical("There is no blockchain instance.")
        return None

    if token_ref is None:
        logger.critical(
            "There are no identity tokens inferred from your instance. A login authentication should not bypass this method from running. This a developer issue, please report as possible or try again."
        )

    logger.debug("Blockchain instance retrieved, returning to the requestor ...")
    return blockchain_service  # type: ignore # Not sure how can I comprehend where's the mistake, or I just got caffeine overdose to understand mypy's complaint.
