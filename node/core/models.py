"""
FastAPI Models for the API (api.py).

This file is part of Folioblocks.

Folioblocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Folioblocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Folioblocks. If not, see <https://www.gnu.org/licenses/>.
"""

from pydantic import BaseModel, Field

# ! Note that we can use one the exclude or include functionality upon returning the context of these models.

# Model for the Blocks inside of the Node, in the means of block that is chained altogether.
class Blockchain(BaseModel):
    pass

# Model for the Block Details
class BlockContext(BaseModel):
    pass

class NodeLoginContext(BaseModel):
    pass

