from logging import Logger, getLogger
from typing import Coroutine

from aiohttp import BasicAuth, ClientResponse, ClientSession

from core.constants import ASYNC_TARGET_LOOP, NodeRoles

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

# There should be a feature where we lock other functions after knowing their role.
class AdaptedPoETConsensus:
    def __init__(self, role: NodeRoles, credentials=dict[str, str]) -> None:
        self.adjacent_nodes: list[
            object
        ] = []  # TODO: Create pydantic model of a NodeEntity (as Node).

        self._consensus_http_session: ClientSession = ClientSession()

        logger.info("Attempting to what...")

    # Calls on replace if not.
    async def is_valid(self) -> None:
        pass

    # Any nodes who respond to this will automatically be placed from the frozendict or just a set or dict, whatever, that can be called for the initiate_consensus later.
    async def echo(self) -> None:
        pass

    # This function is just an API endpoin
    async def acknowledge(self) -> None:  # Of what???
        pass

    async def initiate(self) -> None:
        pass

    async def resolve(self) -> None:
        pass

    async def close(self) -> Coroutine:
        return self._consensus_http_session.close()
