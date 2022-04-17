from argparse import Namespace
from asyncio import create_task, get_event_loop, sleep
from base64 import urlsafe_b64encode
from copy import deepcopy
from datetime import datetime, timedelta
from hashlib import sha256
from http import HTTPStatus
from logging import Logger, getLogger
from secrets import token_urlsafe
from sqlite3 import IntegrityError
from sys import maxsize as MAX_INT_PYTHON
from time import time
from typing import Any, Final, Mapping
from uuid import uuid4

from aiofiles import open as aopen
from blueprint.models import (
    applications,
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
    ApplicantProcessTransaction,
    ApplicantUserTransaction,
    ApplicantUserTransactionInitializer,
    ArchivalMinerNodeInformation,
    Block,
    BlockOverview,
    HashableBlock,
    NodeCertificateTransaction,
    NodeConsensusInformation,
    NodeConsensusTransaction,
    NodeGenesisTransaction,
    NodeMasterInformation,
    NodeMinerProofTransaction,
    NodeRegisterTransaction,
    NodeSyncTransaction,
    NodeTransaction,
    OrganizationIdentityValidator,
    OrganizationTransaction,
    OrganizationTransactionInitializer,
    Transaction,
    TransactionSignatures,
)
from cryptography.fernet import Fernet
from databases import Database
from fastapi import UploadFile
from frozendict import frozendict
from orjson import dumps as export_to_json
from orjson import loads as import_raw_json_to_dict
from pydantic import BaseModel, EmailStr
from pydantic import ValidationError as PydanticValidationError
from pympler.asizeof import asizeof
from sqlalchemy import func, select
from sqlalchemy.sql.expression import Insert, Select, Update
from utils.http import HTTPClient, get_http_client_instance
from utils.processors import (
    hash_context,
    unconventional_terminate,
    validate_organization_existence,
    validate_transaction_mapping_exists,
    validate_user_address,
    validate_user_existence,
)

from core.consensus import ConsensusMechanism
from core.constants import (
    ADDRESS_UUID_KEY_PREFIX,
    ASYNC_TARGET_LOOP,
    BLOCK_HASH_LENGTH,
    BLOCKCHAIN_HASH_BLOCK_DIFFICULTY,
    BLOCKCHAIN_MINIMUM_TRANSACTIONS_TO_BLOCK,
    BLOCKCHAIN_NAME,
    BLOCKCHAIN_NEGOTIATION_ID_LENGTH,
    BLOCKCHAIN_RAW_PATH,
    BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS,
    BLOCKCHAIN_WAIT_TIME_REFRESH_FOR_TRANSACTION,
    INFINITE_TIMER,
    REF_MASTER_BLOCKCHAIN_ADDRESS,
    REF_MASTER_BLOCKCHAIN_PORT,
    AddressUUID,
    AssociatedNodeStatus,
    BlockchainContentType,
    BlockchainFileContext,
    BlockchainIOAction,
    BlockchainPayload,
    ConsensusNegotiationStatus,
    EmploymentApplicationState,
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
    random_generator,
)
from core.decorators import ensure_blockchain_ready, restrict_call
from core.dependencies import (
    get_args_values,
    get_database_instance,
    get_identity_tokens,
    get_master_node_properties,
)
from core.email import EmailService, get_email_instance

logger: Logger = getLogger(ASYNC_TARGET_LOOP)


