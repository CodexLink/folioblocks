"""
Node Component, Dashboard API
This section contains API endpoints for the dashboard. Dashboard API is only available on Node API with a role of Master Node. As a developer, I do understand the consequences of a node running 3 set of APIs, but to cut costs, I need to deploy it this way. In ideal world, this is not acceptable.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from http import HTTPStatus
from fastapi import Query, APIRouter
from typing import List
from api.core.schemas import (
    Applicant,
    Applicants,
    DashboardContext,
    Issuance,
    Issuances,
    IssueToStudentIn,
    IssueToStudentOut,
    NewStudentIn,
    NewStudentOut,
    Request,
    Requests,
    Student,
    Students,
    # UserLoginIn,
    # UserLoginResult,
    UserLogoutIn,
)
from utils.constants import BaseAPI
from utils.constants import AddressUUID, DashboardAPI, ItemReturnCount

dashboard_router = APIRouter(
    prefix="/dashboard",
    tags=[BaseAPI.DASHBOARD.value],
    responses={404: {"description": "Not Found."}},  # TODO: Handle more than Not Found.
)

"""
# Note regarding on this endpoint

Will work on this one when I was able to finish the explorer and node API functionalities.
"""


@dashboard_router.get(
    "/dashboard",
    tags=[DashboardAPI.DASHBOARD_GENERAL_API.value],
    response_model=DashboardContext,
    summary="Obtains necessary information for the dashboard display.",
    description="An API endpoint that returns the data of the user based on their role.",
)
async def get_data_to_dashboard(context: DashboardContext):
    pass


@dashboard_router.post(
    "/login",
    tags=[DashboardAPI.DASHBOARD_GENERAL_API.value],
    # response_model=UserLoginResult,
    summary="Logs the user from the dashboard.",
    description="An API endpoint that logs the user based on their credentials.",
)
async def login_user(credentials):
    return None  # For now.


@dashboard_router.post(
    "/logout",
    tags=[DashboardAPI.DASHBOARD_GENERAL_API.value],
    summary="Invalidates user's session.",
    description="An API endpoint that logouts the user by invalidating the JWT token.",
    status_code=HTTPStatus.OK,
)
async def logout_user(to_invalidate):
    pass


@dashboard_router.get(
    "/applicants",
    tags=[DashboardAPI.EMPLOYER_API.value],
    response_model=List[Applicants],
    summary="Obtains a list of individuals who opted from the employer's company.",
    description="An API-exclusive to employers that obtains a list of individuals (applicants) who applies to them.",
)
async def get_applicants(
    applicant_count: int
    | None = Query(
        ItemReturnCount.MIN,
        title="Number of Applicants to Return",
        description="The number of applicants to return.",
    ),
    page: int
    | None = Query(
        None,
        title="Current Index Page",
        description="The page you are currently sitting, defaults to page 1. Other pages are available if the `applicant_count` is higher than the number of returned blocks.",  # TODO: If this renders the `` style, use it across other arguments that have the same functionality.
    ),
):
    pass


@dashboard_router.get(
    "/applicant/{applicant_id}",
    tags=[DashboardAPI.EMPLOYER_API.value],
    response_model=Applicant,
    summary="Obtain a certain individual.",
    description="An API-exclusive to employers that obtains a particular individual, which displays their information.",
)
async def get_applicant(applicant_id: AddressUUID):
    pass


@dashboard_router.get(
    "/requests",
    tags=[
        DashboardAPI.APPLICANT_API.value,
        DashboardAPI.EMPLOYER_API.value,
        DashboardAPI.INSTITUTION_API.value,
    ],
    response_model=List[Requests],
    summary="Obtains all requests associated to this client-individual.",
    description="An API endpoint that obtains all requests associated to this user. This endpoint is also flexible for all roles associated from this system.",
)
async def get_all_requests():
    pass


@dashboard_router.get(
    "/request/{request_id}",
    tags=[
        DashboardAPI.APPLICANT_API.value,
        DashboardAPI.EMPLOYER_API.value,
        DashboardAPI.INSTITUTION_API.value,
    ],
    response_model=Request,
    summary="Obtain a particular request. Context-protected based on the association of the user.",
    description="An API endpoint that returns a particular requests that is associated from this user.",
)
async def get_request(request_id: int):  # Remember the type assertion here.
    pass


@dashboard_router.get(
    "/request/{request_id}/request_view/{doc_type}",
    tags=[DashboardAPI.EMPLOYER_API.value],
    # response_model = RequestDocView,
    summary="Submit request for viewing a particular document from the applicant.",
    description="An API-exclusive to employers that allows them to make request for documents to be viewed.",
)
async def request_document_view(
    request_id: int, doc_type: str
):  # TODO: Types. | doc_type should have choices.
    pass


@dashboard_router.get(
    "/issuances",
    tags=[DashboardAPI.INSTITUTION_API.value],
    response_model=Issuances,
    summary="Get a list of issuances from the students.",
    description="An API endpoint that returns of a list of issuances that was invoked from the students.",
)
async def get_issuances(
    issuance_count: int
    | None = Query(
        ItemReturnCount.MIN,
        title="Number of Issued Documents to Return",
        description="The number of documents issued to return.",
    ),
    page: int
    | None = Query(
        None,
        title="Current Index Page",
        description="The page you are currently sitting, defaults to page 1. Other pages are available if the `applicant_count` is higher than the number of returned blocks.",  # TODO: If this renders the `` style, use it across other arguments that have the same functionality.
    ),
):
    pass


@dashboard_router.get(
    "/issuance/{issue_id}",
    tags=[DashboardAPI.INSTITUTION_API.value],
    response_model=Issuance,
    summary="Obtain a particular issued document.",
    description="An API endpoint that obtains a specified document based on its ID.",
)
async def get_issued_docs(issue_id: int):
    pass


@dashboard_router.post(
    "/issue",
    tags=[DashboardAPI.INSTITUTION_API.value],
    response_model=IssueToStudentOut,
    summary="Submit a document to mint from the blockchain.",
    description="An API endpoint that allows institutions to submit new documents in the blockchain. Note that minting them requires user (address) reference.",
)
async def mint_document(doc_context: IssueToStudentIn):
    pass


@dashboard_router.get(
    "/students",
    tags=[DashboardAPI.INSTITUTION_API.value],
    response_model=Students,
    summary="Obtain a list of classified students in the blockchain.",
    description="An API endpoint that returns a list of addresses that is classified as student.",
)
async def get_students(
    student_count: int
    | None = Query(
        ItemReturnCount.MIN,
        title="Number of Students to Return",
        description="The number of students to return.",
    ),
    page: int
    | None = Query(
        None,
        title="Current Index Page",
        description="The page you are currently sitting, defaults to page 1. Other pages are available if the `applicant_count` is higher than the number of returned blocks.",  # TODO: If this renders the `` style, use it across other arguments that have the same functionality.
    ),
):
    pass


@dashboard_router.get(
    "/student/{student_addr}",
    tags=[DashboardAPI.INSTITUTION_API.value],
    response_model=Student,
    summary="Obtain a particular student's information.",
    description="An API endpoint that obtains a student along with its readable information.",
)
async def get_student(student_addr: AddressUUID):
    pass


# ! TODO: We need PUT method and a batch push accounts method to the blockchain so that it is less error prone. We implement that if we already have the web.
@dashboard_router.post(
    "/student",
    tags=[DashboardAPI.INSTITUTION_API.value],
    response_model=NewStudentOut,
    summary="Create a student information for the blockchain to recognize.",
    description="An API endpoint that creates a student account on the blockchain.",
)
async def create_student(student_context: NewStudentIn):
    pass
