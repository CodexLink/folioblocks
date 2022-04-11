"""
Consensus Mechanism (consensus.py) | A subclass component from the `BlockchainMechanism`.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from asyncio import create_task, sleep, wait
from logging import Logger, getLogger
from os import environ as env
from typing import Any, Callable

from blueprint.models import associated_nodes
from databases import Database
from core.dependencies import get_args_value
from utils.http import get_http_client_instance
from utils.processors import load_env

from core.constants import (
    ASYNC_TARGET_LOOP,
    AUTH_ENV_FILE_NAME,
    REF_MASTER_BLOCKCHAIN_ADDRESS,
    REF_MASTER_BLOCKCHAIN_PORT,
    AddressUUID,
    HTTPQueueMethods,
    IdentityTokens,
    JWTToken,
    NodeType,
    RequestPayloadContext,
    URLAddress,
)
from core.dependencies import (
    get_database_instance,
    get_identity_tokens,
    get_master_node_properties,
)

logger: Logger = getLogger(ASYNC_TARGET_LOOP)


class ConsensusMechanism:
    def __init__(self, *, role: NodeType) -> None:
        self.role = role
        self.http_instance = get_http_client_instance()
        self.master_target = get_master_node_properties

    def __restrict_call(*, on: NodeType) -> Callable:  # type: ignore
        """Restricts the method to be called depending on their `self.role`.
        Since most of the methods is designed respectively based on their role.
        Ever process requires this certain role to only call this method and nothing else.

        Args:
                on (NodeType): The `role` of the node.

        Returns:
                Callable: Calls the decorator method.
        """

        def deco(fn: Callable) -> Callable:
            def instance(
                self: Any, *args: list[Any], **kwargs: dict[Any, Any]
            ) -> Callable | None:
                if self.role == on:
                    return fn(self, *args, **kwargs)

                self.warning(
                    f"Your role {self.role} cannot call this method `{fn.__name__}` due to the role is restricted to {on}."
                )
                return None

            return instance

        return deco

    @__restrict_call(on=NodeType.ARCHIVAL_MINER_NODE)
    async def establish(self) -> None:
        """Make `ARCHIVAL_MINER_NODE` to call master's `acknowledge` endpoint providing certains credentials as a proof of registration."""
        master_origin_address, master_origin_port = self.master_target(
            key=REF_MASTER_BLOCKCHAIN_ADDRESS
        ), self.master_target(key=REF_MASTER_BLOCKCHAIN_PORT)

        node_instance_args = get_args_value()
        node_address, node_port = (
            node_instance_args.node_host,
            node_instance_args.node_port,
        )

        stored_session_token: IdentityTokens | None = get_identity_tokens()
        db: Database = get_database_instance()

        if stored_session_token is None:
            logger.error(
                "There are no stored session token (`AddressUUID` and `JWTToken`) for this process to begin. This may be an error logic issue. Please report to the developers as possible."
            )
            return None

        auth_source: AddressUUID = stored_session_token[0]
        auth_session: JWTToken = stored_session_token[1]  # * Get the JWT token.

        while True:
            auth_acceptance: str | None = env.get("AUTH_ACCEPTANCE_CODE", None)

            if auth_acceptance is None:
                load_env()

                logger.error(
                    f"Auth Acceptance Code does not exists, yet you were able to login, have you modified `{AUTH_ENV_FILE_NAME}`? Retrying in 5 seconds."
                )
                await sleep(5)
                continue
            break

        master_response = await self.http_instance.enqueue_request(
            url=URLAddress(
                f"http://{master_origin_address}:{master_origin_port}/node/establish/receive_echo"
            ),
            headers={
                "x-source": auth_source,
                "x-session": auth_session,
                "x-token": auth_session,
                "x-acceptance": auth_acceptance,
            },
            data={"source_address": node_address, "source_port": node_port},
            method=HTTPQueueMethods.POST,
            await_result_immediate=True,
            name="get_echo_from_master",
        )

        # - Add the credentials to the associated nodes as self.
        if master_response.ok:
            association_certificate: RequestPayloadContext = (
                await master_response.json()
            )

            insert_fetched_certificate_stmt = associated_nodes.insert().values(
                user_address=auth_source,
                certificate=association_certificate["certificate_token"],
                # * The following fields are not needed throughout the runtime, but is required due to constraint.
                # ! Not that these variables does not represent the current node but rather the target node.
                source_address=master_origin_address,
                source_port=master_origin_port,
            )

            await db.execute(insert_fetched_certificate_stmt)

            logger.info("Generation of Association certificate token were successful!")

        else:
            logger.error(
                f"Generation of association certificate is not successful due to rejection or no reply from the {NodeType.MASTER_NODE}"
            )

        return None

    @__restrict_call(on=NodeType.MASTER_NODE)
    async def negotiate(self) -> None:
        return


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
# TODO: Actions should be, receive_block, (During this, one of the assert processes will be executed.)
"""

"""
# Node-to-Node Consensus Blockchain Operation Endpoints

