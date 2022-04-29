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
    AddressUUID,
    ApplicantLogContentType,
    CredentialContext,
    HashUUID,
    HTTPQueueMethods,
    JWTToken,
    NodeTransactionInternalActions,
    NodeType,
    OrganizationType,
    RandomUUID,
    RequestPayloadContext,
    TokenStatus,
    TransactionActions,
    TransactionContextMappingType,
    URLAddress,
    UserActivityState,
    UserEntity,
    UserRole,
)
from fastapi import UploadFile
from pydantic import BaseModel, EmailStr, Field

# # Agnostic Models — END


class AdditionalContextTransaction(BaseModel):
    address_origin: AddressUUID
    title: str
    description: str
    inserter: AddressUUID | None
    timestamp: datetime | None


class ApplicantLogTransaction(BaseModel):
    address_origin: AddressUUID
    type: ApplicantLogContentType
    name: str
    description: str
    role: str
    file: UploadFile | HashUUID | None
    duration_start: datetime
    duration_end: datetime | None
    validated_by: AddressUUID | None  # * We will be using `AddressUUID` for the output. Meanwhile, we will left the right-operand as None since we are dependent to the user who does that by getting the session token.
    timestamp: datetime | None  # * We will be using `datetime` for output, while we don't take any inputs from the frontend in terms of the timestamp, it can be easily modified, so therefore let the backend calculate the time.


# # Agnostic Models — END

# # Dashboard API — START


class ApplicantEditableProperties(BaseModel):
    avatar: UploadFile | None
    description: str | None
    personal_skills: str | None


class DashboardApplicant(BaseModel):
    tx_associated_count: int
    last_update: datetime


class DashboardArchival(BaseModel):
    negotiation_count: int
    last_block_hashed: int


class DashboardOrganization(BaseModel):
    total_students: int
    total_associated_logs: int
    total_associated_extra: int


class DashboardContext(BaseModel):
    address: AddressUUID
    first_name: str | None
    last_name: str | None
    username: str
    role: UserRole
    reports: DashboardApplicant | DashboardArchival | DashboardOrganization | None


class PortfolioSettings(BaseModel):
    enable_sharing: bool
    expose_email_info: bool
    show_files: bool


class PortfolioLogMinimal(BaseModel):
    at_block: int
    log_type: TransactionContextMappingType
    origin_address: AddressUUID
    tx_hash: HashUUID


class Portfolio(ApplicantEditableProperties, BaseModel):
    address: AddressUUID
    email: EmailStr | None
    program: str
    prefer_role: str
    association: AddressUUID
    logs: list[ApplicantLogTransaction] | None
    extra: list[AdditionalContextTransaction] | None


# class PortfolioDetailed(PortfolioBase):
#     pass


class Student(BaseModel):
    first_name: str
    last_name: str
    address: AddressUUID
    program: str
    date_created: datetime


"""
# Generate Auth Token Models
- The following is just a model that represents the query inputs for the endpoint 'admin/generate_auth'.
"""


class GenerateAuthInput(BaseModel):
    email: EmailStr
    role: UserEntity


"""
# Block Node Structure Models
- The following pydantic models are made from the `Transaction` of the `Block`.
@o Notice that the the declaration of the classes were done in descending form to the actual declaration of the `Block`.
@o There are some fields were declared as `None` as they are defined during or after a certain processes.
"""

# @o This is used for both fields under `extra` of Applicant and Organization.

# # Generalized Validator — START


class AgnosticCredentialValidator(BaseModel):
    # @d This model was created for the validation for `insert_external_transaction` method.
    first_name: str
    last_name: str
    email: EmailStr
    username: str


class OrganizationIdentityValidator(BaseModel):
    association_address: str | None
    association_name: str | None
    association_group_type: OrganizationType | None


# # Generalized Validator — END

# # Organization-based Transactions — START


class AgnosticTransactionUserCredentials(AgnosticCredentialValidator, BaseModel):
    password: str


class AgnosticViewExtenderFields(BaseModel):
    extra: AdditionalContextTransaction | None


class ApplicantUserBaseTransaction(BaseModel):
    avatar: UploadFile | None  # - Changeable but will be recorded as a proof.
    identity: AddressUUID | None  # * This is going to be resolved during process.
    inserter: AddressUUID | None  # * Reference to user from the organization.
    institution: AddressUUID | None
    description: str | None  # - Changeable, but will be recorded as a proof.
    skills: str | None  # - Changeable, but will be recorded as a proof.
    program: str
    preferred_role: str


class ApplicantUserTransaction(
    AgnosticTransactionUserCredentials, ApplicantUserBaseTransaction
):
    pass


# - REST API Model.
class ApplicantUserViewExtender(AgnosticViewExtenderFields, BaseModel):
    applicants: ApplicantUserBaseTransaction
    logs: list[ApplicantLogTransaction] | None


# * This organization (generative) model contains fields that seem to be nullable or optional, which does not. Some fields may be nullable at the case were an association was registered in the first place, or was referred from this organization.
# - The important matter here is that, a identity and a institution will be referred, to which at this case, when fetched will be rendered from this model later.


class OrganizationUserBaseFields(BaseModel):
    identity: str | None  # * Will be resolved during creation process.
    institution: str | None


class OrganizationUserBaseTransaction(OrganizationUserBaseFields, BaseModel):
    org_type: OrganizationType | None
    founded: datetime | None
    description: str | None  # - May be changeable.


class OrganizationUserTransaction(
    AgnosticTransactionUserCredentials,
    OrganizationIdentityValidator,
    OrganizationUserBaseTransaction,
):
    pass


