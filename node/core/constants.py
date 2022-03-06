"""
Literal Constants (constants.py) | A set of variables for references for the components that needs it.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from enum import Enum, IntEnum, auto
from pathlib import Path
from typing import Any, Final
from typing import NewType as _N
from typing import TypeVar, Union

from asgiref.typing import ASGIApplication


# ! Priority Classification Types
class DocToRequestTypes(IntEnum):
    # TODO: We need more information. Preferrable under
    TOR = auto()
    SPECIFIED = auto()


# # Custom Variable Types
NotificationContext = list[dict[str, Any]]
RoleContext = dict[str, Any]
DocumentSet = list[dict[str, Any]]

# # Custom Assertable Types
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
HashedData = _N("HashedData", str)
InternExperience = _N("InternExperience", DocumentSet)
IPAddress = _N("IPAddress", str)
IPPort = _N("IPPort", int)
NodeRole = _N("NodeRole", str)
JWTToken = _N("JWTToken", str)
ProgramMetadata = _N("ProgramMetadata", str)
RawData = _N("RawData", str)
RegExp = _N("RegExp", str)
RuntimeLoop = _N("RuntimeLoop", str)
RequestContext = _N("RequestContext", str)
URLAddress = _N("URLAddress", str)
UserRole = _N("UserRole", str)
TxID = _N("TxID", str)
WorkExperience = _N("WorkExperience", DocumentSet)

# # Custom Typed Types
# * For the exceptions.
Expects = TypeVar("Expects")
Has = TypeVar("Has")

# # Constants, Auth
FERNET_KEY_LENGTH: Final[int] = 44  # TODO: ???
SECRET_KEY_LENGTH: Final[int] = 32  # TODO: ???
MAX_JWT_HOLD_TOKEN: Final[int] = 5

UUID_KEY_PREFIX: Final[str] = "fl"
UUID_KEY_LENGTH: Final[int] = 35
AUTH_FILE_NAME: Final[str] = ".env"

# # Constants, Auth: JWT
JWT_DAY_EXPIRATION: Final[int] = 7
JWT_ALGORITHM: Final[str] = "HS256"

# # Constants, Auth: SMTP Email

DEFAULT_SMTP_URL: Final[str] = "smtp.gmail.com"
DEFAULT_SMTP_PORT: Final[int] = 465
DEFAULT_SMTP_CONNECT_MAX_RETRIES: Final[int] = 10

# # Constants, General
ENUM_NAME_PATTERN: RegExp = RegExp(r"[A-Z]")
ASYNC_TARGET_LOOP: Final[str] = "uvicorn"
ASGI_APP_TARGET: Union[ASGIApplication, str] = "__main__:api_handler"

# # Constants, Resources
DATABASE_NAME: Final[str] = "folioblocks-node.db"
DATABASE_RAW_PATH: str = f"{Path(__file__).cwd()}/{DATABASE_NAME}"
DATABASE_URL_PATH: str = f"sqlite:///{DATABASE_RAW_PATH}"

BLOCKCHAIN_NAME: Final[str] = "folioblocks-chain.json"
BLOCKCHAIN_RAW_PATH: str = f"{Path(__file__).cwd()}/{BLOCKCHAIN_NAME}"

# # Constants, Template Models with Pydantic
# ! These are used when initializing new resources.

# BLOCKCHAIN_BLOCK_TEMPLATE = {}
# BLOCKCHAIN_TRANSACTION_TEMPLATE = {}

# BLOCKCHAIN_

# # Constraints — Node Operation Parameter
NODE_LIMIT_NETWORK: Final[
    int
] = 5  # The number of nodes that should exists in the network. Master node will reject any connections when the pool is full.
NODE_IP_URL_TARGET: Final[
    str
] = "localhost"  # The IP address that any instance of the program will check for any existing nodes.
NODE_IP_ADDR_FLOOR: IPAddress = IPAddress("127.0.0.1")
NODE_IP_PORT_FLOOR: IPPort = IPPort(
    5001
)  # Contains the floor port to be used for generating usable and allowable ports.

# # Enums - API Models
class BaseAPI(Enum):
    ADMIN = "Admin API"
    DASHBOARD = "Dashboard API"
    ENTITY = "Entity API"
    EXPLORER = "Explorer API"
    NODE = "Node API"

    """
    Note that, we only need to govern the user for becoming as a Node User or as an organization representative.
    """


class AdminAPI(Enum):
    REQUEST_TO_ACCESS = f"{BaseAPI.ADMIN.value}: Access Generators"
    # REQUEST_AS_ORG = ""


class DashboardAPI(Enum):
    DASHBOARD_GENERAL_API = f"{BaseAPI.DASHBOARD.value}: General"
    APPLICANT_API = f"{BaseAPI.DASHBOARD.value}: Applicant"
    EMPLOYER_API = f"{BaseAPI.DASHBOARD.value}: Employer"
    INSTITUTION_API = f"{BaseAPI.DASHBOARD.value}: Institution"


class EntityAPI(Enum):
    ENTITY_GENERAL_API = f"{BaseAPI.ENTITY.value}: General"
    LOGIN_API = f"{BaseAPI.ENTITY.value}: Login"
    REGISTRATION_API = f"{BaseAPI.ENTITY.value}: Registration"


class ExplorerAPI(Enum):
    GENERAL_FETCH = f"{BaseAPI.EXPLORER.value}: General Fetch"
    LIST_FETCH = f"{BaseAPI.EXPLORER.value}: List Fetch"
    SPECIFIC_FETCH = f"{BaseAPI.EXPLORER.value}: Specific Fetch"
    BLOCK_FETCH = f"{BaseAPI.EXPLORER.value}: Block Fetch"
    TRANSACTION_FETCH = f"{BaseAPI.EXPLORER.value}: Transaction Fetch"
    ADDRESS_FETCH = f"{BaseAPI.EXPLORER.value}: Address Fetch"


class NodeAPI(Enum):
    GENERAL_NODE_API = f"{BaseAPI.NODE.value}: Overview"
    MASTER_NODE_API = f"{BaseAPI.NODE.value}: Master Node"
    SIDE_NODE_API = f"{BaseAPI.NODE.value}: Side Node"
    NODE_TO_NODE_API = f"{BaseAPI.NODE.value}: Node-to-Node"


class TransactionStatus(IntEnum):
    PENDING = auto()
    SUCCESS = auto()
    FAILED = auto()


class TransactionActions(IntEnum):  # TODO: This will be expanded later on.
    ACCOUNT_GENERATED = auto()
    DATA_UPDATED = auto()
    DATA_DISREGARDED = auto()
    DATA_BATCH_MINTING = auto()
    DOCUMENT_INSUANCE = auto()
    REQUEST_INITIATION = auto()
    REQUEST_PROCESSING = auto()
    REQUEST_MARKED_ENDED = auto()
    REQUEST_SPECIFIC_DOC = auto()


class TransactionActionString(Enum):
    pass


# # Enums, Constraints
# ! Blockchain (Explorer) Query
# These are the min and max constraint for querying blockchain data.
class ItemReturnCount(IntEnum):
    LOW = 5
    MIN = 25
    MID = 50
    HIGH = 75
    MAX = 100


# ! Logger Level
class LoggerLevelCoverage(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    TRACE = "TRACE"


class NodeRoles(Enum):
    MASTER = "MASTER"
    SIDE = "SIDE"


# # Enums, Database
class BlacklistDuration(Enum):  # TODO: These may not be official.
    INDEFINITE = "Indefine."
    WARN_1 = "Warn 1: 1 Day."
    WARN_2 = "Warn 2: 3 Days."
    WARN_3 = "Warn 3: 7 Days."
    FINAL_WARNING = "Final Warning: 2 Weeks."


class GroupType(Enum):
    ORGANIZATION = "Organization"  # This covers Employer or any other organization.
    COMPANY_EMPLOYER = "Company Employer"
    APPLICANTS = "Applicants"


class TokenStatus(Enum):
    EXPIRED = "Token Expired"
    RECENTLY_CREATED = "Token Recently Created"
    ON_USE = "Token On Use"
    TOKEN_RETAINED_WHILE_EXPIRED = "Token Expired but Retained"


class TaskType(Enum):
    NEGOTIATION_INITIAL = "Negotiation Phase: Initial"
    NEGOTIATION_PROCESSING = "Negotiation: Processing"
    NEGOTIATION_RECEIVE_RESULT = "Negotiation: End, Receive Result"
    CONSENSUS_MODE = "Consensus Mode, Block Sync"


class UserActivityState(Enum):
    OFFLINE = "Offline"
    ONLINE = "Online"


class UserEntity(Enum):
    NODE_USER = "Node User"
    DASHBOARD_USER = "Dashboard User"
    ADMIN_USER = "Administrator"


# # Enums, Generic
class CryptFileAction(IntEnum):
    TO_DECRYPT = auto()
    TO_ENCRYPT = auto()


class FuncProcessState(IntEnum):
    SUCCESS = auto()
    FAILED = auto()
    SUCCESS_WITH_WARNING = auto()
    FAILED_WITH_WARNING = auto()


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
    ArgumentParameter("HOST"): ArgumentDescription(
        "The IP address that this instance is going to allocate from a machine. This should be the base IP address that other nodes should use in order to communicate from each other."
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