class BlockchainMechanism(ConsensusMechanism):
    def __init__(
        self,
        *,
        block_timer_seconds: int = 10,
        auth_tokens: IdentityTokens,
        node_role: NodeType,
    ) -> None:

        # # Required Variables for the Blockchain Operaetion.
        self.node_role: NodeType = node_role
        self.auth_token: IdentityTokens = auth_tokens

        self.block_timer_seconds: Final[int] = block_timer_seconds
        self.mine_duration: timedelta = timedelta()
        self.consensus_timer_expiration: datetime = datetime.now()

        # # Containers
        self.transaction_container: list[Transaction] = []
        self.hashed_block_container: list[Block] = []
        self.confirming_block_container: list[Block] = []
        self.unsent_block_container: list[Block] = []

        # # Instances
        self.db_instance: Final[Database] = get_database_instance()
        self.http_instance: HTTPClient = get_http_client_instance()
        self.email_service: EmailService = get_email_instance()
        self.identity = auth_tokens  # - Equivalent to get_identity_tokens()

        # # State and Variable References
        self.blockchain_ready: bool = False  # * This bool property is used for determining if the blockchain is ready to take its request from its master or side nodes.
        self.cached_block_id: int = (
            1  # * The current ID of the block to be rendered from the blockchain.
        )
        self.cached_total_transactions: int = 0
        self.new_master_instance: bool = False  # * This bool property will be used whenever when the context of the blockchain file is empty or not. Sets to true when its empty.
        self.node_ready: bool = False  # * This bool property is used for determining if this node is ready in terms of participating from the master node, this is where the consensus will be used.
        self.sleeping_from_consensus: bool = False  # * This bool property is used for determining if the node is under consensus sleep or not. This property is used as a dependency to state whether the node is ready or is the blockchain for other operations.

        super().__init__(role=node_role)

    async def initialize(self) -> None:
        """
        # A method that initialize resources needed for the blockchain system to work.
        """

        # - Load the blockchain for both nodes.
        self._chain: frozendict = await self._process_blockchain_file_to_current_state(
            operation=BlockchainIOAction.TO_READ
        )

        if self.node_role is NodeType.MASTER_NODE:
            if self.new_master_instance:
                for _ in range(0, BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS):
                    await self._create_genesis_block()  # * We can only afford to do per block since async will not detect other variable changes. I think we don't have a variable classifier that is meant to change dramatically without determined time. And that is 'volatile'.

                # @o When on initial instance, we need to handle the property for the blockchain system to run. Otherwise we just lock out the system even we already created.
                self.blockchain_ready = True
                self.new_master_instance = False

                logger.info(
                    "Genesis block generation has been finished! Blockchain system ready."
                )

            else:
                self.blockchain_ready = True
                logger.info("Blockchain system is ready.")

            create_task(
                self._block_timer_executor(),
                name=f"{BlockchainMechanism.__name__}_{self.role.name}_instance_{self._block_timer_executor.__name__}",
            )

            print("final", self._chain)

        else:
            if self.identity is not None:
                existing_certificate = await self._get_own_certificate()

                if not existing_certificate:
                    logger.warning(
                        f"Association certificate token does not exists! Fetching a certificate by establishing connection with the {NodeType.MASTER_NODE} blockchain."
                    )
                    await self.establish()
                else:
                    logger.info(
                        "Association certificate token exists. Ignoring establishment from the `MASTER_NODE`."
                    )

            logger.info(
                f"Running the update method to validate the local hash of the blockchain against the {NodeType.MASTER_NODE} blockchain."
            )

            await self._update_chain()

    @restrict_call(on=NodeType.MASTER_NODE)
    async def insert_external_transaction(
        self,
        action: TransactionActions,
        from_address: AddressUUID,
        to_address: AddressUUID,
        data: ApplicantLogTransaction
        | ApplicantProcessTransaction
        | ApplicantUserTransactionInitializer
        | OrganizationTransaction
        | AdditionalContextTransaction,
    ) -> bool:
        """
        @o A method that is callable outside scope that can create a transaction as well as the entity from the database, if possible. It handles the content to render from the transaction as this will be used for content viewing later from the frontend.

        ### Args:
            * action (TransactionActions): An enum that describes the cause of instantiation of this transaction.
            * from_address (AddressUUID): A unique identifier that instantiated this transaction.
            * to_address (AddressUUID): A unique identifier that is being referred from the content of this transaction.
            * data (ApplicantLogTransaction | ApplicantProcessTransaction | ApplicantUserTransactionInternal | OrganizationTransaction | AdditionalContextTransaction): A pydantic model that is qualified for this method to work. Otherwise it will result in error.

        ### Returns:
            * bool: Returns `True` or `False` depending whether this function success or fails on execution of resolving the transaction for block minin.

        ### Note:
            * For `NodeTransactions`, it was already handled from the method `self._insert_transaction`. It doesn't need extra parameters since those contains internal actions that doesn't need extra handling as they were displayed on Explorer API.
        """

        supported_models: Final[list[Any]] = [
            ApplicantLogTransaction,
            ApplicantProcessTransaction,
            ApplicantUserTransactionInitializer,
            OrganizationTransaction,
            AdditionalContextTransaction,
        ]

        # - Check if data is a pydantic model instance.
        # @o If data is an `instance` from one of the elements of `supported_structures` AND `action` provided is under the scope of `TransactionActions`. AND `from_address` as well as `to_address` contains something like a string. Proceed.
        if (
            any(isinstance(data, each_model) for each_model in supported_models)
            and action in TransactionActions
            and isinstance(from_address, str)
            and isinstance(to_address, str)
        ):

            # - [1] Ensure that the `from_address` is existing.
            # ! For the sake of complexity and due to my knowledge upon using JOIN statement.
            # ! I will be dividing those into two statements.

            get_existing_from_address_query, get_existing_to_address_query = select(
                [func.count()]
            ).where(users.c.unique_address == from_address), select(
                [func.count()]
            ).where(
                users.c.unique_address == to_address
            )

            # * Get it, by we will not be using it.
            # * I don't know how to use count
            (
                is_existing_from_address,
                is_existing_to_address,
            ) = await self.db_instance.fetch_one(
                get_existing_from_address_query
            ), await self.db_instance.fetch_one(
                get_existing_to_address_query
            )

            # @o If all fetched addresses has a count of 1 (means they are existing), proceed.
            # ! These addresses will either contain a `str` or a `None` (`NoneType`).
            # ! If one of them contains `None` or `NoneType` this statement will result to false.
            if all(
                fetched_address
                for fetched_address in [
                    is_existing_to_address,
                    is_existing_from_address,
                ]
            ):

                # @o Declared for type-hint. Initialized on some conditions.
                resolved_payload: AdditionalContextTransaction | ApplicantLogTransaction | ApplicantProcessTransaction | ApplicantUserTransaction | OrganizationTransaction | None = (
                    None
                )
                tx_content_type: TransactionContextMappingType | None = None

                # - [2] Verify if action (TransactionAction) to TransactionContextMappingType is viable.
                # # [4]

                # - For the applicant application attempt actions.
                if action in [
                    TransactionActions.APPLICANT_APPLY,
                    TransactionActions.APPLICANT_APPLY_CONFIRMED,
                    TransactionActions.APPLICANT_APPLY_REJECTED,
                ] and isinstance(data, ApplicantProcessTransaction):

                    # - Since this was a new entry, we need to do some handling for the database entry.
                    try:
                        # @o It doesn't matter beyond this point if the user tries again or not, we cannot handle that for now. See `CANNOT DO` of TODO.
                        if (
                            await validate_transaction_mapping_exists(
                                reference_address=AddressUUID(to_address),
                                content_type=TransactionContextMappingType.APPLICANT_BASE,
                            )
                            is True
                        ):
                            # @o Type-hint.
                            application_process_query: Insert | Update

                            if action is TransactionActions.APPLICANT_APPLY:
                                application_process_query = (
                                    applications.insert().values(
                                        process_id=RandomUUID(token_urlsafe(16)),
                                        requestor=data.requestor,
                                        to=data.receiver,
                                        state=EmploymentApplicationState.REQUESTED,
                                    )
                                )
                            else:
                                application_process_query = (
                                    applications.update()
                                    .where(
                                        applications.c.process_uuid == data.process_id
                                    )
                                    .values(
                                        state=EmploymentApplicationState.ACCEPTED
                                        if action
                                        is TransactionActions.APPLICANT_APPLY_CONFIRMED
                                        else EmploymentApplicationState.REJECTED
                                    )
                                )

                            await self.db_instance.execute(application_process_query)

                        else:
                            return False

                    except IntegrityError as e:
                        logger.error(
                            f"There was an error regarding application process entry to database. | Info: {e}"
                        )
                        return False

                    tx_content_type = TransactionContextMappingType.APPLICANT_LOG
                    resolved_payload = data

                # - For transactions that require generation of `user` under Organization or as an Applicant.
                elif action in [
                    TransactionActions.INSTITUTION_ORG_GENERATE_APPLICANT,
                    TransactionActions.ORGANIZATION_USER_REGISTER,
                ] and (
                    isinstance(data, ApplicantUserTransactionInitializer)
                    or isinstance(data, OrganizationTransactionInitializer)
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
                    validate_user: bool
                    existing_association: Mapping | None

                    if (
                        isinstance(data, ApplicantUserTransactionInitializer)
                        and data.association_address is not None
                    ):

                        validate_user = await validate_user_existence(
                            user_identity=AgnosticCredentialValidator(
                                first_name=data.first_name,
                                last_name=data.last_name,
                                username=data.username,
                                email=data.email,
                            )
                        )

                        if validate_user:
                            return False

                        existing_association = await validate_organization_existence(
                            org_identity=OrganizationIdentityValidator(
                                association_address=data.association_address,
                                association_name=data.association_name,
                                association_group_type=data.association_group_type,
                            ),
                            is_org_scope=False,
                        )

                        if existing_association is None:
                            logger.error(
                                "The associate address does not exists! Please refer to the right associate/organization or association to proceed the registration."
                            )
                            return False

                        tx_content_type = TransactionContextMappingType.APPLICANT_BASE

                    # - For the case of registering with the associate/organization, sometimes user can register with associate/organization reference existing and otherwise. With that, we need to handle the part where if the associate/organization doesn't exist then create a new one. Otherwise, refer its self from that associate/organization and we are good to go.

                    elif isinstance(data, OrganizationTransactionInitializer):
                        # - Validate the existence of the user based on the sensitive information.
                        validate_user = await validate_user_existence(
                            user_identity=AgnosticCredentialValidator(
                                first_name=data.first_name,
                                last_name=data.last_name,
                                username=data.username,
                                email=data.email,
                            )
                        )

                        if validate_user:
                            return False

                        # - Validate the existence of an associate/organization.
                        existing_association = await validate_organization_existence(
                            org_identity=OrganizationIdentityValidator(
                                association_address=data.association_address,
                                association_name=data.association_name,
                                association_group_type=data.association_group_type,
                            ),
                            is_org_scope=True,
                        )

                        # - Condition for creating a new associate/organization wherein there's no referrable address.
                        if (
                            data.association_address is None
                            and data.association_group_type is not None
                            and data.association_name is not None
                            and existing_association is None
                        ):
                            generated_address: Final[AddressUUID] = AddressUUID(
                                f"{ADDRESS_UUID_KEY_PREFIX}:{uuid4().hex}"
                            )

                            # - Create an associate/organization when name is only provided assuming its a new instance.
                            new_association_query: Insert = (
                                associations.insert().values(
                                    address=generated_address,
                                    name=data.association_name,
                                    group=data.association_group_type,
                                )
                            )
                            await self.db_instance.execute(new_association_query)

                            # - Assign the generated association address from the context.
                            # @o Since our approach is cascading, we need to assign this `generated_address` instead so that we don't need to do some resolution steps to get the newly inserted association address from the database again.
                            data.association_address = generated_address

                        # - Condition for assigning a user (that will be generated later) from this address.
                        elif (
                            data.association_address is not None
                            and data.association_group_type is None
                            and data.association_name is None
                            and existing_association is not None
                        ):
                            data.association_address = existing_association.address  # type: ignore

                            if existing_association is not None:
                                logger.error(
                                    "The supplied parameter for the `association` address reference does not exist! This is a developer-issue, please contact as possible."
                                )
                            return False

                        else:
                            logger.error(
                                f"Instances has condition unmet. Either the `association` contains nothing or the instance along with the `association` condition does not met. Please try again."
                            )

                        tx_content_type = (
                            TransactionContextMappingType.ORGANIZATION_BASE
                        )

                    # @o When all of the checks are done, then create the user.
                    try:
                        insert_user_query: Insert = users.insert().values(
                            association=data.association_address,
                            first_name=data.first_name,
                            last_name=data.last_name,
                            email=data.email,
                            username=data.username,
                            password=hash_context(pwd=RawData(data.password)),
                        )

                        await self.db_instance.execute(insert_user_query)

                    except IntegrityError as e:
                        logger.error(
                            f"There was an error during account generation. This may likely be a cause of duplication or unique-ness issue. Please check your credentials and try again. | Info: {e}"
                        )
                        return False

                    # - After all that, its time to resolve those context for the `External` model. (For the blockchain to record).

                    # ! Excluding fields via Model is not possible.
                    # ! https://github.com/samuelcolvin/pydantic/issues/1862.

                    # @o Therefore, we need to manually declare those fields from the `AgnosticTransactionUserCredentials`.
                    removed_credentials_context: dict = data.dict(
                        exclude={
                            "association_address": True,
                            "association_name": True,
                            "association_group_type": True,
                            "first_name": True,
                            "last_name": True,
                            "email": True,
                            "username": True,
                            "password": True,
                        }
                    )

                    resolved_payload = (
                        ApplicantUserTransaction(**removed_credentials_context)
                        if isinstance(data, ApplicantUserTransactionInitializer)
                        else OrganizationTransaction(**removed_credentials_context)
                    )

                # - For the invocation of log for the Applicant under enum `ApplicantLogTransaction`.
                # @o This needs special handling due to the fact that it may contain an actual file.
                # ! There's a need of special handling from the API endpoint receiver due to its nature of using content-type: `multipart/form-data`. Therefore, this method expects to have an `ApplicantLogTransaction`.
                elif (
                    action is TransactionActions.INSTITUTION_ORG_REFER_NEW_DOCUMENT
                    and isinstance(data, ApplicantLogTransaction)
                ):
                    if (
                        await validate_transaction_mapping_exists(
                            reference_address=AddressUUID(to_address),
                            content_type=TransactionContextMappingType.APPLICANT_BASE,
                        )
                        is True
                    ):

                        if isinstance(data.file, UploadFile):
                            # @o We combine the current time under isoformat string + given filename + referred user address in full length.

                            # ! We need to create our own key because we are going to access these files.
                            # * Since this project is under repository, we will keep it this way.
                            # * In actual real world, we ain't gonna be doing this.

                            # @o Create the key based from the user address (`target` or `to`), truncated from the first 12 character + datetime in custom format, please see the variable `current_date` below.
                            # # Documentation regarding custom format: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

                            timestamp: datetime = datetime.now()
                            current_date: str = timestamp.strftime(
                                "%y%m%d%H%M%S"
                            )  # @o datetime.now() produces "datetime.datetime(2022, 4, 16, 19, 45, 36, 724779)" and when called with datetime.now().isoformat() produces "2022-04-16T19:45:36.724779'", when we used datetime.now().strftime() with parameters "%y%m%d%H%M%S", will produce "'220416194536'"

                            encrypter_key: bytes = f"{to_address}{current_date}".encode(
                                "utf-8"
                            )
                            file_encrypter: Fernet = Fernet(encrypter_key)

                            async with aopen(
                                f"../userfiles/{timestamp.isoformat()}{data.file.filename}{to_address}",
                                "wb",
                            ) as file_writer:
                                raw_context: bytes | str = await data.file.read()
                                encrypted_context: bytes = file_encrypter.encrypt(
                                    raw_context.encode("utf-8")
                                    if isinstance(raw_context, str)
                                    else raw_context
                                )

                                await file_writer.write(encrypted_context)

                            # - Since we got the file and encrypted it, get the SHA256 of the payload.
                            # - And replace it on the field of the `data.file` so that we will get a reference when we refer from it.
                            data.file = HashUUID(
                                sha256(
                                    raw_context.encode("utf-8")
                                    if isinstance(raw_context, str)
                                    else raw_context
                                ).hexdigest()
                            )

                        # - Do the following for all condition.
                        tx_content_type = TransactionContextMappingType.APPLICANT_LOG
                        resolved_payload = data

                    else:
                        return False

                # - For the `extra` fields of both `ApplicantTransaction` and `OrganizationTransaction`.
                # # [2]
                elif action in [
                    TransactionActions.ORGANIZATION_REFER_EXTRA_INFO,
                    TransactionActions.INSTITUTION_ORG_APPLICANT_REFER_EXTRA_INFO,
                ] and isinstance(data, AdditionalContextTransaction):
                    # * Just validate if the specified entity address does exists.
                    if (
                        validate_user_address(supplied_address=AddressUUID(to_address))
                        is True
                    ):
                        tx_content_type = (
                            TransactionContextMappingType.APPLICANT_ADDITIONAL
                            if action
                            is TransactionActions.INSTITUTION_ORG_APPLICANT_REFER_EXTRA_INFO
                            else TransactionContextMappingType.ORGANIZATION_ADDITIONAL
                        )
                        resolved_payload = data

                else:
                    logger.error(
                        "There was an error during conditional check. Are you sure this combination is right? Please check the declaration and try again."
                    )
                    return False

                if resolved_payload is None:
                    return False  # * There was already a log so there's no need to output something from here.

                transaction_context: dict | bool = (
                    await self._resolve_transaction_payload(
                        action=action,
                        from_address=from_address,
                        to_address=to_address,
                        payload=resolved_payload,
                        is_internal_payload=False,
                    )
                )

                # * Append the transaction mapping here.
                if isinstance(transaction_context, dict):
                    insert_transaction_content_map_query: Insert = (
                        tx_content_mappings.insert().values(
                            address_ref=to_address,
                            block_no_ref=self.cached_block_id,
                            tx_ref=transaction_context["tx_hash"],
                            content_type=tx_content_type,
                            timestamp=datetime.now(),
                        )
                    )

                    await self.db_instance.execute(insert_transaction_content_map_query)

                else:
                    logger.error(
                        f"Received a `{transaction_context}` instead of a `{dict}`. This is not what I wanted. From this method, we should be receiving a `dict` instead. Please report this issue to the developer."
                    )

                get_from_address_email_query: Select = select([users.c.email]).where(
                    users.c.unique_address == from_address
                )

                from_address_email = await self.db_instance.fetch_one(
                    get_from_address_email_query
                )

                if from_address_email is not None and tx_content_type is not None:
                    create_task(
                        self.email_service.send(
                            content=f"<html><body><h1>Notification from Folioblocks!</h1><p>There was an error from your inputs. The transaction regarding {tx_content_type.name} has been disregarded. Please try your actions again.</p><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
                            subject="Error Transaction from Folioblock!",
                            to=EmailStr(from_address_email),
                        ),
                        name="send_email_invalid_address_notification",
                    )
                else:
                    logger.error("Failed to send an email regarding the error.")
                return False

            logger.error(
                f"{'Sender' if from_address is None else 'Receiver'} address seem to be invalid. Please check your input and try again. This transaction will be disregarded."
            )
            return False

        logger.error(
            f"There was a missing or invalid value inserted from  the following parameters: `action`, `from_address` and `data`. `action` requires to have a value of an Enum `{TransactionActions}`, `from_address` should contain a valid {str} and `data` should be wrapped in a pydantic model ({BaseModel})! Please encapsulate your `data` to one of the following pydantic models: {[each_model.__name__ for each_model in supported_models]}."
        )
        return False

        # - Attempt to recognize the action by referring to the instance of the data.

    async def insert_mined_block(
        self,
        *,
        block: Block,
        from_origin: SourceNodeOrigin,
        master_address_ref: AddressUUID | None = None,
    ) -> None:
        if from_origin in SourceNodeOrigin:
            block_mining_processor = await (
                get_event_loop().run_in_executor(
                    None,
                    self._mine_block,
                    block,
                )
            )
            mined_block: Block = await block_mining_processor

            await self._append_block(context=mined_block)
            logger.info(
                f"Block {block.id} has been enqueued for appending from the the blockchain after mining."
            )

            if (
                from_origin is SourceNodeOrigin.FROM_MASTER
                and master_address_ref is not None
                and isinstance(master_address_ref, str)
            ):
                logger.info(
                    f"Block {block.id} is detected as a payload delivery for the consensus of being selected with the condition of sleep expiration. (Proof-of-Elapsed-Time) from the {NodeType.MASTER_NODE.name}. Sending back the hashed/mined block."
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

                recorded_consensus_negotiation = await self.db_instance.fetch_one(
                    recorded_consensus_negotiation_query
                )

                if recorded_consensus_negotiation is not None:
                    payload_to_master = await self.http_instance.enqueue_request(
                        url=URLAddress(
                            f"{master_origin_source_host}:{master_origin_source_port}/receive_hashed_block"
                        ),
                        method=HTTPQueueMethods.POST,
                        headers={
                            "x-certificate-token": await self._get_own_certificate(),
                            "x-token": self.identity[1],
                        },
                        data={
                            "consensus_negotiation_id": recorded_consensus_negotiation.consensus_negotiation_id,  # type: ignore # - For some reason it doesn't detect the mapping.
                            "miner_address": self.identity[0],
                            "block": mined_block.json(),
                        },
                        retry_attempt=150,
                        name=f"send_hashed_payload_at_{NodeType.MASTER_NODE.name.lower()}_block_{mined_block.id}",
                    )

                    if payload_to_master.ok:
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
                        logger.info(f"Consensus Negotiation ID {recorded_consensus_negotiation.consensus_negotiation_id} with the peer (receiver) address {master_address_ref} has been labelled as {ConsensusNegotiationStatus.COMPLETED}!")  # type: ignore

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

            else:  # - Asserts to NodeSourceOrigin.ARCHIVAL_MINER with master_address_ref is None.

                block_confirmed: bool = False
                # - Validate the given block by checking its id and other fields that is outside from the context.
                for each_confirming_block in self.confirming_block_container:

                    logger.debug(
                        f"Block Compare (Confirming Block | Mined Block) |> ID: ({each_confirming_block.id} | {mined_block.id}), Block Size Bytes: ({each_confirming_block.block_size_bytes} | {mined_block.block_size_bytes}), Prev Hash Block: ({each_confirming_block.prev_hash_block} | {mined_block.prev_hash_block}), Timestamp: ({each_confirming_block.contents.timestamp} | {mined_block.contents.timestamp})"
                    )

                    if (
                        each_confirming_block.id == mined_block.id
                        and each_confirming_block.block_size_bytes
                        == mined_block.block_size_bytes
                        and each_confirming_block.prev_hash_block
                        == mined_block.prev_hash_block
                        and each_confirming_block.contents.timestamp
                        == mined_block.contents.timestamp
                    ):
                        self.confirming_block_container.remove(
                            each_confirming_block
                        )  # - Remove from the container as it was already confirmed.

                        block_confirmed = True
                        break

                if not block_confirmed:
                    logger.error(
                        "Cannot confirm any confirming blocks from the received mined blocks. This is not possible for this logic condition to be hit. There may be a missing implementation, please report this to the developer."
                    )
                    return None

            # * Regardless of who receives it, append it from their block.
            # - For MASTER_NODE, this may be a redundant check, but its fine.
            if self.cached_block_id == mined_block.id:
                await self._append_block(context=mined_block)

                return None

        else:
            logger.error(
                f"The provided value for `from_origin` is not a valid enum! Got {from_origin} instead. This is a developer-issue logic error, please report to them this issue as soon as possible."
            )
            return None

    @ensure_blockchain_ready()
    def get_blockchain_public_state(self) -> NodeMasterInformation | None:
        if self.node_role is NodeType.MASTER_NODE:

            # # This may not be okay.
            return NodeMasterInformation(
                chain_block_timer=self.block_timer_seconds,
                total_blocks=len(self._chain["chain"])
                if self._chain is not None
                else 0,
                total_transactions=self.cached_total_transactions,
            )
        logger.warning(
            f"This client node requests for the `public_state` when their role is {self.node_role.name}! | Expects: {NodeType.MASTER_NODE.name}."
        )
        return None

    @ensure_blockchain_ready()
    def get_blockchain_private_state(self) -> NodeConsensusInformation:
        last_block: Block | None = self._get_last_block()

        return NodeConsensusInformation(
            consensus_timer_expiration=self.consensus_timer_expiration,
            is_mining=not self.is_blockchain_ready,
            is_sleeping=self.is_node_ready,
            last_mined_block=last_block.id if last_block is not None else 0,
            node_role=self.role,
            owner=self.auth_token[0],
        )

    async def get_chain_hash(self) -> HashUUID:
        fetch_chain_hash_query = select([file_signatures.c.hash_signature]).where(
            file_signatures.c.filename == BLOCKCHAIN_NAME
        )

        return HashUUID(await self.db_instance.fetch_val(fetch_chain_hash_query))

    async def get_chain(self) -> str:
        # At this state of the system, the blockchain file is currently unlocked. Therefore give it.

        # Adjust function for forcing to save new data when fetched.
        async with aopen(BLOCKCHAIN_NAME, "r") as chain_reader:
            data: str = await chain_reader.read()

        return data

    @property
    def is_blockchain_ready(self) -> bool:
        return self.blockchain_ready

    @property
    def is_node_ready(self) -> bool:
        return self.node_ready and self.is_blockchain_ready

    @ensure_blockchain_ready()
    async def overview_blocks(self, limit_to: int) -> list[BlockOverview] | None:
        if self._chain is not None:
            candidate_blocks: list[BlockOverview] = deepcopy(
                self._chain["chain"][len(self._chain["chain"]) - limit_to :]
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

    async def _append_block(
        self,
        *,
        context: Block,
    ) -> None:
        """
        A method that is callad whenever a new block is ready to be inserted from the blockchain, both in-memory and to the file.

        Args:
            context (Block | Transaction): The context of the block as is.
            auth_context (IdentityTokens): Authentication attribute, not sure what to do on this one yet.

        TODO
        * Implement security of some sort, use `auth_context` or something. | We may use this and compute its hash for comparing context and also length.
        """
        if self._chain is not None:
            block_context: dict = context.dict()
            block_context["contents"] = frozendict(block_context["contents"])

            # @o If a certain block has been inserted in a way that it is way over far or less than the current self.cached_block_id, then disregard this block.
            if block_context["id"] != self.cached_block_id:
                logger.error(
                    f"This block #{block_context['id']} is way too far or behind than the one that is saved in the local blockchain file. Will attempt to fetch a new blockchain file from the MASTER_NODE node. This block will be DISREGARDED."
                )
                return

            # - Apply immutability on other `dict` objects from the block context.
            # @o As per the approach indicated from the `self._process_serialize_to_blockchain_file`. We are going to do this in descending form.

            if len(block_context["contents"]["transactions"]):
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
                    self.cached_total_transactions += 1

                # - [4] Apply immutability on the contents, contaning a set of transaction/s.
                block_context["contents"] = frozendict(block_context["contents"])

            # - [5] Apply immutability from the whole block and then append it.
            self._chain["chain"].append(frozendict(block_context))

            # ! Hit the next block for the allocation as we finished processing a block!
            self.cached_block_id += 1

            await self._process_blockchain_file_to_current_state(
                operation=BlockchainIOAction.TO_WRITE
            )
            logger.info(f"Block {context.id} has been appended from the blockchain!")

            await self._consensus_sleeping_phase()

        else:
            unconventional_terminate(
                message="There's no 'chain' from the root dictionary of blockchain! This is a developer-implementation issue, please report to the developers as soon as possible!",
            )

    @restrict_call(on=NodeType.MASTER_NODE)
    async def _block_timer_executor(self) -> None:
        logger.info(
            f"Block timer has been executed. Refreshes at {self.block_timer_seconds} seconds."
        )

        while True:
            logger.warning(
                f"Sleeping for {self.block_timer_seconds} seconds while collecting real-time transactions."
            )

            # - Sleep first due to block timer.
            await sleep(self.block_timer_seconds)

            # - Queue for other (`ARCHIVAL_MINER_NODE`) nodes to see who can mine the block.
            available_node_info: ArchivalMinerNodeInformation | None = (
                await self._get_available_archival_miner_nodes()
            )

            # @o When there's no miner active, sleep for a while and requeue again.
            if available_node_info is None:
                continue

            # @o Added for type-hints.
            generated_block: Block | None = None

            # @o When there's a miner, do a closed-loop process.

            # @o To save some processing time, we need to have a sufficient transactions before we process them to a block.
            # - Wait until a number of sufficient transactions were received.
            # - Since we already have a node, do not let this one go.
            if len(
                self.transaction_container
            ) > BLOCKCHAIN_MINIMUM_TRANSACTIONS_TO_BLOCK and not len(
                self.unsent_block_container
            ):

                logger.info(
                    f"Number of required transactions were sufficient! There are {len(self.transaction_container)} transactions that will be converted to a block for processing."
                )

                # - Create a block from all of the transactions.
                generated_block = await self._create_block()

            elif len(self.unsent_block_container):
                logger.info(
                    f"Block {self.unsent_block_container[0]} has been left-out from mining due to previous miner unable to respond in time. Using this block for the mining process instead."
                )

                generated_block = self.unsent_block_container.pop(0)

            else:
                logger.warning(
                    f"There isn't enough transactions to create a block. Awaiting for new transactions in {BLOCKCHAIN_WAIT_TIME_REFRESH_FOR_TRANSACTION} seconds."
                )

                await sleep(BLOCKCHAIN_WAIT_TIME_REFRESH_FOR_TRANSACTION)

            # - Create a Consensus Negotiation ID out of `urlsafe_b64encode`.
            # @o Create a Consensus Negotiation ID for the nodes to remember that this happened.
            # @o Even though we already have the certification token, we still need this one to track current negotiations between nodes.

            if generated_block is not None:
                generated_consensus_negotiation_id: str = token_urlsafe(
                    BLOCKCHAIN_NEGOTIATION_ID_LENGTH
                )

                attempt_deliver_payload = await self.http_instance.enqueue_request(
                    url=URLAddress(
                        f"{available_node_info.source_host}:{available_node_info.source_port}/blockchain/receive_raw_block"
                    ),
                    method=HTTPQueueMethods.POST,
                    await_result_immediate=True,
                    headers={
                        "x-certificate-token": await self._get_own_certificate(),
                        "x-hash": await self.get_chain_hash(),
                        "x-token": self.identity[1],
                    },
                    data={
                        "block": generated_block.json(),
                        "master_address": self.identity[0],
                        "consensus_negotiation": generated_consensus_negotiation_id,
                    },
                    retry_attempt=99,
                    name=f"send_raw_payload_at_{NodeType.ARCHIVAL_MINER_NODE.name.lower()}_{available_node_info.miner_address[-6:]}",
                )

                if attempt_deliver_payload.ok:
                    # - Save this consensus negotiation ID as well for the retrieval verification of the hashed/mined block.
                    save_in_progress_negotiation_query: Insert = (
                        consensus_negotiation.insert().values(
                            block_no_ref=generated_block.id,
                            consensus_negotiation_id=generated_consensus_negotiation_id,
                            peer_address=self.identity[0],
                            status=ConsensusNegotiationStatus.ON_PROGRESS,
                        )
                    )

                    await self.db_instance.execute(save_in_progress_negotiation_query)

                    # - Store this for a while for the verification upon receiving a hashed/mined block.
                    self.confirming_block_container.append(generated_block)

                else:
                    logger.warning(
                        "After multiple retries, the generated block will be stored and will find archival miner node candidates who doesn't disconnect."
                    )
                    self.unsent_block_container.append(generated_block)

            logger.error(
                f"Cannot proceed when block generated returned {generated_block}! This is probably a developer-logic error issue. Please contact the developer regarding this."
            )

    def _consensus_calculate_sleep_time(self, *, mining_duration: float) -> None:
        if not self.is_blockchain_ready and not self.new_master_instance:

            self.mine_duration = timedelta(seconds=mining_duration)  # type: ignore # - Let timedelta convert if there's a residue (ie. milliseconds).
            self.consensus_timer_expiration = datetime.now() + self.mine_duration

            logger.debug(
                f"Consensus timer is calculated. Set to {self.mine_duration} seconds before waking. | Will expire (wakes up and approximately) at {self.consensus_timer_expiration}"
            )

    async def _consensus_sleeping_phase(self) -> None:
        if not self.new_master_instance:
            self.sleeping_from_consensus = True

            logger.info(
                f"Block mining is finished. Sleeping until {self.consensus_timer_expiration}."
            )

            await sleep(self.mine_duration.total_seconds())
            self.sleeping_from_consensus = False

            # * When done, ensure that the node's sate is changed.
            self._set_node_state()

            logger.info(
                "Woke up from the consensus timer! Ready to take blocks to mine."
            )
            return

        logger.info(
            f"Consensus timer ignored due to condition. | Is new instance: {self.new_master_instance}, Blockchain ready: {self.blockchain_ready}"
        )

    async def _create_block(self) -> Block | None:
        # @o When building a block, we first have to consider that there are some properties were undefined. The nonce, block_size_bytes, and hash_block.
        # @o With this, we need to seperate the contents of the block, providing a way from the inside of the block to be hashable and identifiable for hash verification.
        # ! Several properties have to be seperated due to their nature of being able to overide the computed hash block.

        last_block: Block | None = self._get_last_block()

        if last_block is not None:
            if last_block.id >= self.cached_block_id:
                logger.critical(
                    f"Cannot create a block! Last block is greater than or equal to the ID of the currently cached available-to-allocate block. | Last Block ID: {last_block.id} | Currently Cached: {self.cached_block_id}"
                )
                return None
        else:
            logger.warning(
                f"This new block will be the first block from this blockchain."
            )

        shadow_transaction_container = deepcopy(self.transaction_container)
        self.transaction_container.clear()

        _block: Block = Block(
            id=self.cached_block_id,
            block_size_bytes=None,  # * To be resolved on the later process.
            hash_block=None,  # ! Unsolvable, mine_block will handle it.
            prev_hash_block=HashUUID(
                last_block.hash_block
                if last_block is not None and last_block.hash_block is not None
                else "0" * BLOCK_HASH_LENGTH
            ),
            contents=HashableBlock(
                nonce=None,  # - This are determined during the process of mining.
                validator=self.identity[0],
                transactions=shadow_transaction_container,
                timestamp=datetime.now(),
            ),
        )

        _block.block_size_bytes = asizeof(_block.contents.json())

        logger.info(
            f"Block #{_block.id} with a size of ({_block.block_size_bytes} bytes) has been created."
        )

        return _block

    async def _create_genesis_block(self) -> None:
        """
        Generates a block, hash it and append it within the context of the blockchain, for both the file and the in-memory.
        """

        # * Create a transaction for the generation of the genesis block.
        await self._insert_internal_transaction(
            action=TransactionActions.NODE_GENERAL_GENESIS_INITIALIZATION,
            data=NodeTransaction(
                action=NodeTransactionInternalActions.INIT,
                context=NodeGenesisTransaction(
                    block_genesis_no=self.cached_block_id,
                    generator_address=self.identity[0],
                    time_initiated=datetime.now(),
                ),
            ),
        ),

        generated_block_w_genesis: Block | None = await self._create_block()

        if generated_block_w_genesis is not None:
            await self.insert_mined_block(
                from_origin=SourceNodeOrigin.FROM_ARCHIVAL_MINER,  # * Fake it.
                block=generated_block_w_genesis,
            )
        else:
            logger.error("There was an error while generating a genesis block.")

        return None

    async def _get_available_archival_miner_nodes(
        self,
    ) -> ArchivalMinerNodeInformation | None:

        available_nodes_query = select(
            [
                associated_nodes.c.user_address,
                associated_nodes.c.source_address,
                associated_nodes.c.source_port,
            ]
        ).where(associated_nodes.c.status == AssociatedNodeStatus.CURRENTLY_AVAILABLE)

        available_nodes: list[Mapping] = await self.db_instance.fetch_all(
            available_nodes_query
        )

        if not len(available_nodes):
            logger.info(
                f"There are no available nodes to mine the block. Retrying again the after interval of the block timer. ({self.block_timer_seconds} seconds)"
            )
            return None

        logger.info(f"There are {len(available_nodes)} candidates available!")

        for each_candidate in available_nodes:
            candidate_response = await get_http_client_instance().enqueue_request(
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

                print(resolved_candidate_state_info)
                logger.info(
                    f"Archival Miner Candidate {resolved_candidate_state_info['owner']} has responded from the mining request!"
                )

                if (
                    not resolved_candidate_state_info["is_mining"]
                    and NodeType(resolved_candidate_state_info["node_role"])
                    is NodeType.ARCHIVAL_MINER_NODE
                    and datetime.now()
                    >= datetime.fromisoformat(
                        resolved_candidate_state_info["consensus_timer_expiration"]
                    )
                ):
                    return ArchivalMinerNodeInformation(
                        miner_address=resolved_candidate_state_info["owner"],
                        source_host=URLAddress(each_candidate["source_address"]),
                        source_port=each_candidate["source_port"],
                    )

                logger.warning(
                    f"Archival Miner Candidate {resolved_candidate_state_info['owner']} seem to be mining but it was not labelled from the database? Please contact the developer as this may evolve as a potential problem sooner or later!"
                )

        logger.warning(
            f"All archival miner nodes seem to be busy. Attempting to find available nodes after the interval of the block timer. ({self.block_timer_seconds} seconds)"
        )
        return None

    def _get_last_block(self) -> Block | None:
        # ! This return seems confusing but I have to sacrafice for my own sake of readability.
        # @o First we access the list by calling the key 'chain'.
        # @o Since we got to the list, we might wanna get the last block by slicing the list with the use of its own length - 1 to get the last block.
        # @o But before we do that, ensure that last item has a content. Accessing the last item with the use of index while it doesn't contain anything will result in `IndexError`.

        if len(self._chain["chain"]):
            last_block_ref = Block.parse_obj(
                self._chain["chain"][len(self._chain["chain"]) - 1 :][0]
            )
            logger.debug(
                f"Last block has been fetched. Context | ID: {last_block_ref.id}, Hash: {last_block_ref.hash_block}, Date: {last_block_ref.contents.timestamp.isoformat()}"
            )

            return last_block_ref

        logger.warning("There's no block inside blockchain.")

    async def _get_own_certificate(self) -> str | None:
        if self.node_role is NodeType.ARCHIVAL_MINER_NODE:
            find_existing_certificate_query = select(
                [associated_nodes.c.certificate]
            ).where(associated_nodes.c.user_address == self.identity[0])

            return await self.db_instance.fetch_val(find_existing_certificate_query)

        logger.error(
            f"You cannot fetch your own certificate as a {NodeType.MASTER_NODE.name}!"
        )
        return None

    def _get_sizeof(self, *, block: Block) -> int | None:
        return asizeof(block)

    async def _get_content_data(
        self,
        *,
        data_type: BlockchainContentType,
        recently: bool = False,
        size: int = 5,
        content_id: str | None = None,
    ) -> None:

        # ! If we wanted to fetch everything then don't add size and put recently to False.

        return

    @restrict_call(on=NodeType.MASTER_NODE)
    async def _insert_internal_transaction(
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

        elif isinstance(data.context, NodeSyncTransaction) or isinstance(
            data.context, NodeCertificateTransaction
        ):
            resolved_from_address, resolved_to_address = (
                self.identity[0],
                data.context.requestor_address,
            )

        elif isinstance(data.context, NodeConsensusTransaction):
            resolved_from_address, resolved_to_address = (
                data.context.master_address,
                data.context.miner_address,
            )

        elif isinstance(data.context, NodeMinerProofTransaction):
            resolved_from_address, resolved_to_address = (
                data.context.receiver_address,
                data.context.miner_address,
            )

        else:
            resolved_from_address, resolved_to_address = self.identity[0], None

        if await self._resolve_transaction_payload(
            action=action,
            from_address=AddressUUID(
                resolved_to_address
                if resolved_to_address is not None
                else self.identity[0]
            ),
            to_address=AddressUUID(resolved_from_address),
            is_internal_payload=True,
            payload=data,
        ):
            return

        unconventional_terminate(message="Cannot resolve transaction.")

    # # Cannot do keyword arguments here as per stated on excerpt: https://stackoverflow.com/questions/23946895/requests-in-asyncio-keyword-arguments
    async def _mine_block(self, block: Block) -> Block:
        # If success, then return the hash of the block based from the difficulty.
        self.blockchain_ready = False
        prev: float = time()
        nth: int = 1

        logger.info(f"Attempting to mine a Block #{block.id} ...")

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
                self._consensus_calculate_sleep_time(mining_duration=time() - prev)
                self.blockchain_ready = True
                return block

            nth += 1

    async def _process_block_transactions(
        self,
    ) -> Any:
        # Processes the block along with the transactions, to be embedded from the blockchain (deserialize) or convert the block transactions object / datatype to a universally acceptable format.
        pass

    # Overwrites existing buffer from the frozendict if consensus has been established.
    async def _process_blockchain_file_to_current_state(
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
                        self._chain,
                        default=self._process_serialize_to_blockchain_file,
                    )

                    logger.debug(
                        f"Updating blockchain file's hash signature on database. | Targets: {BLOCKCHAIN_RAW_PATH}"
                    )
                    new_blockchain_hash: str = sha256(byte_json_content).hexdigest()

                    await self._update_chain_hash(new_hash=new_blockchain_hash)
                    await content_buffer.write(byte_json_content.decode("utf-8"))

                    logger.debug(
                        f"Blockchain's file signature has been changed! | Current Hash: {new_blockchain_hash}"
                    )
                else:
                    logger.warning(
                        "Bypass from the update method has been imposed. Attempting to insert data "
                    )
                    await self._update_chain_hash(new_hash=context_from_update[0])
                    await content_buffer.write(context_from_update[1])

                return self._chain

            else:
                raw_data = await content_buffer.read()
                partial_deserialized_data = import_raw_json_to_dict(raw_data)
                deserialized_data = (
                    self._process_deserialize_to_load_blockchain_in_memory(
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

    def _process_deserialize_to_load_blockchain_in_memory(
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

        self.new_master_instance = (  # # Redundant condition checking but better.
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
                self.cached_total_transactions = 0  # ! This means that we are resetting count back to zero because we are loading a new blockchain file.

            required_genesis_blocks: int = BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS  # ! We need to validate that there should be a set of required gensis blocks. If there are insufficient, then this blockchain as a whole is fraudalent.

            for block_idx, block_data in enumerate(context["chain"]):
                genesis_transaction_identifier: bool = False  # ! Additional switch to identify at least one genesis transaction per block.

                # @o For every block, we have to deserialize (1) the block itself, (2) contents of the block, which contains the transactions, (3) the payload as well as the (4) the signatures of the transactions.
                # - We are going to do this in reverse. Since doing this in ascending would prohibit due to existing cast of `frozendict` to each field.

                # - Check if there's a transaction first.
                if len(context["chain"][block_idx]["contents"]["transactions"]):

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
                            == TransactionActions.NODE_GENERAL_GENESIS_INITIALIZATION
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

                        self.cached_total_transactions += 1

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

                # - If cached_block_id is equal to dict_data["id"]. Then increment it easily.
                if self.cached_block_id == block_data["id"]:
                    self.cached_block_id += 1
                    logger.debug(
                        f"Block has a valid recent reference. | Currently (Incremented) Cached ID: {self.cached_block_id}, Recent Block ID (Decremented by 1): {block_data['id']}"
                    )

                # - However, when its not equal then then something is wrong.
                else:
                    unconventional_terminate(
                        message=f"Blockchain is currently unchained! (Currently Cached: {self.cached_block_id} | Block ID: {block_data['id']}) Some blocks are missing or is modified. This a developer-issue.",
                    )
                    return None

                if genesis_transaction_identifier and required_genesis_blocks:
                    required_genesis_blocks -= 1

            print(
                "DEBUG SWITCH ON LOAD",
                required_genesis_blocks,
                self.node_role is NodeType.MASTER_NODE,
                self.new_master_instance,
                required_genesis_blocks
                and self.node_role is NodeType.MASTER_NODE
                and not self.new_master_instance,
            )

            if (
                required_genesis_blocks
                and self.node_role is NodeType.MASTER_NODE
                and not self.new_master_instance
            ):
                unconventional_terminate(
                    message=f"This node's blockchain contains a potential fraudalent blocks! Though with the intention of using {NodeType.ARCHIVAL_MINER_NODE.name} for the possibility of finding the longest chain to recover, this may not be possible as of now. Please load any backup and replace the files then try again."
                )

            elif required_genesis_blocks and self.role is NodeType.ARCHIVAL_MINER_NODE:
                logger.error(
                    "This node's blockchain may be incomplete from the previous update, note that it will get updated after communicating with the master no`de."
                )
            else:
                logger.info(
                    f"The blockchain context from the file (via deserialiation) has been loaded in-memory and is secured by immutability! | Next Block ID is Block #{self.cached_block_id}."
                )

            self.blockchain_ready = True
            return frozendict(context)

        unconventional_terminate(
            message=f"The given `context` is not a valid dictionary object! | Received: {context} ({type(context)}). This is a logic error, please report to the developers as soon as possible.",
        )

    def _process_serialize_to_blockchain_file(self, o: frozendict) -> dict[str, Any]:
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

    async def _resolve_transaction_payload(
        self,
        *,
        action: TransactionActions,
        payload: ApplicantLogTransaction
        | ApplicantProcessTransaction
        | ApplicantUserTransaction
        | OrganizationTransaction
        | AdditionalContextTransaction
        | NodeTransaction,
        from_address: AddressUUID,
        to_address: AddressUUID | None,
        is_internal_payload: bool,  # @o Even though I can logically assume its a `Node-based transaction` when `to_address` is None, it is not possible since some `Node-based transactions` actually has a point to `address`.
    ) -> dict | bool:

        logger.debug(f"{payload} | {type(payload)}")

        if not any(
            isinstance(payload, context_model_candidates)
            for context_model_candidates in [
                ApplicantLogTransaction,
                ApplicantProcessTransaction,
                ApplicantUserTransaction,
                OrganizationTransaction,
                AdditionalContextTransaction,
                NodeTransaction,
            ]
        ):
            logger.error(
                f"The payload is not a valid pydantic object (got '{payload.__class__.__name__}'). Please refer to function signature for more information. This should not happen, report this issue to the  developer to resolve as possible."
            )
            return False

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
                constructed_context_to_key: bytes = (
                    str(action.value) + from_address[:7] + to_address[-12:] + timestamp
                ).encode("utf-8")
                encrypter_key = urlsafe_b64encode(constructed_context_to_key)

            else:
                logger.error(
                    "Payload is not internal transaction but `to_address` field is empty! This is an implementation error, please contact the developer regarding this issue."
                )
                return False

        encrypter_payload: Fernet = Fernet(encrypter_key)
        logger.debug(
            f"A key has been generated for the following action `{action}`. | Info: {encrypter_key.decode('utf-8')}"
        )

        payload_to_encrypt: ApplicantLogTransaction | ApplicantProcessTransaction | ApplicantUserTransaction | OrganizationTransaction | AdditionalContextTransaction | NodeTransaction = deepcopy(
            payload
        )

        if isinstance(payload_to_encrypt, NodeTransaction):
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
                from_address=AddressUUID(self.identity[0])
                if isinstance(payload_to_encrypt, NodeTransaction)
                else AddressUUID(from_address),
                to_address=AddressUUID(to_address) if to_address is not None else None,
            )
            print("DEBUG", built_internal_transaction)

        except PydanticValidationError as e:
            logger.error(f"There was an error during payload transformation. Info: {e}")
            return False

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

        # @o Append this and we are good to go!
        self.transaction_container.append(built_internal_transaction)
        logger.info(
            f"Transaction `{built_internal_transaction.tx_hash}` has been created and is on-queue for block generation!"
        )

        # - For user-based transactions, the method 'self.insert_external_transaction' waits for this method to finish for its transaction to get mapped from the blockchain. With that, let's return necessary contents.
        if not isinstance(payload_to_encrypt, NodeTransaction):
            return {
                "tx_hash": built_internal_transaction.tx_hash,
                "address_ref": to_address,
                "timestamp": timestamp,
            }

        return True

    async def _search_for(self, *, type: str, uid: AddressUUID | str) -> None:
        return

    def _set_node_state(self) -> None:
        self.node_ready = (
            True
            if not self.sleeping_from_consensus and self.is_blockchain_ready
            else False
        )

    @restrict_call(on=NodeType.ARCHIVAL_MINER_NODE)
    async def _update_chain(self) -> None:
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

            master_hash_valid_response = await self.http_instance.enqueue_request(
                url=URLAddress(
                    f"{master_node_props[REF_MASTER_BLOCKCHAIN_ADDRESS]}:{master_node_props[REF_MASTER_BLOCKCHAIN_PORT]}/node/blockchain/verify_hash"  # type: ignore
                ),
                method=HTTPQueueMethods.POST,
                await_result_immediate=True,
                headers={
                    "x-token": self.identity[1],
                    "x-certificate-token": await self._get_own_certificate(),
                    "x-hash": await self.get_chain_hash(),
                },
                do_not_retry=True,
                name="verify_local_hash_with_master_node",
            )

            if not master_hash_valid_response.ok:
                # - If that's the case then fetch the blockchain file.
                blockchain_content = await self.http_instance.enqueue_request(
                    url=URLAddress(
                        f"{master_node_props[REF_MASTER_BLOCKCHAIN_ADDRESS]}:{master_node_props[REF_MASTER_BLOCKCHAIN_PORT]}/node/blockchain/request_update"  # type: ignore
                    ),
                    method=HTTPQueueMethods.POST,
                    await_result_immediate=True,
                    headers={
                        "x-token": self.identity[1],
                        "x-certificate-token": await self._get_own_certificate(),
                    },
                    name="fetch_upstream_from_master_node",
                )

                # - For some reason, in my implementation, I also returned the hash with respect to the content.
                if blockchain_content.ok:
                    dict_blockchain_content = await blockchain_content.json()

                    in_memory_chain: frozendict | None = (
                        self._process_deserialize_to_load_blockchain_in_memory(
                            import_raw_json_to_dict(dict_blockchain_content["content"])
                        )
                    )

                    if not isinstance(in_memory_chain, frozendict):
                        logger.error(
                            "There was an error duing loading the blockchain from file to in-memory. It should not be possible to get on this condition as the method already handles it. But since we are in async state, please wait for it to terminate."
                        )
                        await sleep(INFINITE_TIMER)

                    else:
                        self._chain = in_memory_chain

                    # ! Once we inject the new payload after fetch, then write it from the file.

                    await self._process_blockchain_file_to_current_state(
                        operation=BlockchainIOAction.TO_WRITE,
                        context_from_update=(
                            HashUUID(dict_blockchain_content["current_hash"]),
                            BlockchainFileContext(dict_blockchain_content["content"]),
                        ),
                        bypass_from_update=True,
                    )

                    # - Record this to the blockchain.
                    await self._insert_internal_transaction(
                        action=TransactionActions.NODE_GENERAL_CONSENSUS_BLOCK_SYNC,
                        data=NodeTransaction(
                            action=NodeTransactionInternalActions.SYNC,
                            context=NodeSyncTransaction(
                                requestor_address=AddressUUID(self.identity[0]),
                                timestamp=datetime.now(),
                            ),
                        ),
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

    async def _update_chain_hash(self, *, new_hash: str) -> None:
        blockchain_hash_update_query: Update = (
            file_signatures.update()
            .where(file_signatures.c.filename == BLOCKCHAIN_NAME)
            .values(hash_signature=new_hash)
        )

        await self.db_instance.execute(blockchain_hash_update_query)


# # This approach was (not completely) taken from stackoverflow.
# * Please refer to the node/core/email.py for more information.
blockchain_service: BlockchainMechanism | None = None


def get_blockchain_instance(
    *,
    role: NodeType | None = None,
) -> BlockchainMechanism:

    global blockchain_service
    token_ref: IdentityTokens | None = get_identity_tokens()

    logger.debug("Initializing or returning blockchain instance ...")

    if role and blockchain_service is None and token_ref is not None:
        # # Note that this will create an issue later when we tried ARCHIVAL_MINER_NODE node mode later on.
        blockchain_service = BlockchainMechanism(
            auth_tokens=token_ref,
            node_role=role,
        )

    # If there are no resulting objective, then we can log this as an error, otherwise return the object.
    if blockchain_service is None:
        logger.critical("There are no blockchain instance.")

    if token_ref is None:
        logger.critical(
            "There are no identity tokens inferred from your instance. A login authentication should not bypass this method from running. This a developer issue, please report as possible or try again."
        )

    logger.debug("Blockchain instance retrieved, returning to the requestor ...")
    return blockchain_service  # type: ignore # Not sure how can I comprehend where's the mistake, or I just got caffeine overdose to understand mypy's complaint.
