"""
API — Explorer and Node API for the Master Node.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""


from asyncio import create_task, gather
from datetime import datetime, timedelta
from http import HTTPStatus
from logging import Logger, getLogger
from os import environ as env

from blueprint.models import (
    associated_nodes,
    auth_codes,
    consensus_negotiation,
    tokens,
    users,
)
from blueprint.schemas import (
    AdditionalContextTransaction,
    ApplicantLogTransaction,
    ApplicantUserTransaction,
    ConsensusFromMasterPayload,
    ConsensusSuccessPayload,
    ConsensusToMasterPayload,
    GroupTransaction,
    NodeCertificateTransaction,
    NodeConfirmMineConsensusTransaction,
    NodeConsensusInformation,
    NodeInformation,
    NodeMasterInformation,
    NodeSyncTransaction,
    NodeTransaction,
    SourcePayload,
)
from core.blockchain import BlockchainMechanism, get_blockchain_instance
from core.constants import (
    ASYNC_TARGET_LOOP,
    BLOCKCHAIN_HASH_BLOCK_DIFFICULTY,
    AddressUUID,
    ApplicantLogContentType,
    AssociatedNodeStatus,
    AuthAcceptanceCode,
    BaseAPI,
    ConsensusNegotiationStatus,
    JWTToken,
    NodeAPI,
    NodeTransactionInternalActions,
    NodeType,
    SourceNodeOrigin,
    TransactionActions,
    TransactionContextMappingType,
    UserEntity,
    random_generator,
)
from core.dependencies import (
    EnsureAuthorized,
    generate_consensus_sleep_time,
    get_database_instance,
)
from cryptography.fernet import Fernet
from databases import Database
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Header,
    HTTPException,
    Response,
    UploadFile,
)
from fastapi.responses import JSONResponse
from pydantic import PydanticValueError
from sqlalchemy import func, select
from sqlalchemy.sql.expression import ClauseElement, Delete, Insert, Select, Update
from utils.processors import (
    validate_previous_consensus_negotiation,
    validate_source_and_origin_associates,
)

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

node_router = APIRouter(
    prefix="/node",
    tags=[BaseAPI.NODE.value],
)


@node_router.get(
    "/info",
    tags=[
        NodeAPI.GENERAL_NODE_API.value,
        NodeAPI.NODE_TO_NODE_API.value,
        NodeAPI.MASTER_NODE_API.value,
    ],
    response_model=NodeInformation,
    summary="Fetch information from the master node.",
    description="An API endpoint that returns information based on the authority of the client's requests. This requires special headers.",
    # # Notes: I left this one in open-air since there are no credentials to steal (maybe maybe maybe).
)
async def get_node_info() -> NodeInformation:
    blockchain_instance: BlockchainMechanism | None = get_blockchain_instance()

    if isinstance(blockchain_instance, BlockchainMechanism):
        node_state: NodeConsensusInformation = (
            blockchain_instance.get_blockchain_private_state()
        )
        node_statistics: NodeMasterInformation | None = (
            blockchain_instance.get_blockchain_public_state()
        )

        return NodeInformation(
            properties=node_state,
            statistics=node_statistics,
        )

    raise HTTPException(
        detail="Blockchain instance is not yet initialized to return blockchain's public and private states. Please try again later.",
        status_code=HTTPStatus.NO_CONTENT,
    )


"""
/consensus/echo | When received ensure its the master by fetching its info.
/consensus/acknowledge | When acknowledging, give something, then it will return something.

