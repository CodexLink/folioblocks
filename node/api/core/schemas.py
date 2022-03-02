"""
FastAPI Pydantic Models (models.py) for the Node Backend API (api.py).

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from datetime import datetime
from typing import Any, List

from pydantic import BaseModel, EmailStr, Field, FilePath
from utils.constants import (
    AcademicExperience,
    AddressUUID,
    Certificates,
    CredentialContext,
    DocRequestType,
    DocumentMeta,
    DocumentProof,
    Documents,
    GenericUUID,
    HashUUID,
    InternExperience,
    JWTToken,
    KeyContext,
    NotificationContext,
    RequestContext,
    RoleContext,
    TransactionActions,
    TransactionStatus,
    UserEntity,
    UserRole,
    WorkExperience,
)

# ! Note that we can use one the exclude or include functionality upon returning the context of these models.

# # Dashboard API — START


class DashboardContext(BaseModel):
    address: AddressUUID
    role: UserRole
    notifications: NotificationContext
    role_context: RoleContext


class UserLoginResult(BaseModel):
    address: AddressUUID
    hash_session: JWTToken
    role: UserRole


class UserLoginIn(BaseModel):
    username: CredentialContext
    password: CredentialContext


class UserLogoutIn(BaseModel):
    hash_session: JWTToken


class Applicants(BaseModel):
    id: int
    address: AddressUUID
    job_target: str
    date_applied: datetime


class Applicant(BaseModel):  # ! This is unconfirmed!
    address: AddressUUID
    academic: AcademicExperience
    certificates: Certificates
    intern_experience: InternExperience
    other_documents: Documents
    proof_documents: DocumentProof
    work_experience: WorkExperience


class Requests(BaseModel):
    id: int
    from_address: AddressUUID
    summary: str


class Request(BaseModel):
    id: int
    from_address: AddressUUID
    description: str
    request: DocRequestType  # This is indicated under Enums. Also this indicates ACCESS, not document.


class RequestInput(BaseModel):
    ref_id: int
    title: RequestContext
    message: RequestContext
    doc_type: str | None = None  # I still cannot envision this part.


class Issuances(BaseModel):
    id: int
    from_address: AddressUUID
    to_address: AddressUUID
    title: str
    summary: str
    date_issued: datetime


class IssueToStudentIn(BaseModel):
    to_student_addr: AddressUUID
    doc_type: str | FilePath  # External document or
    description: str
    institution_reference: AddressUUID


class IssueToStudentOut(BaseModel):
    hash_ref: GenericUUID
    date_created: datetime


class Issuance(BaseModel):
    title: DocumentMeta
    description: str
    context: str | FilePath  # Unconfirmed.


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
    applicant_data: Applicant  # Nested since students will become applicants later on.
    date_created: datetime


class NewStudentIn(BaseModel):  # TODO: We need to typed this one soon.
    first_name: str
    last_name: str
    age: int
    sex: str
    year: int
    semester: str
    program: str
    telephone: int
    city_address: str
    city_zip_code: int
    email: EmailStr
    telephone_no: str | int
    cell_no: str | int
    school_name: str
    school_branch: str
    year_started: int
    year_ended: int


class NewStudentOut(BaseModel):
    student_address: AddressUUID
    date_created: datetime


# # Dashboard API — END

# # Explorer API — START


class Transactions(BaseModel):
    tx_hash: AddressUUID
    action: TransactionActions
    status: TransactionStatus
    stored_at_block: int
    date_executed: datetime


class Transaction(BaseModel):
    tx_hash: AddressUUID
    action: TransactionActions
    date_executed: datetime
    from_address: AddressUUID
    to_address: AddressUUID
    context: Any  # TODO: We have to type this one as well. Or create an Enum that classifies those actions.
    status: TransactionStatus
    stored_at_block: int


class Block(BaseModel):
    id: int
    nonce: int
    validator: AddressUUID  # ! TODO: We need the database before being able to implement self-reference from producing the genesis block.
    prer_block: HashUUID
    next_block: HashUUID | None
    transactions: List[Transaction]
    block_size: int
    timestamp: datetime


# This was dissected.
class Blockchain(BaseModel):
    block: List[Block]
    transactions: List[Transaction]
    status_reports: Any  # TODO: We have to return more than this, to provide insights about the current master node.


class Blocks(BaseModel):
    id: int
    date_created: datetime
    transaction_count: int
    validator: AddressUUID


class Addresses(BaseModel):
    id: int
    address: AddressUUID
    date_created: datetime


class Address(BaseModel):
    id: int
    address: AddressUUID
    transactions: List[Transaction]
    role: str


class SearchContext(
    BaseModel
):  # ! Idk, is there something else? Maybe we will expand this when we have the web.
    context: str


# # Explorer API — END

# # Node API — START

# Model for the Block Details
class NodeRegisterCredentials(BaseModel):
    username: CredentialContext = Field(
        ..., description="Unique-readable indicator of the entity."
    )
    password: CredentialContext = Field(
        ..., description="Text-entry for authorizing the entity."
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

    auth_code: KeyContext | None


class NodeRegisterResult(BaseModel):
    user_address: AddressUUID = Field(
        ...,
        description="The unique identifier of the entity. This was generated when the entity has been acknowledged for registration.",
    )
    date_registered: datetime = Field(
        ...,
        description="The date and time from where this entity has been introduced from the system.",
    )
    role: UserEntity = Field(
        ..., description="The role of this entity from the system."
    )


class NodeLoginContext(BaseModel):
    jwt_token: JWTToken
    expiration: datetime
    time_elapsed: datetime  # This indicates the time before you can participate in the blockchain network, as per consensus condition.


class NodeLoginCredentials(BaseModel):
    user_address: AddressUUID
    password: CredentialContext
    auth_code: str  # TODO: This functionality is not official. As this may be the same as the Google Authenticator or any other time based authorization.


# # AT THIS POINT, I CANNOT ADD THE FIELDS SINCE I STILL HAVE NO IDEA ON HOW TO IMPLEMENT THEM.
# * There are other fields were I don't know if they are helpful or not.

# Other NodeInfoXXX have to be expand later.
class NodeInfoConfig(BaseModel):
    pass


class NodeInfoOthers(BaseModel):
    pass


class NodeInfoContext(BaseModel):  # This is the main context for the /info.
    pass


# As well as this one.
class NodeNegotiationInit(BaseModel):
    pass


class NodeNegotiationEnd(BaseModel):
    pass


class NodeNegotiation(BaseModel):
    negotiation: NodeNegotiationInit | NodeNegotiationEnd


# During process, we also have to invoke other information as well.
class NodeNegotiationProcess(BaseModel):
    pass


# # Node API — START
