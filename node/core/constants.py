"""
Literal Constants (constants.py) | A set of variables for references for the components that needs it.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from argparse import Namespace
from enum import Enum, IntEnum, auto
from pathlib import Path
from secrets import SystemRandom
from typing import Any, Callable, Final
from typing import NewType as _N
from typing import TypeVar, Union

from asgiref.typing import ASGIApplication
from databases import Database

# # Custom Assertable Types
AddressUUID = _N("AddressUUID", str)
ArgumentParameter = _N("ArgumentParameter", str)
ArgumentDescription = _N("ArgumentDescription", str)
AuthAcceptanceCode = _N("AuthAcceptanceCode", str)
BlockchainFileContext = _N("BlockchainFileContext", str)
CredentialContext = _N("CredentialContext", str)
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
URLAddress = _N("URLAddress", str)
UserRole = _N("UserRole", str)

# # Custom Variable Types
ArgsPlusDatabaseInstances = tuple[Namespace, Database]
BlockchainPayload = tuple[HashUUID, BlockchainFileContext]
IdentityTokens = tuple[AddressUUID, JWTToken]
RawBlockchainPayload = dict[str, Any]
RequestPayloadContext = dict[str, Any]
UserCredentials = tuple[CredentialContext, CredentialContext]


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

ADDRESS_UUID_KEY_PREFIX: Final[str] = "fl"
UUID_KEY_LENGTH: Final[int] = 35
AUTH_ENV_FILE_NAME: Final[str] = "node-env.vars"

AUTH_CODE_MIN_CONTEXT: Final[int] = 4
AUTH_CODE_MAX_CONTEXT: Final[int] = 32

# # Constants, Blockchain
BLOCKCHAIN_HASH_BLOCK_DIFFICULTY: Final[int] = 4
BLOCKCHAIN_BLOCK_TIMER_IN_SECONDS: Final[int] = 5
BLOCKCHAIN_GENESIS_MIN_CHAR_DATA: Final[int] = 16
BLOCKCHAIN_GENESIS_MAX_CHAR_DATA: Final[int] = 32
BLOCKCHAIN_MINIMUM_USER_TRANSACTIONS_TO_BLOCK: Final[int] = 2
BLOCKCHAIN_TRANSACTION_COUNT_PER_NODE: Final[int] = 2
BLOCKCHAIN_FILENAME_RANDOM_CHAR_LENGTH: Final[int] = 24
BLOCKCHAIN_NEGOTIATION_ID_LENGTH: Final[int] = 8
BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS: Final[int] = 15
BLOCKCHAIN_SECONDS_TO_MINE_FROM_ARCHIVAL_MINER: Final[int] = 2
BLOCKCHAIN_CONSENSUS_SLEEP_BASE_VALUE: Final[int] = 2
BLOCKCHAIN_TIME_TRUNCATION_ON_TX_TO_BLOCK: Final[int] = 13
REF_MASTER_BLOCKCHAIN_ADDRESS: Final[str] = "MASTER_NODE_ADDRESS"
REF_MASTER_BLOCKCHAIN_PORT: Final[str] = "MASTER_NODE_PORT"

# # Constants, Blockchain Encrypter and Decrypter Values

# - Variables for the method `BlockchainMechanism.__resolve_transaction_payload.` at Blockchain Module. | Used to encrypt and decrpyt the payload of 'GroupTransactions.context'.
TRANSACTION_PAYLOAD_MIN_CHAR_COUNT: Final[int] = 11
TRANSACTION_PAYLOAD_MAX_CHAR_COUNT: Final[int] = 12
TRANSACTION_PAYLOAD_FROM_ADDRESS_CHAR_CUTOFF_INDEX: Final[int] = 7
TRANSACTION_PAYLOAD_TIMESTAMP_FORMAT_AS_KEY: Final[str] = "%m%y%d%H%M%S"

# - Variables for the method `certify_miner` at Node API. | Used to create a unique token based from a key, which is a cipher.
CERTIFICATE_TOKEN_SECRET_KEY_START_INDEX = 16
CERTIFICATE_TOKEN_SECRET_KEY_MIDDLE_INDEX = 32
CERTIFICATE_TOKEN_SECRET_KEY_END_INDEX = 48

# - Variables for the method `BlockchainMechanism.insert_external_transaction` at Blockchain Module, focused on encrypting and decrypting a file fetched.
FILE_PAYLOAD_TIMESTAMP_FORMAT_AS_KEY: Final[str] = "%y%m%d%H%M%S"
FILE_PAYLOAD_TO_ADDRESS_START_TRUNCATION_INDEX: Final[int] = 3
FILE_PAYLOAD_TO_ADDRESS_CHAR_LIMIT_MIN: Final[int] = 13
FILE_PAYLOAD_TO_ADDRESS_CHAR_LIMIT_MAX: Final[int] = 14

# # Constants, HTTP
HTTP_MICRO_SLEEP_TO_FETCH_REQUEST: Final[float] = 0.2
HTTP_SLEEP_TO_RETRY_SECONDS: Final[int] = 3

# # Constants, Auth: JWT
JWT_DAY_EXPIRATION: Final[int] = 7
JWT_ALGORITHM: Final[str] = "HS256"

# # Constants, Auth: Time-based OTP (TOTP).
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
INF: Final[int] = 4294967295  # * Equivalent of asyncio.windows_events.INFINITE.

# # Constants, Auth: SMTP Email
DEFAULT_SMTP_URL: Final[str] = "smtp.gmail.com"
DEFAULT_SMTP_PORT: Final[int] = 465
DEFAULT_SMTP_ATTEMPT_MAX_RETRIES: Final[int] = 10
DEFAULT_SMTP_TIMEOUT_CONNECTION: Final[int] = 10
USER_FILES_FOLDER_NAME: Final[str] = "userfiles/"
USER_AVATAR_FOLDER_NAME: Final[str] = "avatars/"

# # Constants, Resources
DATABASE_NAME: Final[str] = "folioblocks-node.db"
DATABASE_RAW_PATH: str = f"{Path(__file__).cwd()}/{DATABASE_NAME}"
DATABASE_URL_PATH: str = f"sqlite:///{DATABASE_RAW_PATH}"

BLOCKCHAIN_NAME: Final[str] = "folioblocks-chain.json"
BLOCKCHAIN_RAW_PATH: str = f"{Path(__file__).cwd()}/{BLOCKCHAIN_NAME}"

# # Constraints, Portfolio
PORTFOLIO_MINUTES_TO_ALLOW_STATE_CHANGE: Final[int] = 3

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


class SourceNodeOrigin(IntEnum):
    FROM_MASTER = auto()
    FROM_ARCHIVAL_MINER = auto()


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


class NodeType(IntEnum):
    MASTER_NODE = auto()
    ARCHIVAL_MINER_NODE = auto()


# # Enums, Database


class AssociatedNodeStatus(IntEnum):
    CURRENTLY_AVAILABLE = auto()
    CURRENTLY_HASHING = auto()
    CURRENTLY_NOT_AVAILABLE = auto()


class OrganizationType(IntEnum):
    INSTITUTION = auto()
    ORGANIZATION = auto()


class ConsensusNegotiationStatus(IntEnum):
    COMPLETED = auto()
    ON_PROGRESS = auto()


class TokenStatus(IntEnum):
    EXPIRED = auto()
    CREATED_FOR_USE = auto()
    LOGGED_OUT = auto()


class TransactionContextMappingType(IntEnum):
    """This `IntEnum` is an equivalence to <class 'TransactionActions'> from the context of database data insertion. It will be used to identity the data to render from the frontend.

    Args:
        IntEnum: Uses integer `auto()` to classify choices per declaration.
    """

    APPLICANT_BASE = auto()
    APPLICANT_LOG = auto()
    APPLICANT_ADDITIONAL = auto()
    ORGANIZATION_BASE = auto()  # ! Potentially deprecated.
    ORGANIZATION_ASSOCIATIONS = auto()  # ! Potentially deprecated.
    ORGANIZATION_ADDITIONAL = auto()  # ! Potentially deprecated.


class UserActivityState(IntEnum):
    OFFLINE = auto()
    ONLINE = auto()


class UserEntity(Enum):
    MASTER_NODE_USER = "Master Node User"
    ARCHIVAL_MINER_NODE_USER = "Archival Miner Node User"
    APPLICANT_DASHBOARD_USER = "Applicant Dashboard User"
    ORGANIZATION_DASHBOARD_USER = "Organization Dashboard User"


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
    SYNC = auto()


# # SORT THIS.


class ApplicantLogContentType(IntEnum):
    WORK_EXPERIENCE = auto()
    EDUCATION = auto()
    MISCELLANEOUS = auto()


class TransactionActions(IntEnum):
    # # Note that this was the same as the <class `TransactionActionsReadable`>, but for this case, the declaration would be the same as the name.
    # @o To conform with pydantic models using another pydantic models or specially, Enum classes. I would be referring to an Enum class where it should output a technical name.
    # @o Since I cannot infer `TransactionActions` while providing `TransactionActions.name` which results to `str` it would be not elegant where all fields are relying in other objects for validation.
    # @o With that, `TransactionActionsReadable` were born. That enum alone can be used for exporting data from Explorer and Dashboard API.

    # * As I practice DRY principles, I know the disadvatange of magic numbers and then using them later on in the frontend without knowing what the heck are those numbers.
    # * Rest assured I will be resolving that issue and will map those Enums the same as how I go here.

    # - There was a debate inside my head whether I would go for string enum or integer enums, read more for recommendations:
    # - https://softwareengineering.stackexchange.com/questions/266582/is-it-better-to-use-strings-or-int-to-reference-enums-outside-the-java-part-of-t

    # - Node-based Transactions: General
    NODE_GENERAL_CONSENSUS_INIT = auto()
    NODE_GENERAL_REGISTER_INIT = auto()
    NODE_GENERAL_GENESIS_BLOCK_INIT = auto()

    # - Node-based Transaction: Consensus (Consensus)
    NODE_GENERAL_CONSENSUS_BLOCK_SYNC = auto()  # - To edit.
    NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START = auto()
    NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING = auto()

    # # Note that anything below from this context requires assistance from `models.block_context_mappings`.
    # - For Institutions / Organization.
    INSTITUTION_ORG_GENERATE_APPLICANT = auto()
    INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO = auto()
    INSTITUTION_ORG_APPLICANT_REFER_EXTRA_INFO = auto()

    # - For Organization, in general.
    ORGANIZATION_USER_REGISTER = auto()
    ORGANIZATION_REFER_EXTRA_INFO = auto()

    # # Deprecated Enum Members.
    # * The following enum members are deprecated because their feature is too much than what this system is intended to be.
    # * For the system to have a USP, the initial thought was to have an additional feature such as the applicant processing and approval for hiring purposes.
    # ! However its too far from the scope and should be deduced since this is a thesis with a limited time frame.

    # - The enums with prefixes 'APPLICANT_' is intended to implement the hiring system.
    # - The enum with prefix 'COMPANY_' is intended to implement the invitation to access the credentials of the user (the non-sensitive information).
    # APPLICANT_APPLY = auto()
    # APPLICANT_APPLY_CONFIRMED = auto()
    # APPLICANT_APPLY_REJECTED = auto()
    # COMPANY_INVITE_APPLICANTS = auto()


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
    ArgumentParameter("NODE_ROLE"): ArgumentDescription(
        f"The role of this node. Each role in {NodeType} represents different functionality. Please use the assigned role to avoid potential errors."
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