@o Whenever the blockchain's `MASTER_NODE` is looking for `ARCHIVAL_MINER_NODE`s. It has to ping them in a way that it shows their availability.
@o However, since we already did some established connection between them, we need to pass them off from the `ARCHIVAL_MINER_NODE`s themselves to the
@o `MASTER_NODE`. This was to ensure that the node under communication is not a fake node by providing the `AssociationCertificate`.

! These endpoints are being used both.
"""


# @node_router.post(
# 	"/consensus/acknowledge",
# 	tags=[NodeAPI.NODE_TO_NODE_API.value],
# 	summary="",
# 	description="",
# 	dependencies=[
# 		Depends(
# 			EnsureAuthorized(
# 				_as=[UserEntity.ARCHIVAL_MINER_NODE_USER, UserEntity.MASTER_NODE_USER]
# 			)
# 		)
# 	],
# )
# async def consensus_acknowledge() -> None:
# 	return


# @node_router.post(
# 	"/consensus/echo",
# 	tags=[NodeAPI.NODE_TO_NODE_API.value],
# 	summary="",
# 	description="",
# 	dependencies=[
# 		Depends(
# 			EnsureAuthorized(
# 				_as=[UserEntity.ARCHIVAL_MINER_NODE_USER, UserEntity.MASTER_NODE_USER]
# 			)
# 		)
# 	],
# )
# async def consensus_echo() -> None:
# 	return


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

# Result: AssociationCertificate for the `ARCHIVAL_MINER_NODE` in AES form, whereas, the key is based from the ARCHIVAL-MINER_NODE's keys + SECRET_KEY + AUTH_KEY + DATETIME (in ISO format).

! Note that the result from the `MASTER_NODE` is saved, thurs, using `datetime` for the final key is possible.

- When this was created, `ARCHIVAL_MINER_NODE` will save this under the database and will be used further with no expiration.
"""


# @node_router.post(
# 	"/establish/acknowledge",
# 	tags=[NodeAPI.NODE_TO_NODE_API.value],
# 	summary="",
# 	description="",
# 	dependencies=[Depends(EnsureAuthorized(_as=UserEntity.MASTER_NODE_USER))],
# )
# async def establish_acknowledge() -> None:
# 	return


# @node_router.post(
# 	"/establish/echo",
# 	tags=[NodeAPI.NODE_TO_NODE_API.value],
# 	summary="",
# 	description="",
# 	dependencies=[Depends(EnsureAuthorized(_as=UserEntity.ARCHIVAL_MINER_NODE_USER))],
# )
# async def establish_echo() -> None:
# 	"""
# 	An endpoint that the ARCHIVAL_MINER_NODE_USER will use to provide information to the master node.
# 	"""


# 	echo_to_master_data = await get_http_client_instance().enqueue_request(

# 		method=HTTPQueueMethods.POST,
# 		data={
# 			"session_token": "",
# 			"auth_acceptance": "",
# 		}
# 		await_result_immediate=True
# 	)
# 	return


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
