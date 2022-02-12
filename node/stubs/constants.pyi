from enum import Enum, IntEnum
from typing import Any, Final

class DocToRequestTypes(IntEnum):
    TOR: int
    SPECIFIED: int
NotificationContext = list[dict[str, Any]]
RoleContext = dict[str, Any]
DocumentSet = list[dict[str, Any]]
AcademicExperience: Any
AddressUUID: Any
ArgumentParameter: Any
ArgumentDescription: Any
BlockID: Any
Certificates: Any
CredentialContext: Any
DocRequestType: Any
Documents: Any
DocumentMeta: Any
DocumentProof: Any
GenericUUID: Any
HashUUID: Any
InternExperience: Any
NodeRole: Any
JWTToken: Any
ProgramMetadata: Any
RegExp: Any
RequestContext: Any
URLAddress: Any
UserRole: Any
TxID: Any
WorkExperience: Any
ENUM_NAME_PATTERN: str
DATABASE_NAME: Final[str]
DATABASE_URL_PATH: str
NODE_LIMIT_NETWORK: Final[int]
NODE_IP_URL_TARGET: Final[str]
NODE_IP_PORT_FLOOR: int

class BaseAPI(Enum):
    DASHBOARD: str
    EXPLORER: str
    NODE: str

class DashboardAPI(Enum):
    DASHBOARD_GENERAL_API: str
    APPLICANT_API: str
    EMPLOYER_API: str
    INSTITUTION_API: str

class ExplorerAPI(Enum):
    GENERAL_FETCH: str
    LIST_FETCH: str
    SPECIFIC_FETCH: str
    BLOCK_FETCH: str
    TRANSACTION_FETCH: str
    ADDRESS_FETCH: str

class NodeAPI(Enum):
    GENERAL_NODE_API: str
    MASTER_NODE_API: str
    SIDE_NODE_API: str
    NODE_TO_NODE_API: str

class TransactionStatus(IntEnum):
    PENDING: int
    SUCCESS: int
    FAILED: int

class TransactionActions(IntEnum):
    ACCOUNT_GENERATED: int
    DATA_UPDATED: int
    DATA_DISREGARDED: int
    DATA_BATCH_MINTING: int
    DOCUMENT_INSUANCE: int
    REQUEST_INITIATION: int
    REQUEST_PROCESSING: int
    REQUEST_MARKED_ENDED: int
    REQUEST_SPECIFIC_DOC: int

class TransactionActionString(Enum): ...

class ItemReturnCount(IntEnum):
    LOW: Final[int]
    MIN: Final[int]
    MID: Final[int]
    HIGH: Final[int]
    MAX: Final[int]

class LoggerLevelCoverage(Enum):
    DEBUG: Final[str]
    INFO: Final[str]
    WARNING: Final[str]
    ERROR: Final[str]
    CRITICAL: Final[str]
    TRACE: Final[str]

class NodeRoles(IntEnum):
    MASTER: int
    SIDE: int

class Activity(Enum):
    OFFLINE: str
    ONLINE: str

class BlacklistDuration(Enum):
    INDEFINITE: str
    WARN_1: str
    WARN_2: str
    WARN_3: str
    FINAL_WARNING: str

class TokenType(IntEnum):
    EXPIRED: int
    RECENTLY_CREATED: int
    ON_USE: int
    TOKEN_RETAINED_WHILE_EXPIRED: int

class UserType(Enum):
    AS_NODE: str
    AS_USER: str

FOLIOBLOCKS_NODE_TITLE: Final[ProgramMetadata]
FOLIOBLOCKS_NODE_DESCRIPTION: Final[ProgramMetadata]
FOLIOBLOCKS_EPILOG: Final[ProgramMetadata]
FOLIOBLOCKS_HELP: Final[dict[ArgumentParameter, ArgumentDescription]]
