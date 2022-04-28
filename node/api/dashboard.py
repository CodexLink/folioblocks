"""
Node Component, Dashboard API
This section contains API endpoints for the dashboard. Dashboard API is only available on Node API with a role of Master Node. As a developer, I do understand the consequences of a node running 3 set of APIs, but to cut costs, I need to deploy it this way. In ideal world, this is not acceptable.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from http import HTTPStatus

from blueprint.schemas import (
    ApplicantEditableProperties,
    DashboardContext,
    PortfolioLogs,
    PortfolioSettings,
    Student,
    StudentDetail,
)
from core.constants import BaseAPI, DashboardAPI, HashUUID, UserEntity
from core.dependencies import EnsureAuthorized
from fastapi import APIRouter, Depends, HTTPException

dashboard_router = APIRouter(
    prefix="/dashboard",
    tags=[BaseAPI.DASHBOARD.value],
)

"""
# Note regarding on this endpoint

Will work on this one when I was able to finish the explorer and node API functionalities.
"""


@dashboard_router.get(
    "",
    tags=[DashboardAPI.DASHBOARD_GENERAL_API.value],
    response_model=DashboardContext,
    summary="Obtains necessary information for the dashboard display.",
    description="An API endpoint that returns the data of the user based on their role.",
    dependencies=[
        Depends(
            EnsureAuthorized(
                _as=[
                    UserEntity.ORGANIZATION_DASHBOARD_USER,
                    UserEntity.APPLICANT_DASHBOARD_USER,
                ],
                return_token=True,
            )
        )
    ],
)
async def fetch_dashboard_data() -> HTTPException:
    return HTTPException(detail="Works.", status_code=HTTPStatus.NOT_IMPLEMENTED)


@dashboard_router.get(
    "/students",
    tags=[
        DashboardAPI.INSTITUTION_API.value,
    ],
    response_model=list[Student],
    summary="Returns a set of students associated from the organization.",
    description="An API endpoint that returns generated students from the blockchain, solely from the association from where this institution user belongs.",
    dependencies=[
        Depends(
            EnsureAuthorized(
                _as=UserEntity.ORGANIZATION_DASHBOARD_USER, return_token=True
            )
        )
    ],
)
async def fetch_associated_students() -> None:
    return


@dashboard_router.get(
    "/student/{address}",
    tags=[
        DashboardAPI.INSTITUTION_API.value,
    ],
    response_model=StudentDetail,
    summary="Returns generated information of the student, non-editable.",
    description="An API endpoint that returns the information of the student.",
    dependencies=[
        Depends(
            EnsureAuthorized(
                _as=UserEntity.ORGANIZATION_DASHBOARD_USER, return_token=True
            )
        )
    ],
)
async def fetch_associated_student(*, address: HashUUID) -> StudentDetail:
    return StudentDetail()


@dashboard_router.get(
    "/user_profile",
    tags=[DashboardAPI.APPLICANT_API.value],
    response_model=ApplicantEditableProperties,
    summary="Returns the editable information from the applicant.",
    description="An API endpoint that returns information that are editable from the applicant to display from their portfolio.",
)
async def fetch_user_profile() -> ApplicantEditableProperties:
    return ApplicantEditableProperties()


@dashboard_router.post(
    "/apply_profile_changes",
    tags=[DashboardAPI.APPLICANT_API.value],
    response_model=ApplicantEditableProperties,
    summary="Applies changes of the editable information of the applicant.",
    description="An API endpoint that applies changes to the editable information of the applicant.",
    status_code=HTTPStatus.ACCEPTED,
)
async def save_user_profile(data: ApplicantEditableProperties) -> None:
    return None
    # return Response(status_code=HTT)


@dashboard_router.get(
    "/portfolio",
    tags=[DashboardAPI.INSTITUTION_API.value, DashboardAPI.APPLICANT_API.value],
    summary="Renders the portfolio of this applicant.",
    description="An API-exclusive to applicants where they can view their portfolio.",
)
async def fetch_portfolio() -> None:
    return


@dashboard_router.get(
    "/portfolio_settings",
    tags=[DashboardAPI.APPLICANT_API],
    response_model=PortfolioSettings,
    summary="Returns the state of the portfolio.",
    description="An API endpoint that returns the state of portfolio, where state changes affects the output of the portfolio.",
)
async def fetch_portfolio_settings() -> None:
    return


@dashboard_router.get(
    "/apply_portfolio_settings",
    tags=[DashboardAPI.APPLICANT_API],
    summary="Applies portfolio setting from applicant's portfolio.",
    description="An API endpoint that applies changes to the portfolio's state.",
    status_code=HTTPStatus.ACCEPTED,
)
async def save_portfolio_settings() -> None:
    return


@dashboard_router.get(
    "/portfolio_log",
    tags=[DashboardAPI.APPLICANT_API.value],
    response_model=PortfolioLogs,
    summary="Fetches the logs regarding this portfolio.",
    description="An API endpoint that returns the logs of the portfolio, which should contain the changes done.",
)
async def fetch_portfolio_log() -> None:
    return
