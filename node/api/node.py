"""
API — Explorer and Node API for the Master Node.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""


from typing import Any

from blueprint.schemas import NodeConsensusInformation
from core.blockchain import get_blockchain_instance
from core.constants import AddressUUID, BaseAPI, NodeAPI, UserEntity
from core.dependencies import (
    EnsureAuthorized,
    get_identity_tokens,
)
from fastapi import APIRouter, Depends

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
    response_model=NodeConsensusInformation,
    summary="Fetch information from the master node.",
    description="An API endpoint that returns information based on the authority of the client's requests. This requires special headers.",
    dependencies=[
        Depends(
            EnsureAuthorized(
                _as=[UserEntity.ARCHIVAL_MINER_NODE_USER, UserEntity.MASTER_NODE_USER]
            )
        ),
    ],
)
async def get_node_info() -> NodeConsensusInformation:
    blockchain_state: dict[
        str, Any
    ] = get_blockchain_instance().get_blockchain_private_state()

    return NodeConsensusInformation(
        owner=AddressUUID(
            get_identity_tokens()[0] if get_identity_tokens is not None else "0"
        ),
        is_sleeping=blockchain_state["sleeping"],
        is_mining=blockchain_state["mining"],
        node_role=blockchain_state["role"],
        consensus_timer=blockchain_state["consensus_timer"],
        last_mined_block=blockchain_state["last_mined_block"],
    )


"""
/consensus/echo | When received ensure its the master by fetching its info.
/consensus/acknowledge | When acknowledging, give something, then it will return something.

# Note that MASTER will have to do this command once! Miners who just finished will have to wait and keep on retrying.
/consensus/negotiate | This is gonna be complex, on MASTER, if there's current negotiation then create a new one (token). Then return a consensus as initial from the computation of the consensus_timer.
/consensus/negotiate | When there's already a negotiation, when called by MASTER, return the context of the consensus_timer and other properties that validates you of getting the block when you are selected.
/consensus/negotiate | When block was fetched then acknowledge it.
/consensus/negotiate | When the miner is done, call this one again but with a payload, and then keep on retrying, SHOULD BLOCK THIS ONE.
/consensus/negotiate | When it's done, call this again for you to sleep by sending the calculated consensus, if not right then the MASTER will send a correct timer.
/consensus/negotiate | Repeat.
"""


@node_router.post(
    "/consensus/negotiate",
    tags=[
        NodeAPI.NODE_TO_NODE_API.value,
    ],
    summary="Initiates and finishes negotiation for the consensus mechanism named as 'Proof-of-Elapsed-Time.'",
    description="A special API endpoint that is called multiple times for the consensus mechanism from initial to final negotiation.",
    dependencies=[
        Depends(
            EnsureAuthorized(
                _as=[UserEntity.ARCHIVAL_MINER_NODE_USER, UserEntity.MASTER_NODE_USER]
            )
        )
    ],
)
async def consensus_negotiate() -> None:  # TODO: Actions should be, receive_block, (During this, one of the assert processes will be executed.)
    return


"""
# Node-to-Node Consensus Blockchain Operation Endpoints

@o Whenever the blockchain's `MASTER_NODE` is looking for `ARCHIVAL_MINER_NODE`s. It has to ping them in a way that it shows their availability.
@o However, since we already did some established connection between them, we need to pass them off from the `ARCHIVAL_MINER_NODE`s themselves to the
@o `MASTER_NODE`. This was to ensure that the node under communication is not a fake node by providing the `AssociationCertificate`.

! These endpoints are being used both.
"""


@node_router.post(
    "/consensus/acknowledge",
    tags=[NodeAPI.NODE_TO_NODE_API.value],
    summary="",
    description="",
    dependencies=[
        Depends(
            EnsureAuthorized(
                _as=[UserEntity.ARCHIVAL_MINER_NODE_USER, UserEntity.MASTER_NODE_USER]
            )
        )
    ],
)
async def consensus_acknowledge() -> None:
    return


@node_router.post(
    "/consensus/echo",
    tags=[NodeAPI.NODE_TO_NODE_API.value],
    summary="",
    description="",
    dependencies=[
        Depends(
            EnsureAuthorized(
                _as=[UserEntity.ARCHIVAL_MINER_NODE_USER, UserEntity.MASTER_NODE_USER]
            )
        )
    ],
)
async def consensus_echo() -> None:
    return


"""
# Node-to-Node Establish Connection Endpoints

@o Before doing anything, an `ARCHIVAL_MINER_NODE` has to establish connection to the `MASTER_NODE`.
@o With that, the `ARCHIVAL_MINER_NODE` has to give something a proof, that shows their proof of registration and login.
@o The following are required: `JWT Token` and `Auth Code` (as Auth Acceptance Code)

- When the `MASTER_NODE` identified those tokens to be valid, it will create a special token for the association.
- To-reiterate, the following are the structure of the token that is composed of the attributes between the communicator `ARCHIVAL_MINER_NODE` and the `MASTER_NODE`.
- Which will be the result of the entity named as `AssociationCertificate`.

@o From the `ARCHIVAL_MINER_NODE`: (See above).
@o From the `MASTER_NODE`: `ARCHIVAL_MINER_NODE`'s keys + AUTH_KEY (1st-Half, 32 characters) + SECRET_KEY(2nd-half, 32 character offset, 64 characters)

# Result: AssociationCertificate for the `ARCHIVAL_MINER_NODE` in AES form, whereas, the key is based from the SECRET_KEY + AUTH_KEY + DATETIME (in ISO format).

! Note that the result from the `MASTER_NODE` is saved, thurs, using `datetime` for the final key is possible.

- When this was created, `ARCHIVAL_MINER_NODE` will save this under the database and will be used further with no expiration.
"""


@node_router.post(
    "/establish/acknowledge",
    tags=[NodeAPI.NODE_TO_NODE_API.value],
    summary="",
    description="",
    dependencies=[Depends(EnsureAuthorized(_as=UserEntity.MASTER_NODE_USER))],
)
async def establish_acknowledge() -> None:
    return


@node_router.post(
    "/establish/echo",
    tags=[NodeAPI.NODE_TO_NODE_API.value],
    summary="",
    description="",
    dependencies=[Depends(EnsureAuthorized(_as=UserEntity.ARCHIVAL_MINER_NODE_USER))],
)
async def establish_echo() -> None:
    return


"""
Blockchain operation
"""

# @node_router.post(
#     "/establish/echo",
#     tags=[NodeAPI.NODE_TO_NODE_API.value],
#     summary="",
#     description="",
#     dependencies=[Depends(EnsureAuthorized(_as=UserEntity.ARCHIVAL_MINER_NODE_USER))],
# )
# async def establish_echo() -> None:
#     return
