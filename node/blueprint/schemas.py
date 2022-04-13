"""
FastAPI Pydantic Models (models.py) for the Node Backend API (api.py).

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from datetime import datetime, timedelta

from core.constants import (
    AUTH_CODE_MAX_CONTEXT,
    AUTH_CODE_MIN_CONTEXT,
    UUID_KEY_LENGTH,
    AcademicExperience,
    AddressUUID,
    # Certificates,
    CredentialContext,
    DocRequestType,
    DocumentMeta,
    # DocumentProof,
    # Documents,
    EmploymentActivityType,
    EmploymentStatus,
    GenericUUID,
    HashUUID,
    HTTPQueueMethods,
    # InternExperience,
    JWTToken,
    KeyContext,
    NodeType,
    NotificationContext,
    RequestContext,
    RequestPayloadContext,
    RoleContext,
    StudentActivities,
    StudentStatus,
    TokenStatus,
    TransactionActions,
    TransactionContentCategory,
    TransactionContentOperation,
    TransactionContentType,
    TransactionStatus,
    URLAddress,
    UserActivityState,
    UserEntity,
    UserRole,
    # WorkExperience,
)
from pydantic import BaseModel, EmailStr, Field

# # Dashboard API — START


class DashboardContext(BaseModel):
    address: AddressUUID
    role: UserRole
    notifications: NotificationContext
    role_context: RoleContext


class Students(BaseModel):
    first_name: str
    last_name: str
    address_equiv: AddressUUID
    program: str
    semester: str
    date_created: datetime


class Student(BaseModel):  # This may or may not be possible.
    first_name: str
    last_name: str
    address_equiv: AddressUUID
    program: str
    semester: str
    # applicant_data: Applicant  # Nested since students will become applicants later on.
    date_created: datetime


class NewStudentOut(BaseModel):
    student_address: AddressUUID
    date_created: datetime


"""
# Generate Auth Token Models
- The following is just a model that represents the query inputs for the endpoint 'admin/generate_auth'.
"""


class GenerateAuthInput(BaseModel):
    email: EmailStr
    role_to_infer: UserEntity


"""
# Block Structure Models
- The following pydantic models are made out of the `Block`. Note that the fields for the `Block` and the `Blockchain` is here as well.
@o Notice that the the declaration of the classes were done in descending form to the actual declaration of the `Block`.
@o There are some fields were declared as `None` as they are defined during or after a certain processes.
"""


class TransactionStudentActivities(BaseModel):
    type: StudentActivities
    name: str
    description: str | None
    duration_start: datetime
    duration_end: datetime
    document_rep: HashUUID | None
    validated_by: AddressUUID


class TransactionStudentOtherInfo(BaseModel):
    title: str
    description: str | None
    inserted_by: AddressUUID


class TransactionStudentPayload(BaseModel):
    identity: AddressUUID
    name: str
    course: str
    course_level: int
    status: StudentStatus
    activities: list[TransactionStudentActivities] | None
    other_info: list[TransactionStudentOtherInfo] | None


class TransactionEmployeeActivites(BaseModel):
    type: EmploymentActivityType
    name: str
    deescription: str | None
    duration_start: datetime
    duration_end: datetime | None
    document_rep: HashUUID | None
    role: str
    validated_by: AddressUUID


class TransactionEmployeePayload(BaseModel):
    identity: AddressUUID
    company: AddressUUID
    role: str
    status: EmploymentStatus
    activities: list[TransactionEmployeeActivites] | None


class TransactionContent(BaseModel):
    category: TransactionContentCategory
    type: TransactionContentType
    operation: TransactionContentOperation
    payload: TransactionEmployeePayload | TransactionStudentPayload


class Transaction(
    BaseModel
):  # TODO | We need TransactionDetail if we were able to fetch it.
    tx_hash: AddressUUID
    action: TransactionActions
    status: TransactionStatus
    content: TransactionContent
    from_address: AddressUUID
    to_address: AddressUUID
    prev_hash: HashUUID | None
    timestamp: datetime


class HashableBlock(BaseModel):
    nonce: int | None
    validator: AddressUUID
    transactions: list[Transaction] | None
    timestamp: datetime


class BaseBlock(BaseModel):
    id: int
    block_size: int | None


class Block(BaseBlock):
    contents: HashableBlock
    hash_block: HashUUID | None
    prev_hash_block: HashUUID


class BlockOverview(BaseBlock):
    validator: AddressUUID


# # Block Structure — END

# # APIs


class NodeConsensusInformation(BaseModel):
    owner: AddressUUID  # * Same as validator.
    is_sleeping: bool
    is_mining: bool
    node_role: NodeType
    consensus_timer_seconds: float
    last_mined_block: int


class NodeMasterInformation(
    BaseModel
):  # TODO: We may remove transactions and addresses.
    block_timer: int
    total_blocks: int
    total_transactions: int


class NodeInformation(BaseModel):
    properties: NodeConsensusInformation
    statistics: NodeMasterInformation | None


class Blockchain(BaseModel):
    block: list[BlockOverview] | None
    transactions: list[Transaction] | None
    node_info: NodeMasterInformation


# # Explorer API — END

# # Entity API — START


class EntityRegisterCredentials(BaseModel):
    username: CredentialContext | str = Field(
        ..., description="Unique-readable indicator of the entity.", max_length=24
    )
    password: CredentialContext | str = Field(
        ..., description="Text-entry for authorizing the entity.", max_length=64
    )
    email: EmailStr = Field(
        ..., description="The email address to contact for notifications."
    )
    first_name: str = Field(
        None, description="The initial name of the entity", max_length=32
    )
    last_name: str = Field(
        None,
        description="The last name of the entity, completing their identity.",
        max_length=32,
    )

    auth_code: str | bytes = Field(  # typevar: KeyContext
        description="The authentication code that is used to authorize the registration.",
        min_length=AUTH_CODE_MIN_CONTEXT,
        max_length=AUTH_CODE_MAX_CONTEXT * 2,
    )


class EntityRegisterResult(BaseModel):
    user_address: AddressUUID | str = Field(
        ...,
        description="The unique identifier of the entity. This was generated when the entity has been acknowledged for registration, and was return for reference.",
        max_length=UUID_KEY_LENGTH,
    )
    username: CredentialContext | str = Field(
        ...,
        description="Your chosen identity to register from the blockchain network.",
        max_length=24,
    )
    date_registered: datetime = Field(
        ...,
        description="The date and time from where this entity has been introduced from the system.",
    )
    role: UserEntity = Field(
        ..., description="The role of this entity from the system."
    )


class EntityLoginResult(BaseModel):
    user_address: AddressUUID | str = Field(
        ...,
        description="The unique identifier of the user in the blockchain space. This can be used to reference yourself for every transaction done in the network.",
        max_length=UUID_KEY_LENGTH,
    )
    user_role: UserEntity = Field(
        ...,
        description="The role of the node, which is technically returned to the client for further validation.",
    )
    jwt_token: JWTToken = Field(
        ...,
        description="The JWT token for authenticating your session in the blockchain network. Invoke this in the header to authorize yourself.",
    )
    expiration: datetime | None = Field(
        ...,
        description="The date and time from where this token will expire. When expired, you need to fetch by re-login.",
    )


class EntityLoginCredentials(BaseModel):
    username: CredentialContext | str = Field(
        ...,
        description="The username of the entity. This will be used primarily for identifying yourself, aside from the unique address given when registered.",
        max_length=24,
    )
    password: CredentialContext | str = Field(
        ...,
        description="The unhashed password of your account. This will be checked compared to your hashed version of your password to authenticate you.",
        max_length=64,
    )


class Tokens(BaseModel):
    id: int = Field(..., description="Reference ID for the token generated.")
    from_user: AddressUUID | str = Field(
        ...,
        description="The reference to the unique ID of the user who generated this token.",
        max_length=UUID_KEY_LENGTH,
    )
    token: JWTToken = Field(..., description="The token generated from this row.")
    state: TokenStatus = Field(..., description="The current status of this token.")
    expiration: datetime | None = Field(
        ...,
        description="The date and time from where this token will expire.",
    )
    issued: datetime = Field(
        ...,
        description="The date and time from where this token was generated.",
    )


class Users(BaseModel):
    unique_address: AddressUUID | str = Field(
        ...,
        description="The unique address of the user in the blockchain network.",
        max_length=UUID_KEY_LENGTH,
    )
    first_name: str | None = Field(
        None, description="The initial name of the entity", max_length=32
    )
    last_name: str | None = Field(
        None,
        description="The last name of the entity, completing their identity.",
        max_length=32,
    )
    username: CredentialContext | str = Field(
        ..., description="Unique-readable indicator of the entity.", max_length=24
    )
    password: CredentialContext | str | None = Field(
        ..., description="Text-entry for authorizing the entity.", max_length=64
    )
    email: EmailStr | None = Field(
        ..., description="The email address to contact for notifications."
    )
    type: UserEntity = Field(
        ..., description="A classifier that represents the entity of this data."
    )
    activity: UserActivityState = Field(
        ..., description="Describes the current state of this entity."
    )
    date_registered: datetime = Field(
        ...,
        description="The date and time from where this entity has been registed from the system.",
    )


# # Entity API — END


# # HTTP Methods — START
# * Note that this class is not used in the API system! Meaning they are used internally.
class HTTPRequestPayload(BaseModel):
    url: str = Field(
        ...,
        description="The URL to send a request at, and from where it will receive a response.",
    )
    data: RequestPayloadContext | None = Field(
        ..., description="The context or the payload to send at the url."
    )
    headers: RequestPayloadContext | None = Field(
        ...,
        description="It contains properties that may modify the output of the response or just an identifier for the request.",
    )
    method: HTTPQueueMethods = Field(
        ...,
        description="The method from which classifies the request from fetcting a data to sending a data and etc.",
    )
    await_result_immediate: bool = Field(
        ...,
        description="An identifier that tells if this request requires an immediate response from the origin.",
    )
    name: str | None = Field(
        ...,
        description="The name of this HTTP request, required whenever `await_result_immediate` is set to `True`.",
    )


class SourcePayload(BaseModel):
    source_address: str
    source_port: int


# # HTTP Methods — END
