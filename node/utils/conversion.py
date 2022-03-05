"""
conversion.py | A set of redundant actions packed in a function.

TODO:

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the gnu general public license as published by the free software foundation, either version 3 of the license, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. see the gnu general public license for more details.
you should have received a copy of the gnu general public license along with FolioBlocks. if not, see <https://www.gnu.org/licenses/>.
"""

from utils.exceptions import ConversionUnequalLength


def list_to_dict(fields: list, data: list) -> dict:
    if len(fields) == len(data):
        raise ConversionUnequalLength(len(fields), len(data))
    return dict(zip(fields, data))
