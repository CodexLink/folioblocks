from asyncio import Task, create_task, sleep
from logging import Logger, getLogger
from secrets import token_urlsafe
from typing import Any

from aiohttp import (
    ClientConnectionError,
    ClientConnectorError,
    ClientResponse,
    ClientSession,
    ContentTypeError,
)
from blueprint.schemas import HTTPRequestPayload
from core.constants import (
    ASYNC_TARGET_LOOP,
    HTTPQueueMethods,
    HTTPQueueResponseFormat,
    RequestPayloadContext,
    URLAddress,
)
from utils.exceptions import (
    HTTPClientFeatureUnavailable,
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
        self._session = ClientSession()
        logger.debug("HTTP client 'ClientSession' were initialized.")

        create_task(
            name=f"{HTTPClient.__name__.lower()}_queue_iterator",
            coro=self._queue_iterator_runtime(),
        )
        self._is_ready = True
        logger.info("HTTP client is ready to take some requests.")

    async def enqueue_request(
        self,
        *,
        url: URLAddress,
        method: HTTPQueueMethods,
        data: RequestPayloadContext | None = None,
        headers: RequestPayloadContext | None = None,
        await_result_immediate: bool = True,
        do_not_retry: bool = False,
        retry_attempt: int = 5,
        name: str | None = None,
    ) -> Any:
        """
        A method that enqueues request payload to the LIFO list container to execute in burst or for the latter.
        ! Docs OUTDATED.
        Args:
                                        - request (URLAddress): The `str` that represents the whole structure of the URL including the protocol, host and port.
                                        - method (HTTPQueueMethods): An enum that contains HTTP methods to classify the request.
                                        - await_result_immediate (bool, optional): Should this request run under asyncio.create_task() or await them? By doing `await_result_immediate`, it blocks other requests at the LIFO list container as it was prioritized to run first. But you get to have a data to return. Defaults to False.
                                        - name (str, optional): The name of the request. This is required whenever the request is not `await_result_immediate`. Use get_finished_request` to fetch the request.

        Note:
                                        * Despite complexity, I wanted to implement this so that we can query something while needing it later. Aside from stacking request, it is best to have a managing queue to ensure that we get back to them as is.
                                        ! With the name being required when the request is not `await_result_immediate`, in the case of `await_result_immediate` requests, there's no need for the name as it was automatically generated since it returns the values immediately. Having a not `await_result_immediate` doesn't have a name is prohibited because you are technically losing the returned response even though you may or may not need its returned response.
                                        # Sidenote that, this queueing is requried for the consensus mechanism of the blockchain.
        """
        response_name: str = ""

        # # First, resolve the request name before handling the condition if its allowed to be retrieved or enqueued basesd on self.is_ready.
        if name:
            if await_result_immediate:
                logger.warning(
                    f"This request is named as '{name}' will not save its result (response) in the queue for result caching, please catch the result instead, ignore this message if the response is catched."
                )
        else:
            if not await_result_immediate:
                request_payload = HTTPRequestPayload(
                    url=url,
                    data=data,
                    headers=headers,
                    method=method,
                    await_result_immediate=await_result_immediate,
                    name=name,
                )
                logger.error(
                    f"An unnamed response requires to have a name as this request is not awaited-immediate. Please add a name even when you don't need its response. | Response Context: {request_payload}"
                )
                return

            else:
                response_name = f"response_{token_urlsafe(8)}"
                logger.debug(
                    f"This request doesn't have a name and is awaited (`await_result_immediate`). Named as `{response_name}` (generated) for log clarity."
                )

        # Resolve conflict references as one.
        name = name if name else response_name

        if not self._is_ready:
            logger.warning(
                f"Enqueued requests ('{name}' in particular) is not possible to be executed unless this instance executes its initialize() method.%s"
                % (
                    f" This request is invalidated and was not inserted from the queue due to `await_result_immediate` is set to {await_result_immediate}."
                    if await_result_immediate
                    else " This request will be inserted from the queue and retrieve it when this instance is ready."
                )
            )

            if await_result_immediate:
                return

        if self._response.get(name, None) is not None:
            logger.error(
                f"One of the request conflicts with the name '{name}'. Please set new request to be distinctive with other request."
            )
            return

        wrapped_request = HTTPRequestPayload(
            url=url,
            data=data,
            headers=headers,
            method=method,
            await_result_immediate=await_result_immediate,
            name=name,
        )

        logger.info(
            f"The following request '{wrapped_request.name}' (requesting to {url}) has been appended from the queue."
        )
        self._queue.append(wrapped_request)

        if await_result_immediate and self._is_ready:
            logger.debug(
                f"Await-immediate enabled on the following request '{name}' ..."
            )

            request_iterator: int = retry_attempt  # @o Declare here so that, we can break from the inner-while loop (request re-attempt) after executing the outer-while loop (request fetching).
            while True:

                # - Wait for a millisecond to process the request.
                await sleep(
                    0.2
                )  # @o Note that this is not a precise since CPU performance differs from every device.

                res_req_equiv = self.get_remaining_responses.get(name, None)

                logger.debug(
                    f"Attempt #{request_iterator} | Fetching response named as `{name}` ..."
                )

                if res_req_equiv is not None and request_iterator:
                    returned_response: ClientResponse | None = (
                        await self.get_finished_request(request_name=name)
                    )

                    if isinstance(returned_response, ClientResponse):
                        return returned_response

                    if not do_not_retry:
                        logger.warning(
                            f"Attempt #{request_iterator} | Seems like the following request {wrapped_request.name} has failed or contains nothing. Retrying ... "
                        )

                        self._queue.append(wrapped_request)
                        request_iterator -= 1
                        await sleep(1.5)
                        continue

                if request_iterator and not do_not_retry:
                    logger.error(
                        f"Attempt #{request_iterator} | Response {name} doesn't exist, for now. Retrying..."
                    )
                    continue

                elif not request_iterator and not do_not_retry:
                    logger.error(
                        "The request attempt has been exceeded. There's something wrong with the request. Please try again later."
                    )
                else:
                    logger.warning("Do not retry has been enabled.")

                break

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
                create_task(
                    name=f"{HTTPClient.__name__}_{self._queue_iterator_runtime.__name__}",
                    coro=self._run_request(),
                )
            await sleep(0)

    async def _run_request(self) -> None:
        if not self._is_ready:
            logger.warning(
                f"You cannot initialize this request executor '{self._run_request.__name__}' unless this instance's initialize() method has been executed."
            )
            return

        for loaded_request in self._queue:
            requested_item = getattr(self._session, loaded_request.method.name.lower())(
                url=loaded_request.url,
                headers=loaded_request.headers,
                json=loaded_request.data,
            )
            logger.debug(
                f"Unwrapped Request '{loaded_request.name}' (Method: {loaded_request.method.name}, with context: {loaded_request.data}) has been generated as a wrapper (to the raw request) to enqueue."
            )

            self._response[loaded_request.name] = create_task(
                name=f"{HTTPClient.__name__.lower()}_{loaded_request.name}_processor",
                coro=requested_item,
            )  ## Enqueue to self.request as dict.

            ## Dequeue that item from self._queue as its response form has been enqueued from the self._response.
            self._queue.pop(self._queue.index(loaded_request))
            logger.debug(
                f"Async-Task-Wrapped Request '{loaded_request.name}' has been enqueued. | Wrapped Object Info: {requested_item}"
            )

    async def get_finished_request(self, *, request_name: str) -> ClientResponse | None:
        fetched_request: Any = self._response.get(request_name, None)

        if not self._is_ready:
            logger.warning(
                "There is no finished task since no task has been executed. Please execute `initialize()` method for this instance to work as intended."
            )
            return None

        if fetched_request is not None:
            logger.info(f"Request '{request_name}' has been fetched.")
            try:
                if not fetched_request.done():
                    logger.warning(
                        f"The following request '{request_name}' is not yet finished! Awaiting ..."
                    )
                    await fetched_request

                if not fetched_request.result().ok:
                    try:
                        response = await fetched_request.result().json()
                    except ContentTypeError:
                        response = "Not Available."

                    logger.error(
                        f"The following request '{request_name}' returned an error response. | Context: {fetched_request.result()}{f' | Response: {response}'}"
                    )

                logger.debug(
                    f"On request, the type of the response is {type(fetched_request.result())}."
                )

            except (
                ConnectionRefusedError,
                ConnectionAbortedError,
                ConnectionResetError,
                ClientConnectionError,
                ClientConnectorError,
            ) as e:
                logger.critical(
                    f"There was error during the process of request. | Info: {e}"
                )
                return None

            finally:
                self._response.pop(request_name)
                logger.debug(
                    f"Request '{request_name}' has been popped from the response queue."
                )

            return fetched_request.result()

        else:
            logger.error(
                f"The following response '{request_name}' does not exist from the queue. Please try again."
            )
            logger.debug(
                f"Currently at Queue (Request), Length: {len(self.get_remaining_enqueued_items)} | {self.get_remaining_enqueued_items}"
            )
            logger.debug(
                f"Currently at Response (Request), Length: {len(self.get_remaining_responses)} | {self.get_remaining_responses}"
            )
            return None

    async def close(self, *, should_destroy: bool = False) -> None:
        while True:
            if self._response:
                logger.info(
                    f"Attempting to %s all ({len(self._response)}) request/s left ..."
                    % ("finish" if not should_destroy else "destroy")
                )

                if should_destroy:
                    _cached = (
                        self._response.copy()
                    )  # ! We need to copy the last state to avoid mutation change during iteration.

                    for each_leftout_request in _cached.values():
                        if self._response.get(each_leftout_request, None) is not None:

                            # * Compare the last state with the currently async-mutated dictionary and remove the element if they are still existing, otherwise ignore it.
                            each_leftout_request.cancel()
                            self._response.popitem()
                    break

                continue

            break

        logger.info("All requests destroyed! HTTP client sessions will close.")
        return await self._session.close()

    async def _sync_state_to_database(
        self,
    ) -> None:
        logger.debug("Syncing unfinished tasks to the database (if there is any) ...")
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
    def get_remaining_responses(self) -> RequestPayloadContext:
        return self._response

    @property
    def get_remaining_enqueued_items(self) -> list[Task]:
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