# - Another Rest API model.
class OrganizationUserViewExtender(AgnosticViewExtenderFields, BaseModel):
    organizations: OrganizationUserBaseTransaction
    associations: list[AddressUUID] | None


# # Organization-based Transactions — END


class NodeRegisterTransaction(BaseModel):
    new_address: AddressUUID
    acceptor_address: AddressUUID
    role: UserEntity
    timestamp: datetime


class NodeGenesisTransaction(BaseModel):
    block_genesis_no: int
    generator_address: AddressUUID
    data: HashUUID
    time_initiated: datetime


class NodeCertificateTransaction(BaseModel):
    requestor_address: AddressUUID
    timestamp: datetime


class NodeSyncTransaction(BaseModel):
    requestor_address: AddressUUID
    timestamp: datetime


class NodeConfirmMineConsensusTransaction(BaseModel):
    consensus_negotiation_id: RandomUUID
    miner_address: AddressUUID
    master_address: AddressUUID


class NodeMineConsensusSuccessProofTransaction(BaseModel):
    miner_address: AddressUUID
    receiver_address: AddressUUID
    consensus_negotiation_id: RandomUUID
    block_received_id: int
    local_block_id: int
    block_hash: HashUUID | None
    time_delivery: datetime


class GroupTransaction(BaseModel):
    content_type: TransactionContextMappingType
    context: ApplicantLogTransaction | ApplicantUserBaseTransaction | AdditionalContextTransaction | HashUUID | OrganizationUserBaseFields | OrganizationUserBaseTransaction


class NodeTransaction(BaseModel):
    action: NodeTransactionInternalActions
    context: HashUUID | NodeCertificateTransaction | NodeConfirmMineConsensusTransaction | NodeGenesisTransaction | NodeMineConsensusSuccessProofTransaction | NodeRegisterTransaction | NodeSyncTransaction


class TransactionSignatures(BaseModel):
    raw: HashUUID
    encrypted: HashUUID


class TransactionOverview(BaseModel):
    tx_hash: HashUUID | None
    action: TransactionActions
    from_address: AddressUUID
    to_address: AddressUUID | None


class Transaction(TransactionOverview, BaseModel):
    payload: GroupTransaction | NodeTransaction
    signatures: TransactionSignatures


class HashableBlock(BaseModel):
    nonce: int | None
    validator: AddressUUID
    timestamp: datetime
    transactions: list[Transaction]


class BaseBlock(BaseModel):
    id: int
    content_bytes_size: int | None


class Block(BaseBlock):
    hash_block: HashUUID | None
    prev_hash_block: HashUUID
    contents: HashableBlock


# # Block Structure — END

# # APIs


class ArchivalMinerNodeInformation(BaseModel):
    candidate_no: int
    miner_address: AddressUUID
    source_host: URLAddress
    source_port: int


class ConsensusSuccessPayload(BaseModel):
    reiterate_master_address: AddressUUID
    addon_consensus_sleep_seconds: float


class ConsensusFromMasterPayload(BaseModel):
    consensus_negotiation_id: str
    master_address: AddressUUID
    block: Block


class ConsensusToMasterPayload(BaseModel):
    consensus_negotiation_id: RandomUUID
    miner_address: AddressUUID
    hashed_block: Block
    local_block_id: int
    hashing_duration_finished: datetime


class NodeConsensusInformation(BaseModel):
    owner: AddressUUID  # * Same as validator.
    is_sleeping: bool
    is_hashing: bool
    node_role: NodeType
    current_consensus_sleep_timer: timedelta
    last_mined_block: int


class NodeMasterInformation(BaseModel):
    chain_block_timer: int
    total_blocks: int
    total_transactions: int
    total_addresses: int
    total_tx_mappings: int


class NodeInformation(BaseModel):
    properties: NodeConsensusInformation
    statistics: NodeMasterInformation | None


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
    auth_code: str = Field(
        description="The authentication code that is used to authorize the registration.",
        min_length=AUTH_CODE_MIN_CONTEXT,
        max_length=AUTH_CODE_MAX_CONTEXT * 2,
    )

    association_name: str | None = Field(
        None,
        description="The name of the association. Specify this if the association doens't exist.",
    )
    association_address: str | None = Field(
        None,
        description="The address of the assocation. Specify if that association does exist.",
    )
    association_type: OrganizationType | None = Field(
        None,
        description="The type of the association, technically the type of the organization.",
    )  # ! In frontend, ensure this was a dropdown.

    association_founded: datetime | None = Field(
        None, description="The time from where this oganization has been founded."
    )
    association_description: str | None = Field(
        None, description="The description of your organization."
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

# # Explorer API (Seperatable) — START
class BlockOverview(BaseBlock):
    validator: AddressUUID
    timestamp: datetime


class Blockchain(BaseModel):
    block: list[BlockOverview] | None
    transactions: list[TransactionOverview] | None
    node_info: NodeMasterInformation | None


class EntityAddress(BaseModel):
    uuid: AddressUUID
    association_uuid: AddressUUID | None
    entity_type: UserEntity
    tx_bindings_count: int
    negotiations_count: int


class EntityAddressDetail(EntityAddress, BaseModel):
    description: str | None
    related_txs: list[TransactionOverview]


class TransactionDetail(BaseModel):
    from_block: int
    transaction: Transaction


# # Explorer API (Seperatable) — END

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


# # Uncategorized
class SourcePayload(BaseModel):
    source_address: str
    source_port: int


# # HTTP Methods — END
