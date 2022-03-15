"""
Function Decorators (decorators.py) | A set of functions refarrable as decorators to execute before the actual function.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""


from utils.exceptions import UnsatisfiedClassType
from core.constants import CryptFileAction, fn
from typing import cast

# * Ref for the typing a decorator: https://stackoverflow.com/questions/65621789/mypy-untyped-decorator-makes-function-my-method-untyped
def assert_instance(*, f: fn) -> fn:  #
    def deco(*args):

        # Assert 'to' have CryptFileAction. I prefer isinstance instead of enum.Enum.__members__.
        if not isinstance(args[2], CryptFileAction):  # Can be better.
            raise UnsatisfiedClassType(args[2], CryptFileAction)

        return f(*args)

    return cast(fn, deco)
