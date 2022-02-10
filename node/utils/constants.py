"""
Constants for the Blockchain (Node) System.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from enum import Enum, IntEnum, auto
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING

# * Libraries
from typing import Any, Final
from typing import NewType as _N


# Priority Classification Types
class DocToRequestTypes(IntEnum):
    # TODO: We need more information. Preferrable under
    TOR: int = auto()
    SPECIFIED: int = auto()


# Custom Variable Types
NotificationContext = list[dict[str, Any]]
RoleContext = dict[str, Any]
DocumentSet = list[dict[str, Any]]

# Custom Assertable Types
# TODO: DocumentSet is unconfirmed because I don't have proper vision of what would be the output.
AcademicExperience = _N("AcademicExperience", str)
AddressUUID = _N("AddressUUID", str)
ArgumentParameter = _N("ArgumentParameter", str)
ArgumentDescription = _N("ArgumentDescription", str)
BlockID = _N("BlockID", str)
Certificates = _N("Certificates", DocumentSet)
CredentialContext = _N("CredentialContext", str)
DocRequestType = _N("DocRequestType", DocToRequestTypes)
Documents = _N("Documents", DocumentSet)
DocumentMeta = _N("DocumentMeta", str)
DocumentProof = _N("DocumentProof", DocumentSet)
GenericUUID = _N("GenericUUID", str)
HashUUID = _N("HashUUID", str)
InternExperience = _N("InternExperience", DocumentSet)
NodeRoles = _N("NodeRoles", str)
JWTToken = _N("JWTToken", str)
ProgramMetadata = _N("ProgramMetadata", str)
RegExp = _N("RegExp", str)
RequestContext = _N("RequestContext", str)
URLAddress = _N("URLAddress", str)
UserRole = _N("UserRole", str)
TxID = _N("TxID", str)
WorkExperience = _N("WorkExperience", DocumentSet)

# # Constants
ENUM_NAME_PATTERN: str = RegExp(r"[A-Z]")

# # Constraints — Node Operation Parameter
NODE_LIMIT_NETWORK: Final[
    int
] = 5  # The number of nodes that should exists in the network. Master node will reject any connections when the pool is full.
NODE_IP_URL_TARGET: Final[
    str
] = "localhost"  # The IP address that any instance of the program will check for any existing nodes.
NODE_IP_PORT_FLOOR: int = 5000  # Contains the floor port to be used for generating usable and allowable ports.

# # Enums - API Models
class BaseAPI(Enum):
    DASHBOARD: str = "Dashboard API"
    EXPLORER: str = "Explorer API"
    NODE: str = "Node API"


class DashboardAPI(Enum):
    DASHBOARD_GENERAL_API: str = f"{BaseAPI.DASHBOARD.value}: General"
    APPLICANT_API: str = f"{BaseAPI.DASHBOARD.value}: Applicant"
    EMPLOYER_API: str = f"{BaseAPI.DASHBOARD.value}: Employer"
    INSTITUTION_API: str = f"{BaseAPI.DASHBOARD.value}: Institution"


class ExplorerAPI(Enum):
    GENERAL_FETCH: str = f"{BaseAPI.EXPLORER.value}: General Fetch"
    LIST_FETCH: str = f"{BaseAPI.EXPLORER.value}: List Fetch"
    SPECIFIC_FETCH: str = f"{BaseAPI.EXPLORER.value}: Specific Fetch"
    BLOCK_FETCH: str = f"{BaseAPI.EXPLORER.value}: Block Fetch"
    TRANSACTION_FETCH: str = f"{BaseAPI.EXPLORER.value}: Transaction Fetch"
    ADDRESS_FETCH: str = f"{BaseAPI.EXPLORER.value}: Address Fetch"


class NodeAPI(Enum):
    GENERAL_NODE_API: str = f"{BaseAPI.NODE.value}: Overview"
    MASTER_NODE_API: str = f"{BaseAPI.NODE.value}: Master Node"
    SIDE_NODE_API: str = f"{BaseAPI.NODE.value}: Side Node"
    NODE_TO_NODE_API: str = f"{BaseAPI.NODE.value}: Node-to-Node"


class TransactionStatus(IntEnum):
    PENDING: int = auto()
    SUCCESS: int = auto()
    FAILED: int = auto()


class TransactionActions(IntEnum):  # TODO: This will be expanded later on.
    ACCOUNT_GENERATED: int = auto()
    DATA_UPDATED: int = auto()
    DATA_DISREGARDED: int = auto()
    DATA_BATCH_MINTING: int = auto()
    DOCUMENT_INSUANCE: int = auto()
    REQUEST_INITIATION: int = auto()
    REQUEST_PROCESSING: int = auto()
    REQUEST_MARKED_ENDED: int = auto()
    REQUEST_SPECIFIC_DOC: int = auto()


class TransactionActionString(Enum):
    pass


# # Enums, Constraints
# ! Blockchain (Explorer) Query
# These are the min and max constraint for querying blockchain data.
class ItemReturnCount(IntEnum):
    LOW: Final[int] = 5
    MIN: Final[int] = 25
    MID: Final[int] = 50
    HIGH: Final[int] = 75
    MAX: Final[int] = 100


# ! Logger Level
class LoggerLevelCoverage(IntEnum):
    DEBUG: Final[int] = DEBUG
    INFO: Final[int] = INFO
    WARNING: Final[int] = WARNING
    ERROR: Final[int] = ERROR
    CRITICAL: Final[int] = CRITICAL


class LoggerTarget(IntEnum):
    LOG_UVICORN: int = auto()
    LOG_MAIN: int = auto()
    LOG_ALL: int = auto()


class NodeRoles(IntEnum):
    MASTER: int = auto()
    SIDE: int = auto()


# Program Metadata
FOLIOBLOCKS_NODE_TITLE: Final[ProgramMetadata] = ProgramMetadata(
    "FolioBlocks - Blockchain Backend (Side | Master) Node API Service (node.py)"
)
FOLIOBLOCKS_NODE_DESCRIPTION: Final[ProgramMetadata] = ProgramMetadata(
    "The backend component of the blockchain system 'folioblocks' | Credential Verification System using Blockchain Technology"
)
FOLIOBLOCKS_EPILOG: Final[ProgramMetadata] = ProgramMetadata(
    "The use of arguments are intended for debugging purposes and development only. Please be careful and be vigilant about the requirements to make certain arguments functioning."
)
FOLIOBLOCKS_HELP: Final[dict[ArgumentParameter, ArgumentDescription]] = {
    ArgumentParameter("LOCAL"): ArgumentDescription(
        "When specified, run the blockchain node system with hot reload and other elements that enables debug features."
    ),
    ArgumentParameter("LOG_LEVEL"): ArgumentDescription(
        "Specifies the level to log in both console and to the file (if enabled). Refer to the Logging Levels of Logging Documentation."
    ),
    ArgumentParameter("LOG_TARGET"): ArgumentDescription(
        "Logs a specific part of the runtime. You can either log the uvicorn (fastapi) instance or log the custom logs provided at several functions. Or just both. Note that by providing both means two files will be generated since they can't be jointed at one file."
    ),
    ArgumentParameter("NO_LOG_FILE"): ArgumentDescription(
        "Disables logging to a file. This assert that the log should be outputted in the CLI."
    ),
    ArgumentParameter("PORT"): ArgumentDescription(
        "Specify the port for this instance. Ensure that this instance is not conflicted with other instances as it will cause to fail before it can get to running its ASGI instance."
    ),
    ArgumentParameter("PREFER_ROLE"): ArgumentDescription(
        f"Assigns a role supplied from this parameter. The role {NodeRoles.MASTER.name} can be enforced once. If there's a node that has a role of {NodeRoles.MASTER.name} before this node, then assign {NodeRoles.SIDE.name} to this node."
    ),
}