# Note that MASTER will have to do this command once! Miners who just finished will have to wait and keep on retrying.
/consensus/negotiate | This is gonna be complex, on MASTER, if there's current consensus negotiation then create a new one (token). Then return a consensus as initial from the computation of the consensus_timer.
/consensus/negotiate | When there's already a consensus negotiation, when called by MASTER, return the context of the consensus_timer and other properties that validates you of getting the block when you are selected.
/consensus/negotiate | When block was fetched then acknowledge it.
/consensus/negotiate | When the miner is done, call this one again but with a payload, and then keep on retrying, SHOULD BLOCK THIS ONE.
/consensus/negotiate | When it's done, call this again for you to sleep by sending the calculated consensus, if not right then the MASTER will send a correct timer.
/consensus/negotiate | Repeat.
# TODO: Actions should be, receive_block, (During this, one of the assert processes will be executed.)
"""


@node_router.post(
    "/receive_hashed_block",
    tags=[NodeAPI.NODE_TO_NODE_API.value, NodeAPI.MASTER_NODE_API.value],
    summary=f"Receives a hashed block for the {NodeType.MASTER_NODE} to append from the blockchain.",
    description=f"A special API endpoint that receives a raw bock to be mined.",
    dependencies=[
        Depends(
            EnsureAuthorized(
                _as=UserEntity.ARCHIVAL_MINER_NODE_USER, blockchain_related=True
            )
        )
    ],
    response_model=ConsensusSuccessPayload,
    status_code=HTTPStatus.ACCEPTED,
)
async def receive_hashed_block(
    context_from_archival_miner: ConsensusToMasterPayload,
    database_instance: Database = Depends(get_database_instance),
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance),
) -> ConsensusSuccessPayload:

    if isinstance(blockchain_instance, BlockchainMechanism):
        block_confirmed: bool = False
        block_equal_from_main: bool = True

        # - Validate the given block by checking its id and other fields that is outside from the context.
        for each_confirming_block in blockchain_instance.confirming_block_container:

            logger.debug(
                f"Block Compare (Confirming Block | Mined Block) |> ID: ({each_confirming_block.id} | {context_from_archival_miner.block.id}), Block Size Bytes: ({each_confirming_block.block_size_bytes} | {context_from_archival_miner.block.block_size_bytes}), Prev Hash Block: ({each_confirming_block.prev_hash_block} | {context_from_archival_miner.block.prev_hash_block}), Timestamp: ({each_confirming_block.contents.timestamp} | {context_from_archival_miner.block.contents.timestamp})"
            )

            # - From the current selected block, check if it match from the received block from the confirming blocks.
            if (
                (each_confirming_block.id == context_from_archival_miner.block.id)
                and each_confirming_block.block_size_bytes
                == context_from_archival_miner.block.block_size_bytes
                and each_confirming_block.prev_hash_block
                == context_from_archival_miner.block.prev_hash_block
                and context_from_archival_miner.block.hash_block[:BLOCKCHAIN_HASH_BLOCK_DIFFICULTY] == "0" * BLOCKCHAIN_HASH_BLOCK_DIFFICULTY  # type: ignore # ! This should contain something.
                and each_confirming_block.contents.timestamp
                == context_from_archival_miner.block.contents.timestamp
            ):

                block_confirmed = True  # - Unlock the path after the iterator to ensure that the block will be processed, based on its condition.

                # - When it matches, check if the received block's id is higher than the main_block_id.
                if (
                    context_from_archival_miner.block.id
                    > blockchain_instance.main_block_id
                ):
                    # - Append from the container.
                    blockchain_instance.hashed_block_container.append(
                        context_from_archival_miner.block
                    )
                    logger.warning(
                        f"Received-hashed block #{context_from_archival_miner.block.id} seem to be way to early to get here. Therefore, save it in the hashed block container to assess when `append_block` is called."
                    )

                    # - After appending the block from the `hashed_block_container`, sort it.
                    blockchain_instance.hashed_block_container.sort(
                        key=lambda block_context: block_context.id
                    )

                # - For equal block id, just remove it from the confirming block container and set that the block has been confirmed.
                else:
                    blockchain_instance.confirming_block_container.remove(
                        each_confirming_block
                    )  # - Remove from the container as it was already confirmed.

                    block_equal_from_main = True

                    break

        if not block_confirmed:
            raise HTTPException(
                detail="Cannot confirm any confirming blocks from the received mined block.",
                status_code=HTTPStatus.NO_CONTENT,
            )

        proposed_consensus_addon_timer: float = generate_consensus_sleep_time(
            block_timer=blockchain_instance.block_timer_seconds
        )

        # - Update the Consensus Negotiation ID.
        update_consensus_negotiation_query: Update = (
            consensus_negotiation.update()
            .where(
                (
                    consensus_negotiation.c.consensus_negotiation_id
                    == context_from_archival_miner.consensus_negotiation_id
                )
                & (
                    consensus_negotiation.c.status
                    == ConsensusNegotiationStatus.ON_PROGRESS
                )
            )
            .values(status=ConsensusNegotiationStatus.COMPLETED)
        )

        # - As well as the association of the miner node.
        update_associate_state_query: Update = (
            associated_nodes.update()
            .where(
                associated_nodes.c.user_address
                == context_from_archival_miner.miner_address
            )
            .values(
                status=AssociatedNodeStatus.CURRENTLY_AVAILABLE,
                consensus_sleep_expiration=context_from_archival_miner.hashing_duration_finished
                + timedelta(seconds=proposed_consensus_addon_timer),
            )
        )

        await gather(
            database_instance.execute(update_consensus_negotiation_query),
            database_instance.execute(update_associate_state_query),
        )

        # - Since we lost the identity value of the enums from the fields, we need to re-bind them so that the loaded block from memory has a referrable enum when called.
        for transaction_idx, transaction_context in enumerate(
            context_from_archival_miner.block.contents.transactions
        ):

            # - Resolve `action` field with `TransactionActions`.
            context_from_archival_miner.block.contents.transactions[
                transaction_idx
            ].action = TransactionActions(transaction_context.action)

            # - Resolve the `action` field from the payload's action `NodeTransaction`.
            if isinstance(
                context_from_archival_miner.block.contents.transactions[
                    transaction_idx
                ].payload,
                NodeTransaction,
            ):
                context_from_archival_miner.block.contents.transactions[  # type: ignore # ! Condition already resolved the issue of an attribute is missing.
                    transaction_idx
                ].payload.action = NodeTransactionInternalActions(
                    transaction_context.payload.action  # type: ignore # ! Condition already resolved the issue of an attribute is missing.
                )

            # - Resolve the `content_type` field from the payload's action `GroupTransaction`.
            elif isinstance(
                context_from_archival_miner.block.contents.transactions[
                    transaction_idx
                ].payload,
                GroupTransaction,
            ):
                context_from_archival_miner.block.contents.transactions[  # type: ignore # ! Condition already resolved the issue of an attribute is missing.
                    transaction_idx
                ].payload.content_type = TransactionContextMappingType(
                    transaction_context.payload.content_type  # type: ignore # ! Condition already resolved the issue of an attribute is missing.
                )

            else:
                logger.warning(
                    f"Transaction {context_from_archival_miner.block.contents.transactions[transaction_idx].tx_hash} payload cannot be casted with the following enumeration classes: {NodeTransaction} and {GroupTransaction}. This is going to be problematic on fetching data, but carry on. But please report this to the developer."
                )

        # - Insert the block, if the condition where the `main_block_id` is the same from the payload's block id.
        if block_equal_from_main:
            await blockchain_instance.append_block(
                context=context_from_archival_miner.block, follow_up=False
            )
            logger.info(
                f"Block #{context_from_archival_miner.block.id} is qualified to be processed immediately by appending it in the blockchain."
            )

        # - Insert an internal transaction.
        # @o This was seperated from the consolidated internal transaction handler due to the need of handling extra variables as `ARCHIVAL_MINER_NODE` sent a payload.
        await blockchain_instance.insert_internal_transaction(
            action=TransactionActions.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING,
            data=NodeTransaction(
                action=NodeTransactionInternalActions.CONSENSUS,
                context=NodeConfirmMineConsensusTransaction(
                    miner_address=context_from_archival_miner.miner_address,
                    master_address=blockchain_instance.node_identity[0],
                    consensus_negotiation_id=context_from_archival_miner.consensus_negotiation_id,
                ),
            ),
        )

        # - Insert transaction from the blockchain for the successful thing.
        return ConsensusSuccessPayload(
            addon_consensus_sleep_seconds=proposed_consensus_addon_timer,
            reiterate_master_address=blockchain_instance.node_identity[0],
        )

    raise HTTPException(
        detail="Blockchain instance is not yet initialized. Please try again later.",
        status_code=HTTPStatus.SERVICE_UNAVAILABLE,
    )


@node_router.post(
    "/receive_raw_block",
    tags=[NodeAPI.NODE_TO_NODE_API.value, NodeAPI.ARCHIVAL_MINER_NODE_API.value],
    summary=f"Receives a raw block for the {NodeType.ARCHIVAL_MINER_NODE} to hash.",
    description=f"A special API endpoint that receives a raw bock to be mined.",
    dependencies=[
        Depends(
            # - In archival instance, we cannot determine the role of the master node since it wasn't registered.
            # - With that, we can use the certification token instead.
            EnsureAuthorized(blockchain_related=True)
        )
    ],
)
async def receive_raw_block(
    context_from_master: ConsensusFromMasterPayload,
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance),
    database_instance: Database = Depends(get_database_instance),
) -> Response:

    if isinstance(blockchain_instance, BlockchainMechanism):
        # - Validate any previous consensus negotiation and delete it as possible.
        await validate_previous_consensus_negotiation(
            database_instance_ref=database_instance,
            block_reference=context_from_master.block,
        )

        # - Record the Consensus Negotiation ID.
        save_generated_consensus_negotiation_id_query: Insert = (
            consensus_negotiation.insert().values(
                block_no_ref=context_from_master.block.id,
                consensus_negotiation_id=context_from_master.consensus_negotiation_id,
                peer_address=context_from_master.master_address,
                status=ConsensusNegotiationStatus.ON_PROGRESS,
            )
        )
        await database_instance.execute(save_generated_consensus_negotiation_id_query)
        logger.info(
            f"Consensus Negotiation initiated by Master Node {context_from_master.master_address}!"
        )

        # - Enqueue the block from the local instance of blockchain.
        create_task(
            blockchain_instance.hash_and_store_given_block(
                block=context_from_master.block,
                from_origin=SourceNodeOrigin.FROM_MASTER,
                master_address_ref=context_from_master.master_address,
            ),
            name=f"hash_given_block_from_master_{context_from_master.master_address[-6:]}",
        )

        return Response(status_code=HTTPStatus.ACCEPTED)

    return Response(status_code=HTTPStatus.SERVICE_UNAVAILABLE)


@node_router.post(
    "/receive_context",
    tags=[NodeAPI.NODE_TO_NODE_API.value, NodeAPI.MASTER_NODE_API.value],
    summary="Receives data that serves as an action of the user from the dashboard.",
    description=f"A special API endpoint that accepts payload from the dashboard. This requires special credentials and handling outside the scope of node.",
    status_code=HTTPStatus.ACCEPTED,
)
async def receive_action_from_dashboard(
    payload: ApplicantUserTransaction | AdditionalContextTransaction,
    auth_instance=Depends(
        EnsureAuthorized(
            _as=[
                UserEntity.APPLICANT_DASHBOARD_USER,
                UserEntity.ORGANIZATION_DASHBOARD_USER,
            ],
            return_token=True,
        )
    ),
    blockchain_instance: BlockchainMechanism = Depends(get_blockchain_instance),
    database_instance: Database = Depends(get_database_instance),
) -> JSONResponse | None:

    # - Since the payload is automatically determined, we are going to resolve its parameter for the `from_address` and `to_address` when calling `blockchain_instance.insert_external_transaction`.

    # @o Type-hints for now.
    resolved_content_type: TransactionContextMappingType | None = None
    resolved_from_address: AddressUUID | None = None
    resolved_to_address: AddressUUID | None = None
    resolved_action: TransactionActions | None = None

    # - Compare via instance and assign necessary components.
    # - As well compare the token payload from the

    #! Note that, `ApplicantLogTransaction` has been handled from `receive_file_from_dashboard` method.

    if isinstance(payload, ApplicantUserTransaction):
        resolved_action = TransactionActions.INSTITUTION_ORG_GENERATE_APPLICANT
        resolved_content_type = TransactionContextMappingType.APPLICANT_BASE

        resolved_to_address = (
            None  # - This will get resolved later since it was generative model.
        )

    elif isinstance(payload, AdditionalContextTransaction):
        # - With the logic being too complicated, we should resolve this `content_type` here instead.
        # - Inside method (the handler from this context) does nothing honestly.

        # * We have no choice but to have the credential re-checked again from the entrypoint of the `insert_external_transactions`.
        identify_user_type_query: Select = select([users.c.type]).where(
            users.c.unique_address == payload.address_origin
        )

        identify_user_type = await database_instance.fetch_val(identify_user_type_query)

        if identify_user_type is None:  # type: ignore
            raise HTTPException(
                detail="Cannot classify user's additional context `type`. Address origin may be invalid.",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        if identify_user_type is UserEntity.APPLICANT_DASHBOARD_USER:  # type: ignore
            resolved_action = (
                TransactionActions.INSTITUTION_ORG_APPLICANT_REFER_EXTRA_INFO
            )
            resolved_content_type = TransactionContextMappingType.APPLICANT_ADDITIONAL

        elif identify_user_type is UserEntity.ORGANIZATION_DASHBOARD_USER:  # type: ignore
            resolved_action = TransactionActions.ORGANIZATION_REFER_EXTRA_INFO
            resolved_content_type = (
                TransactionContextMappingType.ORGANIZATION_ADDITIONAL
            )

        else:
            raise HTTPException(
                detail="Cannot resolve user organization's `associate` type.",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        payload.timestamp = datetime.now()
        resolved_to_address = payload.address_origin

    else:
        raise HTTPException(
            detail="Payload is unidentified or is unhandled from this API entrypoint.",
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        )

    # - Resolve the `from_address` but skip validation for the `to_address` due to the generative models being unable to provide uuids on non-existent properity.
    resolved_from_address = await validate_source_and_origin_associates(
        database_instance_ref=database_instance,
        source_session_token=auth_instance,
        target_address=resolved_to_address,
        skip_validation_on_target=isinstance(payload, ApplicantUserTransaction),
        return_resolved_source_address=True,  # type: ignore # * `resolved_from_address` is already resolved on the top, where it validates the payload's instance.
    )

    # - Create a `GroupTransaction`.
    resolved_payload: GroupTransaction = GroupTransaction(
        content_type=resolved_content_type, context=payload
    )

    if resolved_from_address is None:
        raise HTTPException(
            detail="Cannot find user reference when the provided `content-type` or the parameter `from_address` is invalid.",
            status_code=HTTPStatus.NOT_ACCEPTABLE,
        )

    # - When validation for both the source and address is success, finally invoke the `from_address`.
    payload.inserter = resolved_from_address

    extern_insertion_result = await blockchain_instance.insert_external_transaction(
        action=resolved_action,
        from_address=resolved_from_address,
        to_address=resolved_to_address,
        data=resolved_payload,
    )

    if isinstance(extern_insertion_result, HTTPException):
        raise extern_insertion_result

    else:
        return JSONResponse(
            content={
                "detail": f"An action `{resolved_action.name}` with a content-type of `{resolved_content_type.name}`, given by {resolved_from_address} to {resolved_to_address if resolved_to_address is not None else '<unknown, determined via process>'} has been processed successfully."  # type: ignore # ! Enum gets disregarded when variable is assigned to `NoneType`.
            },
            status_code=HTTPStatus.OK,
        )


@node_router.post(
    "/receive_context_log",
    tags=[NodeAPI.NODE_TO_NODE_API.value, NodeAPI.MASTER_NODE_API.value],
    summary="Receives a multiform content type specific to `ApplicationLogContentType`.",
    description=f"A special API endpoint that is exclusive to a pyadantic model `ApplicantLogTransaction`, which accepts payload from the dashboard along with the file. Even without file, `ApplicantLogTransaction` is destined from this endpoint.",
)
async def receive_file_from_dashboard(
    address_origin: AddressUUID = Form(...),
    content_type: ApplicantLogContentType = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    role: str = Form(...),
    file: UploadFile | None = File(None),
    duration_start: datetime = Form(...),
    duration_end: datetime | None = Form(None),
    auth_instance: JWTToken = Depends(
        EnsureAuthorized(
            _as=[
                UserEntity.APPLICANT_DASHBOARD_USER,
                UserEntity.ORGANIZATION_DASHBOARD_USER,
            ],
            return_token=True,
        )
    ),
    blockchain_instance: BlockchainMechanism = Depends(get_blockchain_instance),
    database_instance: Database = Depends(get_database_instance),
) -> JSONResponse:

    try:
        # ! Logic Conditon Checking
        if isinstance(duration_end, datetime) and duration_start > duration_end:
            raise HTTPException(
                detail="The specified time for the duration start is higher than the end of duration. This is not possible.",
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        resolved_source_address: AddressUUID | None = (
            await validate_source_and_origin_associates(
                database_instance_ref=database_instance,
                source_session_token=auth_instance,
                target_address=address_origin,
                skip_validation_on_target=False,
                return_resolved_source_address=True,
            )
        )

        # - After receiving, wrap the payload.
        wrapped_to_model: ApplicantLogTransaction = ApplicantLogTransaction(
            **{
                "address_origin": address_origin,
                "type": content_type,
                "name": name,
                "description": description,
                "role": role,
                "file": file,
                "duration_start": duration_start,
                "duration_end": duration_end,
                "validated_by": resolved_source_address,  # type: ignore
                "timestamp": datetime.now(),
            }
        )

        # - Then create a GroupTransaction.
        transaction: GroupTransaction = GroupTransaction(
            content_type=TransactionContextMappingType.APPLICANT_LOG,
            context=wrapped_to_model,
        )

        insertion_result: HTTPException | None = (
            await blockchain_instance.insert_external_transaction(
                action=TransactionActions.INSTITUTION_ORG_REFER_NEW_DOCUMENT,
                from_address=AddressUUID(resolved_source_address),  # type: ignore
                to_address=AddressUUID(address_origin),
                data=transaction,
            )
        )

        if isinstance(insertion_result, HTTPException):
            raise insertion_result

        return JSONResponse(
            content={
                "detail": f"An applicant log content given by <address hidden> to {address_origin} has been processed successfully."  # type: ignore # ! Enum gets disregarded when variable is assigned to `NoneType`.
            },
            status_code=HTTPStatus.OK,
        )

    except PydanticValueError as e:
        raise HTTPException(
            detail=f"Cannot wrapped the payload to a respective model ({ApplicantLogTransaction}). | Info: {e}",
            status_code=HTTPStatus.BAD_REQUEST,
        )


"""
# Node-to-Node Establish Connection Endpoints

