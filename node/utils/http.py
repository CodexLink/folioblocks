from asyncio import Task, create_task, sleep
from logging import Logger, getLogger
from secrets import token_urlsafe
from typing import Any

from aiohttp import ClientSession
from blueprint.schemas import HTTPRequestPayload
from core.constants import (
    ASYNC_TARGET_LOOP,
    HTTPQueueMethods,
    HTTPQueueResponseFormat,
    HTTPQueueTaskType,
    RequestPayloadContext,
    URLAddress,
)

from utils.exceptions import (
    HTTPClientFeatureUnavailable,
    HTTPResponseNotOkay,
    NamedNonAwaitedResponseRequired,
)

logger: Logger = getLogger(ASYNC_TARGET_LOOP)


class HTTPClient:
    """
    - This class is just a mini-handler that can be called across the codebase to ensure that there's only one session to be instanted, and only one reference to create and receive requests.

    - The only additional features of this implementation is the storage for the requests that is sent off via `create_task()`. It can also await from the create_task via list.

    ! POST-FEATURE: Database implementation.
    - As of now, my time is too short to implement security features that are specifically side-features.
    """

    def __init__(self) -> None:
        self._queue: list[Any] = []
        self._response: RequestPayloadContext = {}
        self._is_ready: bool = False
        self._queue_running: bool = False

    async def initialize(self) -> None:
        self._session = ClientSession()  # * Initialize the ClientSession.
        logger.debug("HTTP client ClientSession initialized.")

        self._is_ready = True
        logger.info("HTTP client is ready to take some requests...")
        create_task(self._queue_iterator_runtime())

    async def enqueue_request(
        self,
        *,
        url: URLAddress,
        data: RequestPayloadContext,
        method: HTTPQueueMethods,
        task_type: HTTPQueueTaskType = HTTPQueueTaskType.UNSPECIFIED_HTTP_REQUEST,
        await_result_immediate: bool = True,
        name: str | None = None,
    ) -> None:
        """
        A method that enqueues request payload to the LIFO list container to execute in burst or for the latter.

        Args:
                                        - request (URLAddress): The `str` that represents the whole structure of the URL including the protocol, host and port.
                                        - method (HTTPQueueMethods): An enum that contains HTTP methods to classify the request.
                                        - task_type (HTTPQueueTaskType, optional): An enum that contains a set of tasks to classify the request. Defaults to HTTPQueueTaskType.UNSPECIFIED_HTTP_REQUEST.
                                        - await_result_immediate (bool, optional): Should this request run under asyncio.create_task() or await them? By doing `await_result_immediate`, it blocks other requests at the LIFO list container as it was prioritized to run first. But you get to have a data to return. Defaults to False.
                                        - name (str, optional): The name of the request. This is required whenever the request is not `await_result_immediate`. Use get_finished_task` to fetch the request.

        Note:
                                        * Despite complexity, I wanted to implement this so that we can query something while needing it later. Aside from stacking request, it is best to have a managing queue to ensure that we get back to them as is.
                                        ! With the name being required when the request is not `await_result_immediate`, in the case of `await_result_immediate` requests, there's no need for the name as it was automatically generated since it returns the values immediately. Having a not `await_result_immediate` doesn't have a name is prohibited because you are technically losing the returned response even though you may or may not need its returned response.
                                        # Sidenote that, this queueing is requried for the consensus mechanism of the blockchain.
        """
        if not self.is_ready:
            logger.warning(
                "Enqueued requests is not possible to be executed unless this instance executes its initialize() method."  # TODO: Shall we ignore such request on outbound is_ready?
            )

        response_name: str = ""

        if name is None and not await_result_immediate:
            raise NamedNonAwaitedResponseRequired

        elif name is None and await_result_immediate:
            response_name = f"response_{token_urlsafe(8)}"
            logger.debug(
                f"This request doesn't have a name and is awaited (`await_result_immediate`). Named as {response_name} (generated) for log clarity."
            )

        elif name is not None and await_result_immediate:
            logger.warning(
                f"This request is named as '{name}' will not save its result / resposne in the queue for result caching, please catch the result instead."
            )

        # Resolve conflict references as one.
        name = name if name is not None else response_name

        if self._response.get(name, None) is not None:
            logger.error(
                f"One of the request conflicts with the name '{name}'. Please set new request to be distinctive with other request."
            )
            return

        wrapped_request = HTTPRequestPayload(
            url=url,
            data=data,
            method=method,
            task_type=task_type,
            await_result_immediate=await_result_immediate,
            name=name,
        )

        self._queue.append(wrapped_request)

        if await_result_immediate and self._is_ready:
            await self.get_finished_task(task_name=name)

        elif await_result_immediate and not self._is_ready:
            logger.critical(
                f"This instance is not yet initialized (from: {self.enqueue_request.__name__}). Please execute initialize() first before attempting to enqueue requests that requires to have its data to be returned immediately."
            )

    async def _queue_iterator_runtime(self) -> None:
        if not self._is_ready:
            logger.warning(
                f"You cannot initialize this iterator '{self._queue_iterator_runtime.__name__}' unless this instance's initialize() method has been executed."
            )
            return

        while True:
            if self._queue:
                create_task(self._run_request())
            await sleep(1)

    async def _run_request(self) -> None:
        if not self._is_ready:
            logger.warning(
                f"You cannot initialize this request executor '{self._run_request.__name__}' unless this instance's initialize() method has been executed."
            )
            return

        for loaded_request in self._queue:
            requested_item = getattr(self._session, loaded_request.method.name.lower())(
                url=loaded_request.url, data=loaded_request.data
            )
            logger.debug(
                f"Request {loaded_request.name} (Method: {loaded_request.method.name}, with context: {loaded_request.data}) has been generated as a wrapper (to the raw request) to enqueue."
            )

            self._response[loaded_request.name] = create_task(
                name=loaded_request.name, coro=requested_item
            )  ## Enqueue to self.request as dict.

            ## Dequeue that item from self._queue as its response form has been enqueued from the self._response.
            self._queue.pop(self._queue.index(loaded_request))
            logger.debug(
                f"Wrapped Request '{loaded_request.name}' has been enqueued. | Wrapped Object Info: {requested_item}"
            )

    async def get_finished_task(
        self, *, task_name: str, raise_on_not_ok: bool = False
    ) -> Any:
        fetched_task = self._response.get(task_name, None)

        if not self._is_ready:
            logger.warning(
                "There is no finished task since no task has been executed. Please execute initialize() method for this instance to work as intended."
            )
            return

        if fetched_task is not None:
            if not fetched_task.done():
                logger.warning(
                    f"The following task '{task_name}' is not yet finished! Awaiting ..."
                )
                await fetched_task

            if raise_on_not_ok and not fetched_task.result().ok:
                raise HTTPResponseNotOkay(
                    task_name=task_name, result=fetched_task.result()
                )

            self._response.pop(task_name)
            return fetched_task.result()

        else:
            logger.error(
                f"The mentioned task '{task_name}' does not exist from the queue. Please try agian."
            )

    async def close(self, *, should_destroy: bool = False) -> None:
        while True:
            if self._response:
                logger.info(
                    f"Attempting to %s all ({len(self._response)}) request/s left..."
                    % ("finish" if not should_destroy else "destroy")
                )

                if should_destroy:
                    for each_left_task in self._response.values():
                        each_left_task.cancel()
                        self._response.popitem()
                    break

                await sleep(1)
                continue

            break

        logger.info("All requests done! HTTP client sessions will close.")
        return await self._session.close()

    async def _sync_state_to_database(
        self,
    ) -> None:
        logger.debug("Syncing unfinished tasks to the database (if there is any)...")
        raise HTTPClientFeatureUnavailable

    def get_current_queue(  # * This is just an extra.
        self, format: HTTPQueueResponseFormat = HTTPQueueResponseFormat.AS_OBJECT
    ) -> HTTPRequestPayload | RequestPayloadContext | bytes | None:

        if self._queue:
            if format == HTTPQueueResponseFormat.AS_DICT:
                return self._queue[0].dict()
            elif format == HTTPQueueResponseFormat.AS_JSON:
                return self._queue[0].json()
            else:
                return self._queue[0]
        else:
            logger.error("There are no task on queue.")
            return None

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    @property
    def get_remaining_requests(self) -> RequestPayloadContext:
        logger.warning(
            "Function requested to get a view of the remaining request from the HTTP client."
        )
        return self._response

    @property
    def get_remaining_queue(self) -> list[Task]:
        logger.warning(
            "Function requested to get a view of the remaining queue from the HTTP client."
        )
        return self._queue


client_session: HTTPClient | None = None


def get_http_client_instance() -> HTTPClient:
    global client_session

    logger.debug("Initializing or returning HTTP client instance ...")

    if client_session is None:
        client_session = HTTPClient()
        logger.debug(
            "HTTP client instance instantiated! Returning to the requestor ..."
        )
    else:
        logger.debug("HTTP client instance retrieved, returning to the requestor ...")

    return client_session
