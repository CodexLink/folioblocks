from asyncio import create_task, get_event_loop, sleep
from copy import deepcopy
from datetime import datetime, timedelta
from email.mime import application
from hashlib import sha256
from logging import Logger, getLogger
from secrets import token_urlsafe
from sqlite3 import IntegrityError
from sys import maxsize as MAX_INT_PYTHON
from time import time
from typing import Any, Callable, Final
from uuid import uuid4

from aiofiles import open as aopen
from fastapi import UploadFile
from blueprint.models import (
    applications,
    associations,
    associated_nodes,
    file_signatures,
    users,
)
from blueprint.schemas import (
    ApplicantLogTransaction,
    ApplicantProcessTransaction,
    ApplicantUserTransactionInitializer,
    Block,
    BlockOverview,
    HashableBlock,
    NodeConsensusInformation,
    NodeMasterInformation,
    NodeTransaction,
    Transaction,
)
from cryptography.fernet import Fernet
from databases import Database
from frozendict import frozendict
from blueprint.schemas import (
    AdditionalContextTransaction,
    TransactionSignatures,
)
from orjson import dumps as export_to_json
from orjson import loads as import_raw_json_to_dict
from pydantic import ValidationError as PydanticValidationError
from pympler.asizeof import asizeof
from sqlalchemy import select
from blueprint.schemas import OrganizationTransactionInitializer
from core.constants import ADDRESS_UUID_KEY_PREFIX, RawData
from blueprint.schemas import (
    ApplicantUserTransaction,
    OrganizationTransaction,
)
from node.core.constants import EmploymentApplicationState, RandomUUID
from utils.processors import validate_user_address
from utils.processors import hash_context
from utils.http import HTTPClient, get_http_client_instance
from utils.processors import unconventional_terminate