@o Before doing anything, an `ARCHIVAL_MINER_NODE` has to establish connection to the `MASTER_NODE`.
@o With that, the `ARCHIVAL_MINER_NODE` has to give something a proof, that shows their proof of registration and login.
@o The following are required: `JWT Token`, `Source Address`, and `Auth Code` (as Auth Acceptance Code)

- When the `MASTER_NODE` identified those tokens to be valid, it will create a special token for the association.
- To-reiterate, the following are the structure of the token that is composed of the attributes between the communicator `ARCHIVAL_MINER_NODE` and the `MASTER_NODE`.
- Which will be the result of the entity named as `AssociationCertificate`.

@o From the `ARCHIVAL_MINER_NODE`: (See above).
@o From the `MASTER_NODE`: `ARCHIVAL_MINER_NODE`'s keys + AUTH_KEY (1st-Half, 32 characters) + SECRET_KEY(2nd-half, 32 character offset, 64 characters)

# Result: AssociationCertificate for the `ARCHIVAL_MINER_NODE` in AES form, whereas, the key is based from the ARCHIVAL-MINER_NODE's keys + SECRET_KEY + AUTH_KEY + DATETIME (in ISO format).

! Note that the result from the `MASTER_NODE` is saved, thurs, using `datetime` for the final key is possible.

