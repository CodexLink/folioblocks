from aiohttp import ClientSession
from typing import Any
from core.constants import QueueStatus, QueueTaskType


class HTTPClient:
    """
    This class is just a mini-handler that can be called across the codebase to ensure that there's only one session and a request that will be instantiated.

    Also, there are some addtional features added to ensure that there is a management from initiated requests.

    TODO: Note that we may need to ensure the database implementation regarding lost work.
    """

    def __init__(self, *args, **kwargs) -> None:
        self._queue: list[Any] = []
        self._is_ready: bool = False

    # We can create a pool here if we want that.

    async def initialize(self):
        self._session = ClientSession()

    async def _insert_request(self) -> None:
        # TODO: QueueStatus
        # self._queue.append()
        pass

    # TODO: We need to do the FILO here to remove the at_queue.
    # TODO: When empty we need to handle its exception (custom???)
    async def _run_request(self) -> None:
        pass

    async def _sync_state_to_database(self) -> None:
        pass

    async def close(self) -> None:
        return await self._session.close()

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    @property
    def get_current_queue(self) -> Any:
        pass

    @property
    def get_remaining_request(self) -> Any:
        pass
