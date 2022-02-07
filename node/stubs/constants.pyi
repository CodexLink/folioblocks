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
NodeRoles: Any
JWTToken: Any
ProgramMetadata: Any
RequestContext: Any
URLAddress: Any
UserRole: Any
TxID: Any
WorkExperience: Any
NODE_LIMIT_NETWORK: Final[int]
NODE_IP_URL_TARGET: Final[str]
NODE_IP_PORT_FLOOR: int
NODE_ROLE_CHOICES: Final[list[NodeRoles]]

class BaseAPI(Enum):
    DASHBOARD: str
    EXPLORER: str
    NODE: str

class DashboardAPI(Enum):
    DASHBOARD_GENERAL_API: str
    CLIENT_ONLY_API: str
    APPLICANT_ONLY_API: str
    EMPLOYER_ONLY_API: str
    INSTITUTION_ONLY_API: str

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

FOLIOBLOCKS_NODE_TITLE: Final[ProgramMetadata]
FOLIOBLOCKS_NODE_DESCRIPTION: Final[ProgramMetadata]
FOLIOBLOCKS_EPILOG: Final[ProgramMetadata]
FOLIOBLOCKS_HELP: Final[dict[ArgumentParameter, ArgumentDescription]]
