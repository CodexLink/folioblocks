from logging import Logger, getLogger
from typing import Any, Callable
from core.constants import NodeType
from core.constants import ASYNC_TARGET_LOOP
from utils.processors import unconventional_terminate

# - Parameterized Decorator | Based: https://www.geeksforgeeks.org/creating-decorator-inside-a-class-in-python/, Adapted from https://stackoverflow.com/questions/5929107/decorators-with-parameters

logger: Logger = getLogger(ASYNC_TARGET_LOOP)


def ensure_blockchain_ready(
    message: str = "Blockchain system is not yet ready!",
    terminate_on_call: bool = False,
) -> Callable:
    def deco(fn: Callable) -> Callable:
        def instance(
            self: Any, *args: list[Any], **kwargs: dict[Any, Any]
        ) -> Callable | None:
            if self.is_blockchain_ready:
                return fn(self, *args, **kwargs)

            if terminate_on_call:
                unconventional_terminate(message=message)

            return None

        return instance

    return deco


def restrict_call(*, on: NodeType) -> Callable:
    """
        Restricts the method to be called depending on their `self.role`.
        Since most of the methods is designed respectively based on their role.
        Ever process requires this certain role to only call this method and nothing else.

        Args:
            on (NodeType): The `role` of the node.
    Returns:
            Callable: Calls the decorator method.
    Notes:
        # This was duplicated, it was originated from the consensus.py.
        # I cannot get it because its inside of the class and it doesn't get shared because it has not `self` attribute.
    """

    def deco(fn: Callable) -> Callable:
        def instance(
            self: Any, *args: list[Any], **kwargs: dict[Any, Any]
        ) -> Callable | None:
            if self.role == on:
                return fn(self, *args, **kwargs)

            logger.warning(
                f"Your role {self.role} cannot call the following method `{fn.__name__}` due to role restriction, which prohibits '{on}' from accessing this method."
            )
            return None

        return instance

    return deco
