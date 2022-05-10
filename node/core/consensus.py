"""
Consensus Mechanism (consensus.py) | A subclass component from the `BlockchainMechanism`.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from asyncio import gather, sleep
from logging import Logger, getLogger
from os import environ as env

from aiohttp import ClientResponse
from blueprint.models import associated_nodes
from databases import Database
from utils.processors import save_database_state_to_volume_storage
from utils.http import HTTPClient
from sqlalchemy import select
from sqlalchemy.sql.expression import Insert, Select
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
from core.decorators import restrict_call
from core.dependencies import get_args_values, get_master_node_properties

logger: Logger = getLogger(ASYNC_TARGET_LOOP)


class ConsensusMechanism:
    def __init__(
        self,
        *,
        role: NodeType,
        ref_database_instance: Database,
        ref_http_instance: HTTPClient,
        ref_node_identity_instance: IdentityTokens,
    ) -> None:
        self.node_role: NodeType = role
        self.__master_target = get_master_node_properties

        self.__http_instance: HTTPClient = ref_http_instance
        self.__database_instance: Database = ref_database_instance
        self.__identity = ref_node_identity_instance

    @restrict_call(on=NodeType.ARCHIVAL_MINER_NODE)
    async def establish_node_certification(self) -> float | None:
        """Make `ARCHIVAL_MINER_NODE` to call master's `acknowledge` endpoint providing certains credentials as a proof of registration."""
        master_origin_address, master_origin_port = self.__master_target(
            key=REF_MASTER_BLOCKCHAIN_ADDRESS
        ), self.__master_target(key=REF_MASTER_BLOCKCHAIN_PORT)

        node_instance_args = get_args_values()
        node_address, node_port = (
            node_instance_args.node_host,
            node_instance_args.node_port,
        )

        auth_source: AddressUUID = self.__identity[0]
        auth_session: JWTToken = self.__identity[1]

        while True:
            load_env()
            auth_acceptance: str | None = env.get("AUTH_ACCEPTANCE_CODE", None)

            if auth_acceptance is None:
                logger.error(
                    f"Auth Acceptance Code does not exists, yet you were able to login, have you modified `{AUTH_ENV_FILE_NAME}`? Retrying in 5 seconds."
                )

                await sleep(5)
                continue
            break

        master_response: ClientResponse = await self.__http_instance.enqueue_request(
            url=URLAddress(
                f"{master_origin_address}:{master_origin_port}/node/certify_miner"
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
            return_on_error=False,
            retry_attempts=99,
        )

        # - Add the credentials to the associated nodes as self.
        if master_response.ok:
            association_certificate: RequestPayloadContext = (
                await master_response.json()
            )

            insert_fetched_certificate_query: Insert = associated_nodes.insert().values(
                user_address=auth_source,
                certificate=association_certificate["certificate_token"],
                # * The following fields are not needed throughout the runtime, but is required due to constraint.
                # ! Not that these variables does not represent the current node but rather the target node.
                source_address=master_origin_address,
                source_port=master_origin_port,
            )

            await gather(
                self.__database_instance.execute(insert_fetched_certificate_query),
                save_database_state_to_volume_storage(),
            )

            logger.info("Generation of Association certificate token were successful!")

            return association_certificate["initial_consensus_sleep_seconds"]

        else:
            logger.error(
                f"Generation of association certificate is not successful due to rejection or no reply from the {NodeType.MASTER_NODE.name}"
            )

            return None

    async def _get_consensus_certificate(
        self, *, address_ref: AddressUUID | None = None
    ) -> str:

        resolved_address: AddressUUID = (
            self.__identity[0] if address_ref is None else address_ref
        )

        find_existing_certificate_query = select(
            [associated_nodes.c.certificate]
        ).where(associated_nodes.c.user_address == resolved_address)

        return await self.__database_instance.fetch_val(find_existing_certificate_query)
