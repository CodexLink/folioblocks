"""
Constants for the Blockchain (Node) System.

This file is part of Folioblocks.

Folioblocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Folioblocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Folioblocks. If not, see <https://www.gnu.org/licenses/>.
"""

# * Libraries
from typing import Final, NewType as _N
from enum import auto, IntEnum

# Custom Types
AddressUUID: _N("AddressUUID", str)
ArgumentParameter = _N("ArgumentParameter", str)
ArgumentDescription = _N("ArgumentDescription", str)
BlockID = _N(BlockID, str)
NodeRoles = _N("NodeRoles", str)
URLAddress = _N("URLAddress", str)
ProgramMetadata = _N("ProgramMetadata", str)
TxID: _N("TxID", str)

# Constraints — Node Operation Parameter
NODE_LIMIT_NETWORK: Final[int] = 5 # The number of nodes that should exists in the network. Master node will reject any connections when the pool is full.
NODE_IP_URL_TARGET: Final[str] = "localhost" # The IP address that any instance of the program will check for any existing nodes.
NODE_IP_PORT_FLOOR: int = 5000 # Contains the floor port to be used for generating usable and allowable ports.

# Variable Constants
NODE_ROLE_CHOICES: Final[list[NodeRoles]] = ["MASTER", "SIDE"]

# Enums

class DashboardAPITags(IntEnum):
    GENERAL_API: int = auto()
    CLIENT_ONLY_API: int = auto()
    APPLICANT_ONLY_API: int = auto()
    EMPLOYER_ONLY_API: int = auto()
    INSTITUTION_ONLY_API: int = auto()

class ExplorerAPITags(IntEnum):
    # Overall
    GENERAL_FETCH: int = auto()

    # Action-Type
    LIST_FETCH: int = auto()
    SPECIFIC_FETCH: int = auto()

    # Sepcific-Type
    BLOCK_FETCH: int = auto()
    TRANSACTION_FETCH: int = auto()
    ADDRESS_FETCH: int = auto()

class NodeAPITags(IntEnum):
    GENERAL_NODE_API: int = auto()
    MASTER_NODE_API: int = auto()
    SIDE_NODE_API: int = auto()
    NODE_TO_NODE_API: int = auto()

# Constraints — Blockchain (Explorer) Query
# These are the min and max constraint for querying blockchain data.
class ItemReturnCount(IntEnum):
    LOW: Final[int] = 5
    MIN: Final[int] = 25
    MID: Final[int] = 50
    HIGH: Final[int] = 75
    MAX: Final[int] = 100

# Program Metadata
FOLIOBLOCKS_NODE_TITLE: Final[ProgramMetadata] = "Folioblocks - Blockchain Backend (Side | Master) Node API Service (node.py)"
FOLIOBLOCKS_NODE_DESCRIPTION: Final[ProgramMetadata] = "The backend component of the blockchain system 'folioblocks' | Credential Verification System using Blockchain Technology"
FOLIOBLOCKS_EPILOG: Final[ProgramMetadata] = "The use of arguments are intended for debugging purposes and development only. Please be careful and be vigilant about the requirements to make certain arguments functioning."

FOLIOBLOCKS_HELP: Final[dict[ArgumentParameter, ArgumentDescription]] = {
    "NO_LOG_FILE": "Disables logging to a file. This assert that the log should be outputted in the CLI.",
    "PREFER_ROLE": f"Assigns a role supplied from this parameter. The role {NODE_ROLE_CHOICES[0]} can be enforced once. If there's a node that has a role of {NODE_ROLE_CHOICES[0]} before this node, then assign {NODE_ROLE_CHOICES[1]} to this node.",
    "PORT": "",
}
