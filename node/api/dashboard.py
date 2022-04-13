"""
Node Component, Dashboard API
This section contains API endpoints for the dashboard. Dashboard API is only available on Node API with a role of Master Node. As a developer, I do understand the consequences of a node running 3 set of APIs, but to cut costs, I need to deploy it this way. In ideal world, this is not acceptable.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Any
from blueprint.schemas import (
    DashboardContext,
    NewStudentOut,
    Student,
    Students,
)
from core.constants import (
    QUERY_CURRENT_INDEX_NAME_DESCRIPTION,
    QUERY_CURRENT_INDEX_PAGE_NAME,
    AddressUUID,
    BaseAPI,
    DashboardAPI,
    ExplorerBlockItemReturnCount,
)
from fastapi import APIRouter, Query

dashboard_router = APIRouter(
    prefix="/dashboard",
    tags=[BaseAPI.DASHBOARD.value],
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
async def get_data_to_dashboard(*, context: DashboardContext) -> None:
    return


@dashboard_router.get(
    "/applicants",
    tags=[DashboardAPI.EMPLOYER_API.value],
    description="An API-exclusive to employers that obtains a list of individuals (applicants) who applies to them.",
)
async def get_applicants(
    *,
    applicant_count: int
    | None = Query(
        ExplorerBlockItemReturnCount.MIN,
        title="Number of Applicants to Return",
        description="The number of applicants to return.",
    ),
    page: int
    | None = Query(
        None,
        title=QUERY_CURRENT_INDEX_PAGE_NAME,
        description=QUERY_CURRENT_INDEX_NAME_DESCRIPTION,
    ),
) -> None:
    return


@dashboard_router.get(
    "/applicant/{applicant_id}",
    tags=[DashboardAPI.EMPLOYER_API.value],
    # response_model=Applicant,
    summary="Obtain a certain individual.",
    description="An API-exclusive to employers that obtains a particular individual, which displays their information.",
)
async def get_applicant(*, applicant_id: AddressUUID) -> None:
    return


@dashboard_router.get(
    "/requests",
    tags=[
        DashboardAPI.APPLICANT_API.value,
        DashboardAPI.EMPLOYER_API.value,
        DashboardAPI.INSTITUTION_API.value,
    ],
    description="An API endpoint that obtains all requests associated to this user. This endpoint is also flexible for all roles associated from this system.",
)
async def get_all_requests() -> None:  # TODO.
    return


@dashboard_router.get(
    "/request/{request_id}",
    tags=[
        DashboardAPI.APPLICANT_API.value,
        DashboardAPI.EMPLOYER_API.value,
        DashboardAPI.INSTITUTION_API.value,
    ],
    # response_model=Request,
    summary="Obtain a particular request. Context-protected based on the association of the user.",
    description="An API endpoint that returns a particular requests that is associated from this user.",
)
async def get_request(*, request_id: int) -> None:
    return


@dashboard_router.get(
    "/request/{request_id}/request_view/{doc_type}",
    tags=[DashboardAPI.EMPLOYER_API.value],
    # response_model = RequestDocView,
    summary="Submit request for viewing a particular document from the applicant.",
    description="An API-exclusive to employers that allows them to make request for documents to be viewed.",
)
async def request_document_view(
    *, request_id: int, doc_type: str
) -> None:  # TODO: Types. | doc_type should have choices.
    return


@dashboard_router.get(
    "/issuances",
    tags=[DashboardAPI.INSTITUTION_API.value],
    # response_model=Issuances,
    summary="Get a list of issuances from the students.",
    description="An API endpoint that returns of a list of issuances that was invoked from the students.",
)
async def get_issuances(
    *,
    issuance_count: int
    | None = Query(
        ExplorerBlockItemReturnCount.MIN,
        title="Number of Issued Documents to Return",
        description="The number of documents issued to return.",
    ),
    page: int
    | None = Query(
        None,
        title=QUERY_CURRENT_INDEX_PAGE_NAME,
        description=QUERY_CURRENT_INDEX_NAME_DESCRIPTION,  # TODO: [TO BE CONFIRMED] If this renders the `` style, use it across other arguments that have the same functionality.
    ),
) -> None:
    pass


@dashboard_router.get(
    "/issuance/{issue_id}",
    tags=[DashboardAPI.INSTITUTION_API.value],
    # response_model=Issuance,
    summary="Obtain a particular issued document.",
    description="An API endpoint that obtains a specified document based on its ID.",
)
async def get_issued_docs(*, issue_id: int) -> None:
    return


@dashboard_router.post(
    "/issue",
    tags=[DashboardAPI.INSTITUTION_API.value],
    # response_model=IssueToStudentOut,
    summary="Submit a document to mint from the blockchain.",
    description="An API endpoint that allows institutions to submit new documents in the blockchain. Note that minting them requires user (address) reference.",
)
async def mint_document(*, doc_context: Any) -> None:
    return


@dashboard_router.get(
    "/students",
    tags=[DashboardAPI.INSTITUTION_API.value],
    response_model=Students,
    summary="Obtain a list of classified students in the blockchain.",
    description="An API endpoint that returns a list of addresses that is classified as student.",
)
async def get_students(
    *,
    student_count: int
    | None = Query(
        ExplorerBlockItemReturnCount.MIN,
        title="Number of Students to Return",
        description="The number of students to return.",
    ),
    page: int
    | None = Query(
        None,
        title=QUERY_CURRENT_INDEX_PAGE_NAME,
        description=QUERY_CURRENT_INDEX_NAME_DESCRIPTION,  # TODO: If this renders the `` style, use it across other arguments that have the same functionality.
    ),
) -> None:
    return


@dashboard_router.get(
    "/student/{student_addr}",
    tags=[DashboardAPI.INSTITUTION_API.value],
    response_model=Student,
    summary="Obtain a particular student's information.",
    description="An API endpoint that obtains a student along with its readable information.",
)
async def get_student(*, student_addr: AddressUUID) -> None:
    return


# ! TODO: We need PUT method and a batch push accounts method to the blockchain so that it is less error prone. We implement that if we already have the web.
@dashboard_router.post(
    "/student",
    tags=[DashboardAPI.INSTITUTION_API.value],
    response_model=NewStudentOut,
    summary="Create a student information for the blockchain to recognize.",
    description="An API endpoint that creates a student account on the blockchain.",
)
async def create_student(*, student_context: Any) -> None:
    return
