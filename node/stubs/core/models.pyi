from datetime import datetime
from pydantic import BaseModel, EmailStr as EmailStr, FilePath as FilePath
from typing import Any, List
from utils.constants import AcademicExperience as AcademicExperience, AddressUUID as AddressUUID, Certificates as Certificates, CredentialContext as CredentialContext, DocRequestType as DocRequestType, DocumentMeta as DocumentMeta, DocumentProof as DocumentProof, Documents as Documents, GenericUUID as GenericUUID, HashUUID as HashUUID, InternExperience as InternExperience, JWTToken as JWTToken, NotificationContext as NotificationContext, RequestContext as RequestContext, RoleContext as RoleContext, TransactionActions as TransactionActions, TransactionStatus as TransactionStatus, UserRole as UserRole, WorkExperience as WorkExperience

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

class Applicant(BaseModel):
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
    request: DocRequestType

class RequestInput(BaseModel):
    ref_id: int
    title: RequestContext
    message: RequestContext
    doc_type: Union[str, None]

class Issuances(BaseModel):
    id: int
    from_address: AddressUUID
    to_address: AddressUUID
    title: str
    summary: str
    date_issued: datetime

class IssueToStudentIn(BaseModel):
    to_student_addr: AddressUUID
    doc_type: Union[str, FilePath]
    description: str
    institution_reference: AddressUUID

class IssueToStudentOut(BaseModel):
    hash_ref: GenericUUID
    date_created: datetime

class Issuance(BaseModel):
    title: DocumentMeta
    description: str
    context: Union[str, FilePath]

class Students(BaseModel):
    first_name: str
    last_name: str
    address_equiv: AddressUUID
    program: str
    semester: str
    date_created: datetime

class Student(BaseModel):
    first_name: str
    last_name: str
    address_equiv: AddressUUID
    program: str
    semester: str
    applicant_data: Applicant
    date_created: datetime

class NewStudentIn(BaseModel):
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
    telephone_no: Union[str, int]
    cell_no: Union[str, int]
    school_name: str
    school_branch: str
    year_started: int
    year_ended: int

class NewStudentOut(BaseModel):
    student_address: AddressUUID
    date_created: datetime

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
    context: Any
    status: TransactionStatus
    stored_at_block: int

class Block(BaseModel):
    id: int
    nonce: int
    validator: AddressUUID
    prer_block: HashUUID
    next_block: Union[HashUUID, None]
    transactions: List[Transaction]
    block_size: int
    timestamp: datetime

class Blockchain(BaseModel):
    block: List[Block]
    transactions: List[Transaction]
    status_reports: Any

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

class SearchContext(BaseModel):
    context: str

class NodeRegisterCredentials(BaseModel):
    username: CredentialContext
    password: CredentialContext
    user_address: AddressUUID

class NodeLoginContext(BaseModel):
    jwt_token: JWTToken
    expiration: datetime
    time_elapsed: datetime

class NodeLoginCredentials(BaseModel):
    user_address: AddressUUID
    password: CredentialContext
    auth_code: str

class NodeInfoConfig(BaseModel): ...
class NodeInfoOthers(BaseModel): ...
class NodeInfoContext(BaseModel): ...
class NodeNegotiationInit(BaseModel): ...
class NodeNegotiationEnd(BaseModel): ...

class NodeNegotiation(BaseModel):
    negotiation: Union[NodeNegotiationInit, NodeNegotiationEnd]

class NodeNegotiationProcess(BaseModel): ...
