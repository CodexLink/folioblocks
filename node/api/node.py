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
        Depends(EnsureAuthorized(_as=[UserEntity.NODE_USER])),
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
    dependencies=[Depends(EnsureAuthorized(_as=UserEntity.NODE_USER))],
)
async def consensus_negotiate() -> None:  # TODO: Actions should be, receive_block, (During this, one of the assert processes will be executed.)
    return