from core.consensus import ConsensusMechanism
from core.constants import (
    ASYNC_TARGET_LOOP,
    BLOCK_HASH_LENGTH,
    BLOCKCHAIN_HASH_BLOCK_DIFFICULTY,
    BLOCKCHAIN_MINIMUM_TRANSACTIONS_TO_BLOCK,
    BLOCKCHAIN_NAME,
    BLOCKCHAIN_RAW_PATH,
    BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS,
    BLOCKCHAIN_WAIT_TIME_REFRESH_FOR_TRANSACTION,
    REF_MASTER_BLOCKCHAIN_ADDRESS,
    REF_MASTER_BLOCKCHAIN_PORT,
    AddressUUID,
    AssociatedNodeStatus,
    BlockchainContentType,
    BlockchainFileContext,
    BlockchainIOAction,
    BlockchainPayload,
    HashUUID,
    HTTPQueueMethods,
    IdentityTokens,
    NodeType,
    TransactionActions,
    TransactionStatus,
    URLAddress,
    random_generator,
)
from core.dependencies import (
    get_database_instance,
    get_identity_tokens,
    get_master_node_properties,
)
from sqlalchemy.sql.expression import Insert, Update

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
        self.consensus_timer: timedelta = timedelta(
            seconds=0
        )  # TODO: This will be computed based on the information by the MASTER_NODE on how much is being participated, along with its computed value based on the average mining and iteration.

        self.transaction_container: list[Transaction] = []
        self.hashed_block_container: list[Block] = []
        self.unsent_block_container: list[Block] = []

        # # Instances
        self.db_instance: Final[Database] = get_database_instance()
        self.http_instance: HTTPClient = get_http_client_instance()
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

    # - Parameterized Decorator | Based: https://www.geeksforgeeks.org/creating-decorator-inside-a-class-in-python/, Adapted from https://stackoverflow.com/questions/5929107/decorators-with-parameters
    def __ensure_blockchain_ready(message: str = "Blockchain system is not yet ready!", terminate_on_call: bool = False) -> Callable:  # type: ignore
        def deco(fn: Callable) -> Callable:
            def instance(
                self: Any, *args: list[Any], **kwargs: dict[Any, Any]
            ) -> Callable | None:
                if self.is_blockchain_ready:
                    return fn(self, *args, **kwargs)

                # TODO: Why do we have this?
                if terminate_on_call:
                    unconventional_terminate(message=message)

                return None

            return instance

        return deco

    def __restrict_call(*, on: NodeType) -> Callable:  # type: ignore
        """
        Restricts the method to be called depending on their `self.role`.
        Since most of the methods is designed respectively based on their role.
        Ever process requires this certain role to only call this method and nothing else.

        Args:
                on (NodeType): The `role` of the node.

        Returns:
                Callable: Calls the decorator method.

        Notes:
        # This was duplicated, it was originated from the consensus.py.
        # I cannot get it because its inside of the class and it doesn't get shared because it has not `self` attribute.
        """

        def deco(fn: Callable) -> Callable:
            def instance(
                self: Any, *args: list[Any], **kwargs: dict[Any, Any]
            ) -> Callable | None:
                if self.role == on:
                    return fn(self, *args, **kwargs)

                self.warning(
                    f"Your role {self.role} cannot call the following method `{fn.__name__}` due to role restriction, which prohibits '{on}' from accessing this method."
                )
                return None

            return instance

        return deco

    async def initialize(self) -> None:
        """
        # A method that initialize resources needed for the blockchain system to work.
        """

        # - Load the blockchain for both nodes.
        self._chain: frozendict = await self._process_blockchain_file_to_current_state(
            operation=BlockchainIOAction.TO_READ
        )

        if self.node_role == NodeType.MASTER_NODE:
            # - New instances is indicated when this node doesn't contain any blocks on load. To avoid consensus timer on new instance, we have this switch to ensure that new blocks on fetch has been processed. Also note that this will be turned-around when there's a context.
            self.new_master_instance = True if not len(self._chain["chain"]) else False

            # * Check if there's a context inside of the JSON. If there's none then create 1 to 3 genesis blocks.
            if (
                self._chain is not None
                and "chain" in self._chain
                and not self._chain["chain"]
            ):
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

            create_task(self._block_timer_executor())

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

    @__restrict_call(on=NodeType.MASTER_NODE)
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

            # - [1] Ensure that the from_address is existing.
            # ! For the sake of complexity and due to my knowledge upon using JOIN statement.
            # ! I will be dividing those two statements.
            get_existing_from_address_stmt, get_existing_to_address_stmt = select(
                [users.c.unique_address]
            ).where(users.c.unique_address == from_address), select(
                [users.c.unique_address]
            ).where(
                users.c.unique_address == to_address
            )

            (
                existing_from_address,
                existing_to_address,
            ) = await self.db_instance.fetch_one(
                get_existing_from_address_stmt
            ), await self.db_instance.fetch_one(
                get_existing_to_address_stmt
            )

            # @o If all fetched addresses has context (as `str`), proceed.
            # ! These addresses will either contain a `str` or a `None` (`NoneType`).
            # ! If one of them contains `None` or `NoneType` this statement will result to false.
            if all(
                fetched_address is not None
                for fetched_address in [existing_to_address, existing_from_address]
            ):

                # @o Declared for type-hint. Initialized on some conditions.
                resolved_context: AdditionalContextTransaction | ApplicantLogTransaction | ApplicantProcessTransaction | ApplicantUserTransaction | OrganizationTransaction

                # - [2] Verify if action (TransactionAction) to TransactionContextMappingType is viable.
                # # [4]

                # - For the applicant application attempt actions.
                if action in [
                    TransactionActions.APPLICANT_APPLY,
                    TransactionActions.APPLICANT_APPLY_CONFIRMED,
                    TransactionActions.APPLICANT_APPLY_REJECTED,
                ] and isinstance(data, ApplicantProcessTransaction):

                    # * Since this was a new entry, we need to do some handling for the database entry.
                    try:
                        # * It doesn't matter beyond this point if the user tries again or not, we cannot handle that for now. See `CANNOT DO` of TODO.
                        if action is TransactionActions.APPLICANT_APPLY:
                            application_process_stmt: Insert | Update = (
                                applications.insert().values(
                                    process_id=RandomUUID(token_urlsafe(16)),
                                    requestor=data.requestor,
                                    to=data.receiver,
                                    state=EmploymentApplicationState.REQUESTED,
                                )
                            )
                        else:
                            application_process_stmt = (
                                applications.update()
                                .where(applications.c.process_uuid == data.process_id)
                                .values(
                                    state=EmploymentApplicationState.ACCEPTED
                                    if action
                                    is TransactionActions.APPLICANT_APPLY_CONFIRMED
                                    else EmploymentApplicationState.REJECTED
                                )
                            )

                        await self.db_instance.execute(application_process_stmt)

                    except IntegrityError as e:
                        logger.error(
                            f"There was an error regarding application process entry to database. | Info: {e}"
                        )

                    resolved_context = data

                # - For transactions that require generation of `user` under Organization or as an Applicant.
                elif action in [
                    TransactionActions.INSTITUTION_ORG_GENERATE_APPLICANT,
                    TransactionActions.ORGANIZATION_USER_REGISTER,
                ] and (
                    isinstance(data, ApplicantUserTransactionInitializer)
                    or isinstance(data, OrganizationTransactionInitializer)
                ):
                    # @d While we do understand that exposing the context as a whole, specifically with the credentials involved, it is going to be a huge loophole.
                    # @d With that, we need to seperate this transaction with Internal and External.
                    # @o XXXInternal -> Contains fields that is classified as credentials.
                    # @o XXXExternal -> Contains fields that does not contain anything sensitive as it only describes something out of context.

                    # @o Since XXXInternal subclasses XXXExternal, we only need `Internal` and break down until we get to the `XXXExternal`.

                    # - Validate conditions before user generation.
                    if (
                        isinstance(data, ApplicantUserTransactionInitializer)
                        and data.association_address is None
                        and data.association_name is None
                        and data.association_group_type is None
                    ):
                        logger.error(
                            "Association context is empty. Please add references as it is required to identify where do you belong. This is a developer-issue, please contact as possible."
                        )
                        return False

                    elif isinstance(data, OrganizationTransactionInitializer):

                        # - Validate if there's an association under the following condition.
                        if (
                            data.association_address is not None
                            and data.association_group_type is not None
                            and data.association_name is None
                        ):
                            validate_existence_association_stmt = select(
                                [associations.c.address]
                            ).where(associations.c.address == data.association_address)

                            validated_association = await self.db_instance.fetch_one(
                                validate_existence_association_stmt
                            )

                            if validated_association is None:
                                logger.error(
                                    "The supplied parameter for the `association` address reference does not exist! This is a developer-issue, please contact as possible."
                                )
                                return False

                        # - Create an organization when name is only provided assuming its a new instance.
                        elif (
                            data.association_address is None
                            and data.association_group_type is not None
                            and data.association_name is not None
                        ):
                            generated_address: Final[AddressUUID] = AddressUUID(
                                f"{ADDRESS_UUID_KEY_PREFIX}:{uuid4().hex}"
                            )

                            new_association_stmt = associations.insert().values(
                                address=generated_address,
                                name=data.association_name,
                                group=data.association_group_type,
                            )

                            await self.db_instance.execute(new_association_stmt)

                            # @o Since our approach is cascading, we need to assign this `generated_address` instead so that we don't need to do some resolution steps to get the newly inserted association address from the database again.
                            data.association_address = generated_address

                        else:
                            logger.error(
                                "Condition regarding `association` and `association_name` were unmet. Please refer to the developer for more information on how to use the API."
                            )

                    else:
                        logger.error(
                            f"Instances has condition unmet. Either the `association` contains nothing or the instance along with the `association` condition does not met. Please try again."
                        )

                    # @o When all of the checks are done, then create the user.
                    try:
                        insert_user_stmt = users.insert().values(
                            association=data.association_address,
                            first_name=data.first_name,
                            last_name=data.last_name,
                            email=data.email,
                            username=data.username,
                            password=hash_context(pwd=RawData(data.password)),
                        )

                        await self.db_instance.execute(insert_user_stmt)

                    except IntegrityError as e:
                        logger.error(
                            f"There was an error during account generation. This may likely be a cause of duplication or uniqueness issue. Please check your credentials and try again. | Info: {e}"
                        )
                        return False

                    # @o After that, its time to resolve those context for the `External` (for the blockchain to record).
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

                    # TODO: Declare this variable on the top.
                    resolved_context = (
                        ApplicantUserTransaction(**removed_credentials_context)
                        if isinstance(data, ApplicantUserTransactionInitializer)
                        else OrganizationTransaction(**removed_credentials_context)
                    )

                # - For the invocation of log for the Applicant under enum `ApplicantLogTransaction`.
                # @o This needs special handling due to the fact that it may contain an actual file.
                # ! There's a need of special handling from the API endpoint receiver due to its nature of using content-type: multipart/form-data. Therefore, this method expects to have an `ApplicantLogTransaction`.
                elif (
                    action is TransactionActions.INSTITUTION_ORG_REFER_NEW_DOCUMENT
                    and isinstance(data, ApplicantLogTransaction)
                ):
                    if (
                        data.entity_address_ref is not None
                        and await validate_user_address(
                            supplied_address=AddressUUID(data.entity_address_ref)
                        )
                    ):

                        if isinstance(data.file, UploadFile):
                            # @o We combine the current time under isoformat string + given filename + referred user address in full length.

                            # ! We need to create our own key because we are going to access these files.

                            # * Since this project is under repository, we will keep it this way.
                            # * In actual real world, we ain't gonna be doing this.

                            # @o Create the key based from the user address (target or `to`), truncated from the first 12 character + datetime in custom format, please see the variable `current_date` below.

                            timestamp: datetime = datetime.now()
                            current_date: str = timestamp.strftime("%y%m%d%H%M%S")
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
                            # - And replace it on the field of the data.file so that nothing will be loss.
                            data.file = HashUUID(
                                sha256(
                                    raw_context.encode("utf-8")
                                    if isinstance(raw_context, str)
                                    else raw_context
                                ).hexdigest()
                            )

                        # - Do the following for all condition.
                        data.entity_address_ref = None
                        resolved_context = data

                    else:
                        return False

                # - For the `extra` fields of both `ApplicantTransaction` and `OrganizationTransaction`.
                # # [2]
                elif action in [
                    TransactionActions.ORGANIZATION_REFER_EXTRA_INFO,
                    TransactionActions.INSTITUATION_ORG_APPLICANT_REFER_EXTRA_INFO,
                ] and isinstance(data, AdditionalContextTransaction):
                    # * Just validate if the specified entity address does exists.

                    if (
                        data.entity_address_ref is not None
                        and not validate_user_address(
                            supplied_address=AddressUUID(data.entity_address_ref)
                        )
                    ):
                        data.entity_address_ref = None
                        resolved_context = data

                else:
                    logger.error(
                        "There was an error during conditional check. Are you sure this combination is right? Please check the declaration and try again."
                    )
                    return False

                # - [File]
                try:
                    # Transaction(action=)

                    return True

                except PydanticValidationError as e:
                    logger.error(
                        f"There was an error during payload transformation. Info: {e}"
                    )
                    return False

            logger.error(
                f"{'Sender' if existing_from_address is None else 'Receiver'} address seem to be invalid. Please check your input and try again. This transaction will be inserted disregarded."
            )  # TODO: Send to email when this happened, only when `from_address` exists.

        logger.error(
            f"There was a missing or invalid parameter of the following parameters: `action`, `from_address` and `data`. `action` requires to have a value of an Enum `TransactionActions`, `from_address` should contain a valid string and `data` may not be a pydantic model! Please encapsulate your `data` to one of the following pydantic models: {[each_model.__name__ for each_model in supported_models]}."
        )
        return False

        # - Attempt to recognize the action by referring to the instance of the data.

    @__ensure_blockchain_ready()
    def get_blockchain_public_state(self) -> NodeMasterInformation | None:
        if self.node_role == NodeType.MASTER_NODE:

            # # This may not be okay.
            return NodeMasterInformation(
                chain_block_timer=self.block_timer_seconds,
                total_blocks=len(self._chain["chain"])
                if self._chain is not None
                else 0,
                total_transactions=self.cached_total_transactions
                # total_transactions=len(
                #     self._get_content_data(data_type=BlockchainContentType.TRANSACTION),  # type: ignore
                # ),
            )
        logger.critical(
            f"This client node requests for the `public_state` when their role is {self.node_role}! | Expects: {NodeType.MASTER_NODE}."
        )
        return None

    @__ensure_blockchain_ready()
    def get_blockchain_private_state(self) -> NodeConsensusInformation:
        last_block: Block | None = self._get_last_block()

        return NodeConsensusInformation(
            consensus_timer_seconds=self.consensus_timer.total_seconds(),
            is_mining=not self.is_blockchain_ready,
            is_sleeping=self.is_node_ready,
            last_mined_block=last_block.id if last_block is not None else 0,
            node_role=self.role,
            owner=self.auth_token[0],
        )

    async def get_chain_hash(self) -> HashUUID:
        fetch_chain_hash_stmt = select([file_signatures.c.hash_signature]).where(
            file_signatures.c.filename == BLOCKCHAIN_NAME
        )

        return HashUUID(await self.db_instance.fetch_val(fetch_chain_hash_stmt))

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

    @__ensure_blockchain_ready()
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
        context: Block | Transaction,
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
            block_context = context.dict()
            block_context["contents"] = frozendict(block_context["contents"])

            # @o If a certain block has been inserted in a way that it is way over far or less than the current self.cached_block_id, then disregard this block.
            if block_context["id"] != self.cached_block_id:
                logger.error(
                    f"This block #{block_context['id']} is way too far or behind than the one that is saved in the local blockchain file. Will attempt to fetch a new blockchain file from the MASTER_NODE node. This block will be DISREGARDED."
                )
                return

            self._chain["chain"].append(frozendict(block_context))
            self.cached_block_id += 1
            await self._process_blockchain_file_to_current_state(
                operation=BlockchainIOAction.TO_WRITE
            )
            await self._consensus_sleeping_phase()

        else:
            unconventional_terminate(
                message="There's no 'chain' from the root dictionary of blockchain! This is a developer-implementation issue, please report to the developers as soon as possible!",
            )

    @__restrict_call(on=NodeType.MASTER_NODE)
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
            available_node: NodeConsensusInformation | None = (
                await self._get_available_archival_miner_nodes()
            )

            # @o When there's no miner, then sleep for a while and requeue again.
            if available_node is None:
                continue

            print("Available node get!", available_node)

            # @o When there's a miner, do a closed-loop process.

            # @o To save some processing time, we need to have a sufficient transactions before we process them to a block.
            # - Wait until a number of sufficient transactions were received.
            # - Since we already have a node, do not let this one go.
            if (
                len(self.transaction_container)
                > BLOCKCHAIN_MINIMUM_TRANSACTIONS_TO_BLOCK
            ):

                logger.info(
                    f"Number of required transactions were sufficient! There are {len(self.transaction_container)} transactions that will be converted to a block for processing."
                )

                # @o We need to deepcopy the container to ensure that when we did something from them, the source of this transactions are not modified.
                # @o Note that whenever you pass an object, specially the `dict` objects, their reference is not mangled or not referred as a new object.
                # @o With that, any changes being done to one object will be reflected from the other object that you recently modified, this was due to references were still the same.
                # - Create a deepcopy of the object to process its last state.
                last_state_transaction_container = deepcopy(self.transaction_container)

                # - Create a block from all of the transactions.
                generated_block: Block | None = self._create_block(
                    transactions=last_state_transaction_container
                )

            elif len(self.unsent_block_container):
                logger.info(
                    f"Block {self.unsent_block_container[0]} has been left from mining due to previous miner unable to respond in time. Using this block to for the process instead."
                )

                generated_block = self.unsent_block_container.pop(0)

                return  # TODO

                # @o When a block was created. Create a negotiation ID for the nodes to remember that this happened.

                # - Create a negotiation ID based on the certificate token of the available miner node as well as this master under SHA256 form + datetime.

                # @o Even though we already have the certification token, we still need this one to prove that we are actually know what the heck are we doing and we should be remembering it since it contains transactions or tokens which shouldn't go loss.

                # - Insert the negotiation ID.

                # # Send the context via create_task() with a custom function with retry_attempts of 99.
                # # As deliver_block_or_store().

                # # Send it at node/blockchain/send_raw_block.
                # @o Require certification, and insert the negotiation ID for it to be sent later.

                # - If that failed after numerous retries then insert the block as unsent_blocks.
                # - And unbind the negotiation ID.

                # ! Repeat.

                # * The miner node has to hit the endpoint along with the negotiation ID for it to give its final processed block.

                # # TODO AS FINAL.
                # Prune the transaction container beyond this point.
                # self.transaction_container = [leftover_transactions for leftover_transactions in self.]
            else:
                logger.warning(
                    f"There isn't enough transactions to create a block. Awaiting for new transactions in {BLOCKCHAIN_WAIT_TIME_REFRESH_FOR_TRANSACTION} seconds."
                )

                await sleep(BLOCKCHAIN_WAIT_TIME_REFRESH_FOR_TRANSACTION)

            # # MOVE THE REST AFTER CONFIRMING THE FLOW FROM ALL CONDITIONALS.

            # TODO: process_hashed_block.

            # NOTE: After all of these, file handling left and we are done with the core backend =).

            # However, when there's a time that this chosen node is not available, then it will be skipped.

    def _consensus_calculate_sleep_time(self, *, mine_duration: float | int) -> None:
        if not self.is_blockchain_ready and not self.new_master_instance:
            self.consensus_timer = timedelta(
                seconds=mine_duration
            )  # TODO: Get the average mining seconds to confluence with the timer.
            logger.debug(
                f"Consensus timer is calculated. Set to {self.consensus_timer.total_seconds()} seconds before waking. | Object: {self.consensus_timer}"
            )

    async def _consensus_sleeping_phase(self) -> None:
        if not self.new_master_instance:
            self.sleeping_from_consensus = True

            logger.info(
                f"Block mining is finished. Sleeping for {self.consensus_timer.total_seconds()} seconds."
            )

            await sleep(self.consensus_timer.total_seconds())
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

    def _create_block(
        self,
        *,
        transactions: list[Transaction] | None,
    ) -> Block | None:

        # @o When building a block, we first have to consider that there are some properties were undefined. The nonce, block_size, and hash_block.
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

        _block: Block = Block(
            id=self.cached_block_id,
            block_size=None,  # * Unsolvable at instantiation but can be filled before returning it.
            hash_block=None,  # ! Unsolvable, mine_block will handle it.
            prev_hash_block=HashUUID("0" * BLOCK_HASH_LENGTH) if last_block is None else HashUUID(last_block.hash_block),  # type: ignore
            contents=HashableBlock(
                nonce=None,  # ! Unsolvable, these are determined during the process of mining.
                validator=self.identity[0],
                transactions=transactions,
                timestamp=datetime.now(),
            ),
        )

        _block.block_size = asizeof(_block.contents.json())

        logger.info(
            f"Block #{_block.id} with a size of ({_block.block_size} bytes) has been created."
        )

        return _block

    async def _create_genesis_block(self) -> None:
        """
        Generates a block, hash it and append it within the context of the blockchain, for both the file and the in-memory.
        """

        # Check for the genesis_block before inserting it.
        # TODO: We may need to use create_block since we have an unallocated_block.

        mined_genesis_block = await (
            get_event_loop().run_in_executor(
                None,
                self._mine_block,
                self._create_block(transactions=None),
            )
        )

        await self._append_block(context=mined_genesis_block)

    async def _get_available_archival_miner_nodes(
        self,
    ) -> NodeConsensusInformation | None:
        # Get all available miner nodes.

        available_nodes_stmt = select(
            [
                associated_nodes.c.user_address,
                associated_nodes.c.source_address,
                associated_nodes.c.source_port,
            ]
        ).where(associated_nodes.c.status == AssociatedNodeStatus.CURRENTLY_AVAILABLE)

        available_nodes = await self.db_instance.fetch_all(available_nodes_stmt)

        if not len(available_nodes):
            logger.info(
                f"There are no available nodes to mine the block. Retrying again the after interval of the block timer. ({self.block_timer_seconds} seconds)"
            )
            return None

        logger.info(f"There are {len(available_nodes)} candidates available!")

        for each_candidate in available_nodes:
            candidate_response = await get_http_client_instance().enqueue_request(
                url=URLAddress(
                    f"http://{each_candidate['source_address']}:{each_candidate['source_port']}/node/info"
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

                if not resolved_candidate_state_info["is_mining"]:
                    if (
                        resolved_candidate_state_info["node_role"]
                        == NodeType.ARCHIVAL_MINER_NODE.name
                    ):
                        return NodeConsensusInformation(**resolved_candidate_state_info)

                    continue
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
        if self.node_role == NodeType.ARCHIVAL_MINER_NODE:
            find_existing_certificate_stmt = select(
                [associated_nodes.c.certificate]
            ).where(associated_nodes.c.user_address == self.identity[0])

            return await self.db_instance.fetch_val(find_existing_certificate_stmt)

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

    @__restrict_call(on=NodeType.MASTER_NODE)
    async def _insert_internal_transaction(
        self, action: TransactionActions, data: NodeTransaction
    ) -> None:

        if not isinstance(data, NodeTransaction) or action not in TransactionActions:
            logger.error(
                f"Passed parameters is invalid. Please ensure that `data` is instance of `{NodeTransaction}` and `action` has an enum member candidate to `{TransactionActions}`"
            )
            return None

        # @o Since we can see some patterns for the Node-based Transactions, instead of explicitly declaring them, we are going to use its name with a prefix finder.
        if not action.name.startswith("NODE_GENERAL_"):
            logger.error(
                "The parameter `action` is invalid. Please invoke `TransactionActions` with enum members prefixes starts with `NODE_GENERAL_`."
            )
            return None

        # - Prepare the context encrypter.
        key_payload: bytes = Fernet.generate_key()

        encrypter_payload: Fernet = Fernet(key_payload)
        logger.debug(
            f"Keys has been generated for the action {action}. | Info: {key_payload.decode('utf-8')}"
        )

        # - Deepcopy the `data` (NodeTransaction) and encrypt its context.
        data_encrypted: NodeTransaction = deepcopy(data)
        data_encrypted.context = HashUUID(
            (encrypter_payload.encrypt(export_to_json(data.context))).decode("utf-8")
        )

        # - Build the transaction
        built_transaction: Transaction = Transaction(
            tx_hash=None,
            action=action,
            status=TransactionStatus.SUCCESS,
            payload=NodeTransaction(**data_encrypted.dict()),
            signatures=TransactionSignatures(
                raw=HashUUID(sha256(export_to_json(data.dict())).hexdigest()),
                encrypted=HashUUID(
                    sha256(export_to_json(data_encrypted.dict())).hexdigest()
                ),
            ),
            from_address=AddressUUID(self.identity[0]),
            to_address=None,
            timestamp=datetime.now(),
        )

        # @o Since we now have a copy of the 'premature' transaction, we calculate its hash.
        premature_transaction_copy: dict = built_transaction.dict()

        # @o We don't want to influence `tx_hash` from this even though its a `NoneType`.
        del premature_transaction_copy["tx_hash"]

        # - Calculate
        premature_calc_sha256: str = sha256(
            export_to_json(premature_transaction_copy)
        ).hexdigest()

        # @o After calculation, invoke this new hash from the `tx_hash` of the built_transaction.
        built_transaction.tx_hash = HashUUID(premature_calc_sha256)

        # @o Append this and we are good to go!
        self.transaction_container.append(built_transaction)
        logger.info(
            f"Transaction {built_transaction.tx_hash} has been created and is on-queue for block generation!"
        )

        return None

    # # Cannot do keyword arguments here as per stated on excerpt: https://stackoverflow.com/questions/23946895/requests-in-asyncio-keyword-arguments
    def _mine_block(self, block: Block) -> Block:
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
                self._consensus_calculate_sleep_time(mine_duration=time() - prev)
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
    ) -> frozendict:
        if operation in BlockchainIOAction:
            async with aopen(
                BLOCKCHAIN_RAW_PATH,
                "w" if operation == BlockchainIOAction.TO_WRITE else "r",
            ) as content_buffer:

                if operation == BlockchainIOAction.TO_WRITE:

                    if not bypass_from_update and not len(context_from_update):
                        byte_json_content: bytes = export_to_json(
                            self._chain,
                            default=self._process_serialize_to_file_blockchain,
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
                    deserialized_data = self._process_deserialize_to_load_blockchain(
                        partial_deserialized_data
                    )
                    logger.info(
                        f"Chain has been loaded from the file to the in-memory!"
                    )

                    return deserialized_data

        unconventional_terminate(
            message=f"Supplied value at 'operation' is not a valid enum! Got {operation} ({type(operation)}) instead. This is an internal error.",
        )
        return None

    def _process_deserialize_to_load_blockchain(
        self,
        context: dict[str, Any],
    ) -> frozendict:
        """
        A method that deserializes the universally readable (JSON) format from the blockchain file into an immutable dictionary (frozendict) containing a series of pydantic objects.

        Args:
            context (dict[str, Any]): The consumable data (type-compatible) that is loaded by the orjson.

        Returns:
            frozendict: Returns the immutable version of the given `context`.
        """

        # *  Ensure that the wrapped object is 'dict' regardless of their recent forms.
        if isinstance(context, dict):

            for dict_idx, dict_data in enumerate(context["chain"]):
                # * For every block, we have to deserialize (1) timestamps to `datetime`, (2) `content` to immutable 'dict' (frozendict) and transactions.

                context["chain"][dict_idx]["contents"] = frozendict(
                    dict_data["contents"]
                )
                # * Then, make the whole block immutable and insert it as reference from the blockchain.
                context["chain"][dict_idx] = frozendict(dict_data)

                # @o Check backward reference from the current block to recent block.
                if dict_idx:  # ! Mind the zero-based list access.
                    if (
                        dict_data["prev_hash_block"]
                        != context["chain"][dict_idx - 1]["hash_block"]
                    ):
                        logger.critical(
                            f"Block #{dict_data['id']}'s backward reference to Block #{dict_data['id'] - 1} is invalid! | Expects (from Current Block): {dict_data['hash_block']}, got {context['chain'][dict_idx - 1]['prev_hash_block']} instead."
                        )

                        logger.critical(
                            "Due to potential fraudalent local blockchain file, please wait for the `MASTER_NODE` node to acknowledge your replacement of blockchain file."
                        )
                        self.blockchain_ready = False

                        # # Create a task that waits for it to do something to fetch a valid blockchain file.

                    logger.info(
                        f"Block #{dict_data['id']} backward reference to Block# {dict_data['id'] - 1} is valid!"
                    )
                else:
                    logger.debug(
                        f"Block #{dict_data['id']} doesn't have a prev or leading block to compare reference, probably the latest block."
                    )

                # @o If cached_block_id is equal to dict_data["id"]. Then increment it easily.
                if self.cached_block_id == dict_data["id"]:
                    self.cached_block_id += 1
                    logger.debug(
                        f"Block has a valid recent reference. | Currently (Incremented) Cached ID: {self.cached_block_id}, Recent Block ID (Decremented by 1): {dict_data['id']}"
                    )

                # @o However, when its not equal then then something is wrong.
                else:
                    unconventional_terminate(
                        message=f"Blockchain is currently unchained! (Currently Cached: {self.cached_block_id} | Block ID: {dict_data['id']}) Some blocks are missing or is modified. This a developer-issue.",
                    )
                    return None

            logger.info(
                f"The blockchain context from the file (via deserialiation) has been loaded in-memory and is secured by immutability! | Next Block ID is Block #{self.cached_block_id}."
            )
            self.blockchain_ready = True
            return frozendict(context)

        unconventional_terminate(
            message=f"The given `context` is not a valid dictionary object! | Received: {context} ({type(context)}). This is a logic error, please report to the developers as soon as possible.",
        )

    def _process_serialize_to_file_blockchain(self, o: frozendict) -> dict[str, Any]:
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

                # * Lastly, cast mutability to the content of the whole block of the chain.
                _o["chain"][block_idx]["contents"] = dict(each_block["contents"])

            return _o

        raise TypeError

    # TODO: Ensure to follow the rule that we made last time.
    async def _search_for(self, *, type: str, uid: AddressUUID | str) -> None:
        pass

    def _set_node_state(self) -> None:
        self.node_ready = (
            True
            if not self.sleeping_from_consensus and self.is_blockchain_ready
            else False
        )

    @__restrict_call(on=NodeType.ARCHIVAL_MINER_NODE)
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
                    f"http://{master_node_props[REF_MASTER_BLOCKCHAIN_ADDRESS]}:{master_node_props[REF_MASTER_BLOCKCHAIN_PORT]}/node/blockchain/verify_hash"  # type: ignore
                ),
                method=HTTPQueueMethods.POST,
                await_result_immediate=True,
                headers={
                    "x-token": self.identity[1],
                    "x-certificate-token": await self._get_own_certificate(),
                    "x-hash": await self.get_chain_hash(),
                },
                do_not_retry=True,
            )

            if not master_hash_valid_response.ok:
                # - If that's the case then fetch the blockchain file.
                blockchain_content = await self.http_instance.enqueue_request(
                    url=URLAddress(
                        f"http://{master_node_props[REF_MASTER_BLOCKCHAIN_ADDRESS]}:{master_node_props[REF_MASTER_BLOCKCHAIN_PORT]}/node/blockchain/request_update"  # type: ignore
                    ),
                    method=HTTPQueueMethods.POST,
                    await_result_immediate=True,
                    headers={
                        "x-token": self.identity[1],
                        "x-certificate-token": await self._get_own_certificate(),
                    },
                )

                # - For some reason, in my implementation, I also returned the hash with respect to the content.

                if blockchain_content.ok:
                    dict_blockchain_content = await blockchain_content.json()

                    # TODO: Documentation.
                    # - When we got a result, pop from the asyncio._Tasks to expose the `ClientResponse`.
                    # - With that, parse the `ClientResponse` to be converted to a pythonic dictionary data type.
                    self._chain = self._process_deserialize_to_load_blockchain(
                        import_raw_json_to_dict(dict_blockchain_content["content"])
                    )

                    # ! Once we inject the new payload after fetch, then write it from the file.

                    await self._process_blockchain_file_to_current_state(
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

    async def _update_chain_hash(self, *, new_hash: str) -> None:
        blockchain_hash_update_stmt = (
            file_signatures.update()
            .where(file_signatures.c.filename == BLOCKCHAIN_NAME)
            .values(hash_signature=new_hash)
        )

        await self.db_instance.execute(blockchain_hash_update_stmt)


# # This approach was (not completely) taken from stackoverflow.
# * Please refer to the node/core/email.py:132 for more information.
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
