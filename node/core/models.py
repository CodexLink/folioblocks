"""
FastAPI Models for the API (api.py).

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from pydantic import BaseModel, EmailStr, FilePath
from datetime import datetime

from node.utils.constants import (
    AcademicExperience,
    AddressUUID,
    Certificates,
    CredentialContext,
    DocRequestType,
    DocumentMeta,
    DocumentProof,
    Documents,
    GenericUUID,
    InternExperience,
    JWTToken,
    NotificationContext,
    RequestContext,
    RoleContext,
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


class Blockchain(BaseModel):
    pass


class Blocks(BaseModel):
    pass


class Block(BaseModel):
    pass


class Transactions(BaseModel):
    pass


class Transaction(BaseModel):
    pass


class Addresses(BaseModel):
    pass


class Address(BaseModel):
    pass


class SearchContext(BaseModel):
    pass


# # Explorer API — END

# # Node API — START

# Model for the Block Details
class NodeRegisterCredentials(BaseModel):
    pass


class NodeLoginContext(BaseModel):
    pass


class NodeLoginCredentials(BaseModel):
    pass


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


class NodeNegoitiationEnd(BaseModel):
    pass

# During process, we also have to invoke other information as well.
class NodeNegotiationProcess(BaseModel):
    pass


# # Node API — START
