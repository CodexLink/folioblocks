"""
Custom Exceptions (exceptions.py) | A set of custom reference for all processes (functions) to raise at.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Callable, Final, Type
from core.constants import Expects, Has


class UnsatisfiedClassType(ValueError):
    def __init__(self, has: Type[Expects], expected: Type[Has]) -> None:

        message: str = f"The type assertion is unsatisfied. Argument contains {type(has)} when it should be {expected}. This is a development issue, please contact the developer."

        super().__init__(message)


class NoKeySupplied(ValueError):
    def __init__(self, fn_ref: Callable, extra_info: str | None = None) -> None:

        message: Final[
            str
        ] = f"This function {fn_ref.__name__} requires a value. | Additional Info: {extra_info}"

        super().__init__(message)


class ConversionUnequalLength(AssertionError):
    def __init__(
        self, left_size: int, right_size: int, context: str | None = None
    ) -> None:

        message: Final[str] = (
            f"The left-hand item has a size of {left_size} while right-hand item has a size of {right_size}, thurs unequal.%s"
            % (f"| Additional Info: {context}" if context else "")
        )

        super().__init__(message)
