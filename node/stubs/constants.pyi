from enum import IntEnum
from typing import Any, Final

AddressUUID: Any
ArgumentParameter: Any
ArgumentDescription: Any
BlockID: Any
NodeRoles: Any
URLAddress: Any
ProgramMetadata: Any
TxID: Any
NODE_LIMIT_NETWORK: Final[int]
NODE_IP_URL_TARGET: Final[str]
NODE_IP_PORT_FLOOR: int
NODE_ROLE_CHOICES: Final[list[NodeRoles]]

class DashboardAPITags(IntEnum):
    GENERAL_API: int
    CLIENT_ONLY_API: int
    APPLICANT_ONLY_API: int
    EMPLOYER_ONLY_API: int
    INSTITUTION_ONLY_API: int

class ExplorerAPITags(IntEnum):
    GENERAL_FETCH: int
    LIST_FETCH: int
    SPECIFIC_FETCH: int
    BLOCK_FETCH: int
    TRANSACTION_FETCH: int
    ADDRESS_FETCH: int

class NodeAPITags(IntEnum):
    GENERAL_NODE_API: int
    MASTER_NODE_API: int
    SIDE_NODE_API: int
    NODE_TO_NODE_API: int

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
