"""
Custom Exceptions (exceptions.py) | A set of custom reference for all processes (functions) to raise at.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from logging import Logger, getLogger
from typing import Any, Callable, Final

from core.constants import (
    ASYNC_TARGET_LOOP,
    MAX_JWT_HOLD_TOKEN,
    AddressUUID,
    CredentialContext,
    Expects,
    Has,
)

logger: Logger = getLogger(ASYNC_TARGET_LOOP)


class ConversionUnequalLength(AssertionError):
    def __init__(
        self, left_size: int, right_size: int, context: str | None = None
    ) -> None:

        message: Final[str] = (
            f"The left-hand item has a size of {left_size} while right-hand item has a size of {right_size}, thurs unequal.%s"
            % (f"| Additional Info: {context}" if context else "")
        )

        logger.exception(message)
        super().__init__()


class MaxJWTOnHold(AssertionError):
    def __init__(
        self,
        uuids: tuple[AddressUUID, CredentialContext],
        currently_has: int,
        max_hold: int = MAX_JWT_HOLD_TOKEN,
    ) -> None:

        message: str = f"This user {uuids[0]} ({uuids[1]}) currently withold/s {currently_has} JWT tokens. The maximum value that the user can withold should be only {max_hold}."

        logger.exception(message)
        super().__init__()


class NoKeySupplied(ValueError):
    def __init__(self, fn_ref: Callable, extra_info: str | None = None) -> None:

        message: str = f"This function / context {fn_ref.__name__} requires a value. | Additional Info: {extra_info}"

        logger.exception(message)
        super().__init__()


class UnsatisfiedClassType(ValueError):
    def __init__(self, has: Expects, expected: Has) -> None:

        message: str = f"The type assertion is unsatisfied. Argument contains {type(has)} when it should be {expected}. This is a development issue, please contact the developer."

        logger.exception(message)
        super().__init__()


class InsufficientCredentials(ValueError):
    def __init__(
        self, what_service: Callable | object, fields_require: list[str] | str
    ) -> None:
        message: str = f"This entity {what_service} requires the following credentals: {fields_require}."

        logger.exception(message)
        super().__init__()


class NamedNonAwaitedResponseRequired(ValueError):
    def __init__(self) -> None:

        message: str = f"The response requires to have a name as this request is not awaited-immediate. Please add a name even when you don't need its response."

        logger.exception(message)
        super().__init__()


class ResponseNotOkay(AssertionError):
    def __init__(self, *, task_name: str, result: Any) -> None:

        message: str = f"The following request '{task_name}' returned an error response. | Context: {result}"
        logger.exception(message)

        super().__init__()
