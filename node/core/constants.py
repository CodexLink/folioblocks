"""
Literal Constants (constants.py) | A set of variables for references for the components that needs it.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from argparse import Namespace
from datetime import timedelta
from enum import Enum, IntEnum, auto
from pathlib import Path
from typing import Any, Callable, Final
from typing import NewType as _N
from typing import TypeVar, Union

from asgiref.typing import ASGIApplication
from secrets import SystemRandom

from databases import Database


# # Custom Assertable Types
# TODO: DocumentSet is unconfirmed because I don't have proper vision of what would be the output.
AcademicExperience = _N("AcademicExperience", str)
AddressUUID = _N("AddressUUID", str)
ArgumentParameter = _N("ArgumentParameter", str)
ArgumentDescription = _N("ArgumentDescription", str)
AuthAcceptanceCode = _N("AuthAcceptanceCode", str)
BlockID = _N("BlockID", str)
BlockchainFileContext = _N("BlockchainFileContext", str)
CredentialContext = _N("CredentialContext", str)
DocRequestType = _N("DocRequestType", DocToRequestTypes)
DocumentMeta = _N("DocumentMeta", str)
GenericUUID = _N("GenericUUID", str)
HashUUID = _N("HashUUID", str)
HashedData = _N("HashedData", str)
IPAddress = _N("IPAddress", str)
IPPort = _N("IPPort", int)
NodeRole = _N("NodeRole", str)
JWTToken = _N("JWTToken", str)
ProgramMetadata = _N("ProgramMetadata", str)
RandomUUID = _N("RandomUUID", str)
RawData = _N("RawData", str)
RegExp = _N("RegExp", str)
RuntimeLoopContext = _N("RuntimeLoopContext", str)
RequestContext = _N("RequestContext", str)
URLAddress = _N("URLAddress", str)
UserRole = _N("UserRole", str)
TxID = _N("TxID", str)

# # Custom Variable Types
BlockchainPayload = tuple[HashUUID, BlockchainFileContext]
DocumentSet = list[dict[str, Any]]
IdentityTokens = tuple[AddressUUID, JWTToken]
NotificationContext = list[dict[str, Any]]
BlockchainNodeStatePayload = dict[str, bool | timedelta | int]
RequestPayloadContext = dict[str, Any]
RoleContext = dict[str, Any]
ArgsPlusDatabaseInstances = tuple[Namespace, Database]
UserCredentials = tuple[CredentialContext, CredentialContext]
NodeCredentials = tuple[CredentialContext, CredentialContext]


# # Custom Typed Types
# * For the exceptions.
Expects = TypeVar("Expects", str, object)
Has = TypeVar("Has", str, object)
KeyContext = TypeVar("KeyContext", str, bytes, None)
fn = TypeVar(  # ! Doesn't work for now.
    "fn", bound=Callable[..., Any]
)  # https://stackoverflow.com/questions/65621789/mypy-untyped-decorator-makes-function-my-method-untyped

# # Constants, API
QUERY_CURRENT_INDEX_PAGE_NAME: Final[str] = "Current Index Page"
QUERY_CURRENT_INDEX_NAME_DESCRIPTION: Final[
    str
] = "The page you are currently sitting, defaults to page 1. Other pages are available if the `<context>_count` is higher than the number of returned blocks."

QUERY_TRANSACTION_RETURN_NAME: Final[str] = "Number of Transaction Return"
QUERY_TRANSACTION_RETURN_DESCRIPTION: Final[
    str
] = "The number of transactions to return."

# # Constants / Constraints, Auth
AUTH_KEY: Final[str] = "AUTH_KEY"
SECRET_KEY: Final[str] = "SECRET_KEY"
BLOCK_HASH_LENGTH: Final[int] = 64
FERNET_KEY_LENGTH: Final[int] = 44
SECRET_KEY_LENGTH: Final[int] = 32
MAX_JWT_HOLD_TOKEN: Final[int] = 5

UUID_KEY_PREFIX: Final[str] = "fl"
UUID_KEY_LENGTH: Final[int] = 35
AUTH_ENV_FILE_NAME: Final[str] = "node-env.vars"

AUTH_CODE_MIN_CONTEXT: Final[int] = 4
AUTH_CODE_MAX_CONTEXT: Final[int] = 32

# # Constants, Blockchain
BLOCKCHAIN_HASH_BLOCK_DIFFICULTY: Final[int] = 4
BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS: Final[int] = 15
BLOCKCHAIN_BLOCK_TIMER_IN_SECONDS: Final[int] = 5
BLOCKCHAIN_MINIMUM_TRANSACTIONS_TO_BLOCK: Final[int] = 5
BLOCKCHAIN_WAIT_TIME_REFRESH_FOR_TRANSACTION: Final[int] = 3

REF_MASTER_BLOCKCHAIN_ADDRESS: Final[str] = "MASTER_NODE_ADDRESS"
REF_MASTER_BLOCKCHAIN_PORT: Final[str] = "MASTER_NODE_PORT"

# # Constants, Auth: JWT
JWT_DAY_EXPIRATION: Final[int] = 7
JWT_ALGORITHM: Final[str] = "HS256"

# # Constants, Auth: Time-based OTP.
TOTP_PASSCODE_REFRESH_INTERVAL: Final[int] = 15
TOTP_VALID_WINDOW_SECONDS: Final[int] = 3

# # Constants, FastAPI Configs
CORS_ALLOW_CREDENTIALS: Final[bool] = True
CORS_ALLOWED_HEADERS: Final[list[str]] = ["*"]
CORS_ALLOWED_METHODS: Final[list[str]] = ["DELETE", "GET", "POST", "PUT"]
CORS_ALLOWED_ORIGINS: Final[list[str]] = ["*"]

# # Constants, General
ENUM_NAME_PATTERN: RegExp = RegExp(r"[A-Z]")
ASYNC_TARGET_LOOP: Final[str] = "uvicorn"
ASGI_APP_TARGET: Union[ASGIApplication, str] = "__main__:api_handler"
INFINITE_TIMER: Final[
    int
] = 4294967295  # * Equivalent of asyncio.windows_events.INFINITE.
# # Constants, Auth: SMTP Email
DEFAULT_SMTP_URL: Final[str] = "smtp.gmail.com"
DEFAULT_SMTP_PORT: Final[int] = 465
DEFAULT_SMTP_CONNECT_MAX_RETRIES: Final[int] = 10
DEFAULT_SMTP_TIMEOUT_CONNECTION: Final[int] = 10

# # Constants, Resources
DATABASE_NAME: Final[str] = "folioblocks-node.db"
DATABASE_RAW_PATH: str = f"{Path(__file__).cwd()}/{DATABASE_NAME}"
DATABASE_URL_PATH: str = f"sqlite:///{DATABASE_RAW_PATH}"

BLOCKCHAIN_NAME: Final[str] = "folioblocks-chain.json"
BLOCKCHAIN_RAW_PATH: str = f"{Path(__file__).cwd()}/{BLOCKCHAIN_NAME}"

# # Constants, Template Models with Pydantic
BLOCKCHAIN_NODE_JSON_TEMPLATE: dict[str, list[Any]] = {"chain": []}

# # Constraints — Node Operation Parameter
MASTER_NODE_LIMIT_CONNECTED_NODES: Final[
    int
] = 4  # - The number of nodes that should exists in the network. Master node will reject any connections when the pool is full.
MASTER_NODE_IP_PORT_FLOOR: Final[int] = 0
MASTER_NODE_IP_PORT_CEILING: Final[int] = 10

# # Constraints — Randomizer
random_generator = SystemRandom()

# # Enums - API Models
class BaseAPI(Enum):
    ADMIN = "Admin API"
    DASHBOARD = "Dashboard API"
    ENTITY = "Entity API"
    EXPLORER = "Explorer API"
    NODE = "Node API"


class AdminAPI(Enum):
    REQUEST_TO_ACCESS = f"{BaseAPI.ADMIN.value}: Access Generators"


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
    ARCHIVAL_MINER_NODE_API = f"{BaseAPI.NODE.value}: Archival Miner (Side) Node"
    NODE_TO_NODE_API = f"{BaseAPI.NODE.value}: Node-to-Node"


# # Enums, Blockchain
class BlockchainIOAction(IntEnum):
    TO_WRITE = auto()
    TO_READ = auto()


class BlockchainContentType(IntEnum):
    ADDRESS = auto()
    TRANSACTION = auto()


# # Enums, Constraints
class ExplorerBlockItemReturnCount(IntEnum):
    LOW = 5
    MIN = 25
    MID = 50
    HIGH = 75
    MAX = 100


class LoggerLevelCoverage(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    TRACE = "TRACE"


class NodeType(Enum):
    MASTER_NODE = "MASTER_NODE"
    ARCHIVAL_MINER_NODE = "ARCHIVAL_MINER_NODE"


# # Enums, Database


class AssociatedNodeStatus(IntEnum):
    CURRENTLY_AVAILABLE = auto()
    CURRENTLY_MINING = auto()
    CURRENTLY_NOT_AVAILABLE = auto()
    CURRENTLY_SLEEPING = auto()


class AssociationGroupType(IntEnum):
    COMPANY = auto()
    INSTITUTION = auto()
    ORGANIZATION = auto()


class EmploymentApplicationState(IntEnum):
    REQUESTED = auto()
    REJECTED = auto()
    ACCEPTED = auto()


class TokenStatus(Enum):
    EXPIRED = "Token Expired"
    CREATED_FOR_USE = "Token Recently Created"
    LOGGED_OUT = "Token Disposed: Logged Out"


class TransactionContextMappingType(IntEnum):
    """This `IntEnum` is an equivalence to <class 'TransactionActions'> from the context of database data insertion. It will be used to identity the data to render from the frontend.

    Args:
        IntEnum: Uses integer `auto()` to classify choices per declaration.
    """

    APPLICANT_INFO = auto()
    APPLICANT_LOG = auto()
    APPLICANT_ADDITIONAL = auto()
    SCHOOL_INFO = auto()
    SCHOOL_ASSOCIATIONS = auto()
    SCHOOL_EXTRA_INFO = auto()


class UserActivityState(Enum):
    OFFLINE = "Offline"
    ONLINE = "Online"


class UserEntity(Enum):
    MASTER_NODE_USER = "Master Node User"
    ARCHIVAL_MINER_NODE_USER = "Archival Miner Node User"
    DASHBOARD_USER = "Dashboard User"
    ADMIN_USER = "Administrator"


# # Enums, Generic
class CryptFileAction(IntEnum):
    TO_DECRYPT = auto()
    TO_ENCRYPT = auto()


# # Enums, HTTP Queues


class HTTPQueueMethods(IntEnum):
    GET = auto()
    POST = auto()
    PUT = auto()
    PATCH = auto()
    DELETE = auto()


class HTTPQueueResponseFormat(IntEnum):
    AS_OBJECT = auto()
    AS_JSON = auto()
    AS_DICT = auto()


class HTTPQueueStatus(IntEnum):
    ON_QUEUE = auto()
    UP_NEXT = auto()
    CURRENTLY_WORKING = auto()


# # Enums, Transaction-Related Attributes
class NodeTransactionInternalActions(IntEnum):
    CONSENSUS = auto()
    INIT = auto()


# # SORT THIS.


class ApplicantLogContentType(IntEnum):
    PROJECT = auto()
    ACTIVITY = auto()
    PROMOTION = auto()
    EMPLOYMENT = auto()


class OrganizationType(IntEnum):
    COMPANY = auto()
    LITERAL = auto()
    SCHOOL = auto()


class EmploymentActivityType(IntEnum):
    ACTIVITIES = auto()
    PROJECTS = auto()
    PROMOTION = auto()


class TransactionContentCategory(IntEnum):
    APPLICANT = auto()
    INSTITUTION_ORG = auto()
    COMPANY_ORG = auto()
    NODE_INTERNAL = auto()


class TransactionStatus(IntEnum):
    SUCCESS = auto()
    FAILED = auto()


class TransactionActions(Enum):
    # - Node-based Transactions: General
    NODE_GENERAL_CONSENSUS_INITIATE = "Node: Certificate Init"
    NODE_GENERAL_REGISTER_INIT = "Node: Register"
    NODE_GENERAL_GENESIS_INITIALIZATION = "Node: Genesis Block Init"

    # - Node-based Transaction: Negotiation (Consensus)
    NODE_GENERAL_CONSENSUS_BLOCK_SYNC = "Consensus: Blockchain Sync"
    NODE_GENERAL_CONSENSUS_NEGOTIATION_MINE = "Consensus: Mine Negotiation"
    NODE_GENERAL_CONSENSUS_NEGOTIATION_PROCESSING_PROOF = (
        "Consensus: Receive Miner Proof"
    )

    # # Note that anything below from this context requires assistance from `models.block_context_mappings`.

    # - For Students as Applicants.
    # * Note that their data cannot be modified since it was the administrator of the institution who does that.

    # @o For the blockchain, just display this, literally.
    APPLICANT_APPLY = "Applicant: Apply Process"
    APPLICANT_APPLY_CONFIRMED = (
        "Applicant: Apply Confirmed"  # * Association should be assigned here.
    )
    APPLICANT_APPLY_REJECTED = "Applicant: Apply Rejected"

    # ! About Classification / Organization
    # # Groups with classification of organization should refer to the actual classification instead of just organization.

    # - For Company / Organization.
    # ! Note that this/these may not be used since our scenario is leaning towards to applicants wanting to get hired by them doing the process.
    COMPANY_INVITE_APPLICANTS = "Company: Invite Applicants"  # * As a workaround, we can do some email send module.

    # - For Institutions / Organization.
    INSTITUTION_ORG_GENERATE_APPLICANT = "Generate Applicants"
    INSTITUTION_ORG_REFER_NEW_DOCUMENT = "Applicant: Document Reference"  # * This is a seperate action. THIS REQUIRES FILE.
    INSTITUATION_ORG_APPLICANT_REFER_EXTRA_INFO = "Applicant: New Info"

    # - For Organization, in general.
    ORGANIZATION_USER_REGISTER = "Org: Authority Register"
    ORGANIZATION_REFER_EXTRA_INFO = "Org: Extra Info"


# # Program Metadata
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
    ArgumentParameter("ASSIGNED_ROLE"): ArgumentDescription(
        f"Assigns and represents the role of this node. Each role in {NodeType} represents different functionality. Please use the assigned role to avoid potential errors."
    ),
    ArgumentParameter("KEY_FILE"): ArgumentDescription(
        "A file that contains a set of keys for encrypting and decrypting information for all transaction-related actions. This argument is a file name and is not required, unless the file has a different name."
    ),
    ArgumentParameter("LOG_LEVEL"): ArgumentDescription(
        "Specifies the level to log both console and to the file (if enabled). Refer to the Logging Levels of logging or uvicorn logs documentation for more information."
    ),
    ArgumentParameter("NODE_HOST"): ArgumentDescription(
        "The IP address that this node instance is going to allocate from the machine."
    ),
    ArgumentParameter("NODE_PORT"): ArgumentDescription(
        "The port associated from the host address where this instance will be established. Ensure that this instance is not conflicted with other instances as it will cause to fail before it can get to run its ASGI instance."
    ),
    ArgumentParameter("NO_LOG_FILE"): ArgumentDescription(
        "Disables logging to a file. This does not however, disables logging through CLI."
    ),
    ArgumentParameter("TARGET_HOST"): ArgumentDescription(
        f"The IP address of the target node. This node must be a {NodeType.MASTER_NODE.name} and not a {NodeType.ARCHIVAL_MINER_NODE.name}."
    ),
    ArgumentParameter("TARGET_PORT"): ArgumentDescription(
        "The port to connect based on the target host address."
    ),
}
