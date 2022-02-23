"""
Constants for the Blockchain (Node) System.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from enum import Enum, IntEnum, auto
from pathlib import Path

# * Libraries
from typing import Any, Final
from typing import NewType as _N

from sqlalchemy import Enum as SQLEnum


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
KeyContext = _N("KeyContext", str)
GenericUUID = _N("GenericUUID", str)
HashUUID = _N("HashUUID", str)
InternExperience = _N("InternExperience", DocumentSet)
NodeRole = _N("NodeRole", str)
JWTToken = _N("JWTToken", str)
ProgramMetadata = _N("ProgramMetadata", str)
RegExp = _N("RegExp", str)
RuntimeLoop = _N("RuntimeLoop", str)
RequestContext = _N("RequestContext", str)
URLAddress = _N("URLAddress", str)
UserRole = _N("UserRole", str)
TxID = _N("TxID", str)
WorkExperience = _N("WorkExperience", DocumentSet)

# # Constants, Auth

FERNET_KEY_LENGTH: Final[int] = 44
SECRET_KEY_LENGTH: Final[int] = 32
AUTH_FILE_NAME: Final[str] = ".env"
JWT_ALGORITHM: Final[str] = "HS256"

# # Constants, General
ENUM_NAME_PATTERN: RegExp = RegExp(r"[A-Z]")
ASYNC_TARGET_LOOP: Final[str] = "uvicorn"


# # Constants, Database
DATABASE_NAME: Final[str] = "folioblocks-node.db"
DATABASE_RAW_PATH: str = f"{Path(__file__).cwd()}/{DATABASE_NAME}"
DATABASE_URL_PATH: str = f"sqlite:///{DATABASE_RAW_PATH}"

# # Constraints — Node Operation Parameter
NODE_LIMIT_NETWORK: Final[
    int
] = 5  # The number of nodes that should exists in the network. Master node will reject any connections when the pool is full.
NODE_IP_URL_TARGET: Final[
    str
] = "localhost"  # The IP address that any instance of the program will check for any existing nodes.
NODE_IP_PORT_FLOOR: int = 5001  # Contains the floor port to be used for generating usable and allowable ports.

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
class LoggerLevelCoverage(Enum):
    DEBUG: Final[str] = "debug"
    INFO: Final[str] = "info"
    WARNING: Final[str] = "warning"
    ERROR: Final[str] = "error"
    CRITICAL: Final[str] = "critical"
    TRACE: Final[str] = "trace"


class NodeRoles(IntEnum):
    MASTER: int = auto()
    SIDE: int = auto()


# # Enums, Database
class Activity(SQLEnum):
    OFFLINE: str = "Offline"
    ONLINE: str = "Online"


class BlacklistDuration(SQLEnum):  # TODO: These may not be official.
    INDEFINITE: str = "Indefine."
    WARN_1: str = "Warn 1: 1 Day."
    WARN_2: str = "Warn 2: 3 Days."
    WARN_3: str = "Warn 3: 7 Days."
    FINAL_WARNING: str = "Final Warning: 2 Weeks."


class GroupType(SQLEnum):
    ORGANIZATION: str = (
        "Organization"  # This covers Employer or any other organization.
    )
    COMPANY_EMPLOYER: str = "Company Employer"
    APPLICANTS: str = "Applicants"


class TokenType(SQLEnum):
    EXPIRED: str = "Token Expired"
    RECENTLY_CREATED: str = "Token Recently Created"
    ON_USE: str = "Token On Use"
    TOKEN_RETAINED_WHILE_EXPIRED: str = "Token Expired but Retained"


class TaskType(Enum):
    NEGOTIATION_INITIAL = "Negotiation Phase: Initial"
    NEGOTIATION_PROCESSING = "Negotiation: Processing"
    NEGOTIATION_RECEIVE_RESULT = "Negotiation: End, Receive Result"
    CONSENSUS_MODE = "Consensus Mode, Block Sync"


class UserType(SQLEnum):
    AS_NODE: str = "Node User"
    AS_USER: str = "Dashboard User"


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
    ArgumentParameter("DEBUG"): ArgumentDescription(
        "Enables some of the debug features."
    ),
    ArgumentParameter("KEY_FILE"): ArgumentDescription(
        "A file that contains a set of keys for encrypting and decrypting information for all transaction-related actions. This argument is not required unless the file has a different name."
    ),
    ArgumentParameter("LOCAL"): ArgumentDescription(
        "When specified, run the blockchain node system with hot reload and other elements that enable debug features. Note that this is discouraged since database does not get into the state of locking since hot reload is messing it. I suggest using external hot reloaders."
    ),
    ArgumentParameter("LOG_LEVEL"): ArgumentDescription(
        "Specifies the level to log in both console and to the file (if enabled). Refer to the Logging Levels of Logging Documentation."
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