- When this was created, `ARCHIVAL_MINER_NODE` will save this under the database and will be used further with no expiration.
"""


@node_router.post(
    "/certify_miner",
    tags=[NodeAPI.NODE_TO_NODE_API.value, NodeAPI.MASTER_NODE_API],
    summary=f"Receives echo from the {NodeType.ARCHIVAL_MINER_NODE} for establishment of their connection to the blockchain.",
    description=f"An API endpoint that is only accessile to {UserEntity.MASTER_NODE_USER.name}, where it accepts ECHO request to fetch a certificate before they ({UserEntity.ARCHIVAL_MINER_NODE_USER}) start doing blockchain operations. This will return a certificate as an acknowledgement response from the requestor.",
    dependencies=[
        Depends(EnsureAuthorized(_as=UserEntity.ARCHIVAL_MINER_NODE_USER)),
    ],  # - This is blockchain-related but not internally related, it was under consensus category. Therefore seperate the contents of the method below from the handler of the <class 'EnsureAuthorized'>.
)
async def certify_miner(
    origin: SourcePayload,
    x_source: AddressUUID = Header(..., description="The address of the requestor."),
    x_session: JWTToken = Header(
        ..., description="The current session token that the requestor uses."
    ),
    x_acceptance: AuthAcceptanceCode = Header(
        ...,
        description="The auth code that is known as acceptance code, used for extra validation.",
    ),
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance),
    database_instance: Database = Depends(get_database_instance),
) -> Response:

    # - [1] Validate such entries from the header.
    # - [1.1] Get the source first.
    fetch_node_source_query = select([users.c.unique_address, users.c.email]).where(
        users.c.unique_address == x_source
    )
    validated_source_address = await database_instance.fetch_one(
        fetch_node_source_query
    )

    # - [1.2] Then validate the token by incorporating previous query and the header `x_acceptance`.
    # * Validate other credentials and beyond at this point.
    if validated_source_address is not None:
        fetch_node_auth_query = select([func.count()]).where(
            (auth_codes.c.code == x_acceptance)
            & (
                auth_codes.c.to_email == validated_source_address.email  # type: ignore
            )  # @o Equivalent to validated_source_address.email.
        )

        validated_auth_code = await database_instance.fetch_one(fetch_node_auth_query)

        if validated_auth_code.count:  # type: ignore
            fetch_node_token_query = select([func.count()]).where(
                (tokens.c.token == x_session)
                & (tokens.c.from_user == validated_source_address.unique_address)  # type: ignore
            )

            validated_node_token = await database_instance.fetch_one(
                fetch_node_token_query
            )

            if validated_node_token.count:  # type: ignore
                authority_code: str | None = env.get("AUTH_KEY", None)
                authority_signed: str | None = env.get("SECRET_KEY", None)

                # - Create the token here.
                if authority_signed is not None and authority_code is not None:
                    # - To complete, get one base token and randomize its location and splice it by 25% to encorporate with other tokens.
                    # * This was intended and not a joke.
                    encrypter = Fernet(authority_code.encode("utf-8"))

                    authored_token: bytes = (
                        authority_signed[:16]
                        + x_session
                        + authority_signed[32:48]
                        + x_source
                        + authority_signed[48:]
                        + x_acceptance
                        + authority_signed[16:32]
                        + datetime.now().isoformat()  # Add variance.
                    ).encode("utf-8")

                    encrypted_authored_token: bytes = encrypter.encrypt(authored_token)

                    # @o As a `MASTER` node, store it for validation later.
                    store_authored_token_query: Insert = associated_nodes.insert().values(
                        user_address=validated_source_address.unique_address,  # type: ignore
                        certificate=encrypted_authored_token.decode("utf-8"),
                        # # We need to ensure that the source address and port is right when this was deployed in external.
                        # source_address=request.client.host,
                        # source_port=request.client.port,
                        source_address=origin.source_address,
                        source_port=origin.source_port,
                    )
                    await database_instance.execute(store_authored_token_query)

                    if isinstance(blockchain_instance, BlockchainMechanism):
                        await blockchain_instance.insert_internal_transaction(
                            action=TransactionActions.NODE_GENERAL_CONSENSUS_INIT,
                            data=NodeTransaction(
                                action=NodeTransactionInternalActions.INIT,
                                context=NodeCertificateTransaction(
                                    requestor_address=AddressUUID(x_source),
                                    timestamp=datetime.now(),
                                ),
                            ),
                        )

                        proposed_consensus_sleep_time: float = (
                            generate_consensus_sleep_time(
                                block_timer=blockchain_instance.block_timer_seconds
                            )
                        )

                        # - Fool-proof by recording this consensus sleep time in the database.
                        update_association_initial_query: Update = (
                            associated_nodes.update()
                            .where(
                                associated_nodes.c.user_address
                                == validated_source_address.unique_address  # type: ignore
                            )
                            .values(
                                status=AssociatedNodeStatus.CURRENTLY_AVAILABLE,
                                consensus_sleep_expiration=datetime.now()
                                + timedelta(seconds=proposed_consensus_sleep_time),
                            )
                        )

                        await database_instance.execute(
                            update_association_initial_query
                        )

                        # # Then return it.
                        return JSONResponse(
                            content={
                                "initial_consensus_sleep_seconds": proposed_consensus_sleep_time,
                                "certificate_token": encrypted_authored_token.decode(
                                    "utf-8"
                                ),
                            },
                            status_code=HTTPStatus.OK,
                        )

                raise HTTPException(
                    detail="Authority to sign the certificate is not possible due to missing parameters or the blockchain instance is currently uninitialized.",
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                )

    raise HTTPException(
        detail="One or more headers are invalid to initiate certification.",
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
    )


@node_router.post(
    "/pull_chain_upstream",
    tags=[NodeAPI.NODE_TO_NODE_API.value, NodeAPI.MASTER_NODE_API.value],
    summary=f"Requests the blockchain file as-is from the '{NodeType.MASTER_NODE.name}'.",
    description=f"A special API endpoint that allows '{NodeType.ARCHIVAL_MINER_NODE.name}' to fetch the latest version of the blockchain file from the '{NodeType.MASTER_NODE.name}'. This is mandatory before allowing the node to hash or participate from the blockchain.",
    dependencies=[
        Depends(
            EnsureAuthorized(
                _as=UserEntity.ARCHIVAL_MINER_NODE_USER, blockchain_related=True
            )
        )
    ],
)
async def pull_chain_upstream(
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance),
) -> JSONResponse:

    if isinstance(blockchain_instance, BlockchainMechanism):
        await blockchain_instance.insert_internal_transaction(
            action=TransactionActions.NODE_GENERAL_CONSENSUS_BLOCK_SYNC,
            data=NodeTransaction(
                action=NodeTransactionInternalActions.SYNC,
                context=NodeSyncTransaction(
                    requestor_address=AddressUUID(blockchain_instance.node_identity[0]),
                    timestamp=datetime.now(),
                ),
            ),
        )

        return JSONResponse(
            content={
                "current_hash": await blockchain_instance.get_chain_hash(),
                "content": await blockchain_instance.get_chain(),
            },
            status_code=HTTPStatus.OK,
        )

    raise HTTPException(
        detail="Cannot request for upstream when the blockchain instance has not bee initialized or is not yet ready.",
        status_code=HTTPStatus.NOT_ACCEPTABLE,
    )


@node_router.post(
    "/verify_chain_hash",
    tags=[NodeAPI.NODE_TO_NODE_API.value, NodeAPI.MASTER_NODE_API.value],
    summary="Verifies the input as a hash towards to the latest blockchain.",
    description=f"A special API endpoint that accepts hash in return to validate them against the `{NodeType.MASTER_NODE}`'s blockchain file.",
    dependencies=[
        Depends(
            EnsureAuthorized(
                _as=UserEntity.ARCHIVAL_MINER_NODE_USER, blockchain_related=True
            )
        )
    ],
)
async def verify_chain_hash(
    x_hash: str = Header(
        ...,
        description=f"The input hash that is going to be compared against the {NodeType.MASTER_NODE.name}.",
    ),
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance),
) -> Response:

    is_hash_equal: bool = False

    if isinstance(blockchain_instance, BlockchainMechanism):
        is_hash_equal = await blockchain_instance.get_chain_hash() == x_hash

    return Response(
        status_code=HTTPStatus.OK if is_hash_equal else HTTPStatus.NOT_ACCEPTABLE
    )
