"""
API — Explorer and Node API for the Master Node.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""


from datetime import datetime
from http import HTTPStatus
from logging import Logger, getLogger
from os import environ as env
from typing import Any

from blueprint.models import (
    associated_nodes,
    auth_codes,
    consensus_negotiation,
    tokens,
    users,
)
from blueprint.schemas import (
    ConsensusFromMasterPayload,
    ConsensusSuccessPayload,
    ConsensusToMasterPayload,
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
    AddressUUID,
    AuthAcceptanceCode,
    BaseAPI,
    ConsensusNegotiationStatus,
    JWTToken,
    NodeAPI,
    NodeTransactionInternalActions,
    NodeType,
    SourceNodeOrigin,
    TransactionActions,
    UserEntity,
    random_generator,
)
from core.dependencies import (
    EnsureAuthorized,
    get_database_instance,
    get_identity_tokens,
)
from cryptography.fernet import Fernet
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.sql.expression import Insert, Update

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
    node_state: NodeConsensusInformation = (
        get_blockchain_instance().get_blockchain_private_state()
    )
    node_statistics: NodeMasterInformation | None = (
        get_blockchain_instance().get_blockchain_public_state()
    )

    return NodeInformation(
        properties=node_state,
        statistics=node_statistics,
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
    "/blockchain/receive_hashed_block",
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
async def process_hashed_block(
    context_from_archival_miner: ConsensusToMasterPayload,
) -> ConsensusSuccessPayload:

    # # Ensure that the block we receive is pydantic-compatible, which is going to be inserted from the container.

    blockchain_current_instance: BlockchainMechanism = get_blockchain_instance()

    # - Update the Consensus Negotiation ID.
    update_consensus_negotiation_query: Update = (
        consensus_negotiation.update()
        .where(
            (
                consensus_negotiation.c.consensus_negotiation_id
                == context_from_archival_miner.consensus_negotiation_id
            )
            & (consensus_negotiation.c.status == ConsensusNegotiationStatus.ON_PROGRESS)
        )
        .values(status=ConsensusNegotiationStatus.COMPLETED)
    )

    await get_database_instance().execute(update_consensus_negotiation_query)

    # - Insert the block.
    await get_blockchain_instance().insert_mined_block(
        block=context_from_archival_miner.block,
        from_origin=SourceNodeOrigin.FROM_ARCHIVAL_MINER,
    )

    # - Insert an internal transaction.
    # @o This was seperated from the consolidated internal transaction handler due to the need of handling extra variables as `ARCHIVAL_MINER_NODE` sent a payload.
    await blockchain_current_instance._insert_internal_transaction(
        action=TransactionActions.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING,
        data=NodeTransaction(
            action=NodeTransactionInternalActions.CONSENSUS,
            context=NodeConfirmMineConsensusTransaction(
                miner_address=context_from_archival_miner.miner_address,
                master_address=blockchain_current_instance.identity[0],
                consensus_negotiation_id=context_from_archival_miner.consensus_negotiation_id,
            ),
        ),
    )

    # - Insert transaction from the blockchain for the successful thing.
    return ConsensusSuccessPayload(
        addon_consensus_sleep_seconds=random_generator.uniform(0, 2)
        * blockchain_current_instance.block_timer_seconds,
        reiterate_master_address=blockchain_current_instance.identity[0],
    )


@node_router.post(
    "/blockchain/receive_raw_block",
    tags=[NodeAPI.NODE_TO_NODE_API.value, NodeAPI.ARCHIVAL_MINER_NODE_API.value],
    summary=f"Receives a raw block for the {NodeType.ARCHIVAL_MINER_NODE} to mine.",
    description=f"A special API endpoint that receives a raw bock to be mined.",
    dependencies=[
        Depends(
            EnsureAuthorized(_as=UserEntity.MASTER_NODE_USER, blockchain_related=True)
        )
    ],
)
async def receive_block_to_mine(
    context_from_master: ConsensusFromMasterPayload,
) -> Response:

    # - Record the Consensus Negotiation ID.
    save_generated_consensus_negotiation_id_query: Insert = (
        consensus_negotiation.insert().values(
            block_no_ref=context_from_master.block.id,
            consensus_negotiation_id=context_from_master.consensus_negotiation_id,
            peer_address=context_from_master.master_address,
            status=ConsensusNegotiationStatus.ON_PROGRESS,
        )
    )
    await get_database_instance().execute(save_generated_consensus_negotiation_id_query)
    logger.info(
        f"Consensus Negotiation initiated by Master Node {context_from_master.master_address}!"
    )

    # - Enqueue the block from the local instance of blockchain.
    await get_blockchain_instance().insert_mined_block(
        block=context_from_master.block,
        from_origin=SourceNodeOrigin.FROM_ARCHIVAL_MINER,
    )

    return Response(status_code=HTTPStatus.ACCEPTED)


@node_router.post(
    "/blockchain/receive_context",
    tags=[NodeAPI.NODE_TO_NODE_API.value, NodeAPI.MASTER_NODE_API.value],
    summary="Receives data that serves as an action of the user from the dashboard.",
    description=f"A special API endpoint that accepts payload from the dashboard. This requires special credentials and handling outside the scope of node.",
    dependencies=[
        Depends(
            EnsureAuthorized(_as=UserEntity.DASHBOARD_USER, blockchain_related=True)
        )
    ],
)
async def recieve_action_from_dashboard() -> None:
    # - Identify the type of the transaction.
    # - If there's a file, process it under, files.
    # - Encrypt it via AES from the generated file. (Code should be derived from the existing Fernet() or should we create another one? [such as, AUTH (mid 16 characters) of master + sender ]) and make the filename as UUID with datetime with no extensions.

    # - Field of the file should be changed to a SHA256 with UUID as a base location from where it was located.
    #
    return


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
    "/establish/receive_echo",
    tags=[NodeAPI.NODE_TO_NODE_API.value, NodeAPI.MASTER_NODE_API],
    summary=f"Receives echo from the {NodeType.ARCHIVAL_MINER_NODE} for establishment of their connection to the blockchain.",
    description=f"An API endpoint that is only accessile to {UserEntity.MASTER_NODE_USER.name}, where it accepts ECHO request to fetch a certificate before they ({UserEntity.ARCHIVAL_MINER_NODE_USER}) start doing blockchain operations. This will return a certificate as an acknowledgement response from the requestor.",
    dependencies=[
        Depends(EnsureAuthorized(_as=[UserEntity.ARCHIVAL_MINER_NODE_USER])),
    ],  # - This is blockchain-related but not internally related, it was under consensus category. Therefore seperate the contents of the method below from the handler of the <class 'EnsureAuthorized'>.
)
async def acknowledge_as_response(
    origin: SourcePayload,
    x_source: AddressUUID = Header(..., description="The address of the requestor."),
    x_session: JWTToken = Header(
        ..., description="The current session token that the requestor uses."
    ),
    x_acceptance: AuthAcceptanceCode = Header(
        ...,
        description="The auth code that is known as acceptance code, used for extra validation.",
    ),
) -> Response:
    db: Any = get_database_instance()  # * Initialized on scope.

    # - [1] Validate such entries from the header.
    # - [1.1] Get the source first.
    fetch_node_source_query = select([users.c.unique_address, users.c.email]).where(
        users.c.unique_address == x_source
    )
    validated_source_address = await db.fetch_one(fetch_node_source_query)

    # - [1.2] Then validate the token by incorporating previous query and the header `x_acceptance`.
    # * Validate other credentials and beyond at this point.
    if validated_source_address is not None:
        fetch_node_auth_query = select([auth_codes.c.id]).where(
            (auth_codes.c.code == x_acceptance)
            & (
                auth_codes.c.to_email == validated_source_address.email
            )  # @o Equivalent to validated_source_address.email.
        )

        validated_auth_code = await db.fetch_one(fetch_node_auth_query)

        if validated_auth_code is not None:
            fetch_node_token_query = select([tokens.c.id]).where(
                (tokens.c.token == x_session)
                & (tokens.c.from_user == validated_source_address.unique_address)
            )

            validated_node_token = await db.fetch_one(fetch_node_token_query)

            if validated_node_token is not None:
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
                        user_address=validated_source_address.unique_address,
                        certificate=encrypted_authored_token.decode("utf-8"),
                        # # We need to ensure that the source address and port is right when this was deployed in external.
                        # source_address=request.client.host,
                        # source_port=request.client.port,
                        source_address=origin.source_address,
                        source_port=origin.source_port,
                    )
                    await db.execute(store_authored_token_query)

                    await get_blockchain_instance()._insert_internal_transaction(
                        action=TransactionActions.NODE_GENERAL_CONSENSUS_INIT,
                        data=NodeTransaction(
                            action=NodeTransactionInternalActions.INIT,
                            context=NodeCertificateTransaction(
                                requestor_address=AddressUUID(x_source),
                                timestamp=datetime.now(),
                            ),
                        ),
                    )

                    # # Then return it.
                    return JSONResponse(
                        content={"certificate_token": authored_token.decode("utf-8")},
                        status_code=HTTPStatus.OK,
                    )

                raise HTTPException(
                    detail="Authority to sign the certificate is not possible due to missing parameters.",
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                )

    raise HTTPException(
        detail="One or more headers are invalid.",
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
    )


@node_router.post(
    "/blockchain/request_update",
    tags=[NodeAPI.NODE_TO_NODE_API.value, NodeAPI.MASTER_NODE_API.value],
    summary=f"Requests the blockchain file as-is from the '{NodeType.MASTER_NODE.name}'.",
    description=f"A special API endpoint that allows '{NodeType.ARCHIVAL_MINER_NODE.name}' to fetch the latest version of the blockchain file from the '{NodeType.MASTER_NODE.name}'. This is mandatory before allowing the node to mine or participate from the blockchain.",
    dependencies=[
        Depends(
            EnsureAuthorized(_as=UserEntity.MASTER_NODE_USER, blockchain_related=True)
        )
    ],
)
async def request_blockchain_upstream() -> JSONResponse:
    blockchain_instance: BlockchainMechanism = get_blockchain_instance()

    await blockchain_instance._insert_internal_transaction(
        action=TransactionActions.NODE_GENERAL_CONSENSUS_BLOCK_SYNC,
        data=NodeTransaction(
            action=NodeTransactionInternalActions.SYNC,
            context=NodeSyncTransaction(
                requestor_address=AddressUUID(blockchain_instance.identity[0]),
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


@node_router.post(
    "/blockchain/verify_hash",
    tags=[NodeAPI.NODE_TO_NODE_API.value, NodeAPI.MASTER_NODE_API.value],
    summary="Verifies the input as a hash towards to the latest blockchain.",
    description=f"A special API endpoint that accepts hash in return to validate them against the `{NodeType.MASTER_NODE}`'s blockchain file.",
    dependencies=[
        Depends(
            EnsureAuthorized(_as=UserEntity.MASTER_NODE_USER, blockchain_related=True)
        )
    ],
)
async def verify_given_hash(
    x_hash: str = Header(
        ...,
        description=f"The input hash that is going to be compared against the {NodeType.MASTER_NODE.name}.",
    )
) -> Response:

    return Response(
        status_code=HTTPStatus.OK
        if await get_blockchain_instance().get_chain_hash() == x_hash
        else HTTPStatus.NOT_ACCEPTABLE
    )
