"""
Node Component, Dashboard API
This section contains API endpoints for the dashboard. Dashboard API is only available on Node API with a role of Master Node. As a developer, I do understand the consequences of a node running 3 set of APIs, but to cut costs, I need to deploy it this way. In ideal world, this is not acceptable.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from datetime import datetime, timedelta
from http import HTTPStatus
from pathlib import Path
from sqlite3 import IntegrityError
from typing import Any, Mapping
from databases import Database

from sqlalchemy import Column, func, select

from blueprint.models import (
    associations,
    portfolio_settings,
    tx_content_mappings,
    users,
)
from blueprint.schemas import (
    ApplicantEditableProperties,
    DashboardContext,
    PortfolioLog,
    PortfolioSettings,
    Student,
)
from core.constants import BaseAPI, DashboardAPI, HashUUID, UserEntity
from core.dependencies import EnsureAuthorized
from fastapi import APIRouter, Depends, Form, HTTPException, Response, UploadFile
from sqlalchemy.sql.expression import Select, Update
from starlette.datastructures import UploadFile as StarletteUploadFile

from core.constants import AddressUUID
from core.dependencies import get_database_instance
from core.constants import (
    ASYNC_TARGET_LOOP,
    PORTFOLIO_MINUTE_TO_ALLOW_STATE_CHANGE,
    USER_AVATAR_FOLDER_NAME,
    TransactionContextMappingType,
)
from aiofiles import open as aopen
from logging import getLogger, Logger

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

dashboard_router = APIRouter(
    prefix="/dashboard",
    tags=[BaseAPI.DASHBOARD.value],
)


@dashboard_router.get(
    "",
    tags=[DashboardAPI.DASHBOARD_GENERAL_API.value],
    response_model=DashboardContext,
    summary="Obtains necessary information for the dashboard display.",
    description="An API endpoint that returns the data of the user based on their role.",
)
async def get_dashboard_data(
    database_instance: Database = Depends(get_database_instance),
    entity_address_ref: AddressUUID
    | None = Depends(
        EnsureAuthorized(
            _as=[
                UserEntity.ORGANIZATION_DASHBOARD_USER,
                UserEntity.APPLICANT_DASHBOARD_USER,
            ],
            return_address_from_token=True,
        )
    ),
) -> DashboardContext:
    # - Get the context of this user.

    if entity_address_ref is None:
        raise HTTPException(
            detail="Entity address does reference does not exist.",
            status_code=HTTPStatus.NOT_FOUND,
        )

    get_user_basic_context_query: Select = select(
        [users.c.first_name, users.c.last_name, users.c.username, users.c.type]
    ).where(users.c.unique_address == entity_address_ref)

    user_basic_context = await database_instance.fetch_val(get_user_basic_context_query)

    if user_basic_context is None:
        raise HTTPException(
            detail="No information is provided from the user, but does exists.",
            status_code=HTTPStatus.NOT_FOUND,
        )

    return DashboardContext(
        address=user_basic_context.unique_address,
        first_name=user_basic_context.first_name,
        last_name=user_basic_context.last_name,
        username=user_basic_context.username,
        role=user_basic_context.role,
        reports=None,  # # For now.
    )


@dashboard_router.get(
    "/students",
    tags=[
        DashboardAPI.INSTITUTION_API.value,
    ],
    response_model=list[Student],
    summary="Returns a set of students associated from the organization.",
    description="An API endpoint that returns generated students from the blockchain, solely from the association from where this institution user belongs.",
)
async def get_associated_students(
    database_instance: Database = Depends(get_database_instance),
    org_user_address: AddressUUID
    | None = Depends(
        EnsureAuthorized(
            _as=UserEntity.ORGANIZATION_DASHBOARD_USER, return_address_from_token=True
        )
    ),
) -> list[Student]:

    qualified_students: list[Student] = []

    # - [1] Get the `association` address from this user.
    get_association_from_address_query: Select = select([users.c.association]).where(
        users.c.unique_address == org_user_address
    )
    association_address_ref: AddressUUID | None = AddressUUID(
        await database_instance.fetch_val(get_association_from_address_query)
    )

    if association_address_ref is None:
        raise HTTPException(
            detail="There is no association from this user.",
            status_code=HTTPStatus.NOT_FOUND,
        )

    # - [2] Get students who are associated with it.

    get_students_as_applicants_query: Select = select(
        [
            users.c.first_name,
            users.c.lastname,
            users.c.unique_address,
            users.c.speciality,
            users.c.date_registered,
        ]
    ).where(users.c.association == association_address_ref)

    list_of_qualified_students = await database_instance.fetch_all(
        get_students_as_applicants_query
    )

    for each_student in list_of_qualified_students:
        qualified_students.append(
            Student(
                first_name=each_student.first_name,
                last_name=each_student.last_name,
                address=each_student.unique_address,
                program=each_student.program,
                date_created=each_student.date_registered,
            )
        )

    return qualified_students


@dashboard_router.get(
    "/user_profile",
    tags=[DashboardAPI.APPLICANT_API.value],
    response_model=ApplicantEditableProperties,
    summary="Returns the editable information from the applicant.",
    description="An API endpoint that returns information that are editable from the applicant to display from their portfolio.",
)
async def get_user_profile(
    applicant_address_ref: AddressUUID
    | None = Depends(
        EnsureAuthorized(
            _as=UserEntity.APPLICANT_DASHBOARD_USER, return_address_from_token=True
        )
    ),
    database_instance: Database = Depends(get_database_instance),
) -> ApplicantEditableProperties:
    # - Get the information of this user.
    get_editable_info_query: Select = select(
        [users.c.avatar, users.c.description, users.c.personal_skills]
    ).where(users.c.unique_address == applicant_address_ref)

    editable_infos: list[Mapping] = await database_instance.fetch_val(
        get_editable_info_query
    )

    return ApplicantEditableProperties(
        avatar=editable_infos.avatar,
        description=editable_infos.description,
        personal_skills=editable_infos.personal_skills,
    )


@dashboard_router.post(
    "/apply_profile_changes",
    tags=[DashboardAPI.APPLICANT_API.value],
    response_model=ApplicantEditableProperties,
    summary="Applies changes of the editable information of the applicant.",
    description="An API endpoint that applies changes to the editable information of the applicant.",
    status_code=HTTPStatus.ACCEPTED,
)
async def save_user_profile(
    applicant_address_ref: AddressUUID
    | None = Depends(
        EnsureAuthorized(
            _as=UserEntity.APPLICANT_DASHBOARD_USER, return_address_from_token=True
        )
    ),
    database_instance: Database = Depends(get_database_instance),
    avatar: UploadFile | None = Form(None, title="The avatar of this user."),
    description: str
    | None = Form(None, title="The description that basically describes the user."),
    personal_skills: str
    | None = Form(
        None,
        title="Skills that can be displayed from the portfolio to show extra bits of this user.",
    ),
) -> Response:
    # * State variables.
    resolved_avatar_dir: str = ""

    if applicant_address_ref is None:
        raise HTTPException(
            detail="Cannot update the user profile because it doesn't exists or you are not authorized.",
            status_code=HTTPStatus.NOT_FOUND,
        )

    # - Check for the fields.
    if avatar is None and description is None and personal_skills is None:
        return Response(status_code=HTTPStatus.ACCEPTED)

    # - When there's a avatar, just save, don't make it complicated bro.
    if isinstance(avatar, StarletteUploadFile):
        # @o Is there a directory for the `USER_AVATAR_FOLDER_NAME`?
        user_avatar_dir: Path = Path(USER_AVATAR_FOLDER_NAME)
        resolved_avatar_dir = f"{user_avatar_dir}/{avatar.filename}".replace(":", "_")

        if not user_avatar_dir.is_dir() or not user_avatar_dir.exists():
            logger.warning(
                f"Directory for the {user_avatar_dir} is missing, now created."
            )
            user_avatar_dir.mkdir()

        # - Write the avatar file.
        async with aopen(resolved_avatar_dir, "wb") as avatar_file_writer:
            await avatar_file_writer.write(avatar.file.read())

    try:
        # - Save it from the database, and encode the resources.
        # - Frontend should return the given data back.
        update_user_editable_info: Update = (
            users.update()
            .where(users.c.unique_address == applicant_address_ref)
            .values(
                avatar=resolved_avatar_dir,
                description=description,
                personal_skills=personal_skills,
            )
        )
        await database_instance.execute(update_user_editable_info)

    except IntegrityError:
        raise HTTPException(
            detail="There was an error from updating your user profile.",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    return Response(status_code=HTTPStatus.ACCEPTED)


@dashboard_router.get(
    "/portfolio",
    tags=[DashboardAPI.INSTITUTION_API.value, DashboardAPI.APPLICANT_API.value],
    summary="Renders the portfolio of this applicant.",
    description="An API-exclusive to applicants where they can view their portfolio.",
)
async def get_portfolio() -> None:
    # # Prep.
    # - [1] Check if applicant has a `APPLICANT_BASE` tx_mapping.
    # - [2] Load the portfolio properties.
    # - [3] Check for any `APPLICANT_LOG` to render.
    # - [4] Do the rendering part.
    # - [5] Check for any `APPLICANT_EXTRA` to render.
    # - [6] Do the rendering part.
    # - [7] Setup the pydantic model. (Create one actually.)
    # - [8] Hide all necessary parts or take the portfolio settings in effect.
    # - [9] Render all data to pydantic model.

    # * Integration stuff.
    # - We may need to modify the structure of this endpoint, specially the `EnsureAuthorized`.
    # - Check the performance. xd

    return


@dashboard_router.get(
    "/portfolio_settings",
    tags=[DashboardAPI.APPLICANT_API],
    response_model=PortfolioSettings,
    summary="Returns the state of the portfolio.",
    description="An API endpoint that returns the state of portfolio, where state changes affects the output of the portfolio.",
)
async def get_portfolio_settings(
    applicant_address_ref: AddressUUID
    | None = Depends(
        EnsureAuthorized(
            _as=UserEntity.APPLICANT_DASHBOARD_USER, return_address_from_token=True
        )
    ),
    database_instance: Database = Depends(get_database_instance),
) -> PortfolioSettings:

    # - Ensure that this user has a transaction mapping `APPLICANT_BASE`.
    validate_tx_mapping_from_user_query: Select = select([func.now()]).where(
        (tx_content_mappings.c.address_ref == applicant_address_ref)
        & (
            tx_content_mappings.c.content_type
            is TransactionContextMappingType.APPLICANT_BASE
        )
    )

    contains_tx_mapping: int = await database_instance.fetch_val(
        validate_tx_mapping_from_user_query
    )

    if not contains_tx_mapping:
        raise HTTPException(
            detail="Applicant contains no transaction mapping of their content. Report this issue to the developers for possible-workaround.",
            status_code=HTTPStatus.NOT_FOUND,
        )

    # - Fetch the the portfolio properties of this user.
    get_portfolio_state_query: Select = select(
        [
            portfolio_settings.c.sharing_state,
            portfolio_settings.c.expose_email_state,
            portfolio_settings.c.show_files,
        ]
    ).where(portfolio_settings.c.from_user == applicant_address_ref)

    portfolio_states = await database_instance.fetch_val(get_portfolio_state_query)

    return PortfolioSettings(
        enable_sharing=portfolio_states.sharing_state,
        expose_email_info=portfolio_states.expose_email_state,
        show_files=portfolio_states.show_files,
    )


@dashboard_router.post(
    "/apply_portfolio_settings",
    tags=[DashboardAPI.APPLICANT_API],
    summary="Applies portfolio setting from applicant's portfolio.",
    description="An API endpoint that applies changes to the portfolio's state.",
    status_code=HTTPStatus.ACCEPTED,
)
async def save_portfolio_settings(
    portfolio_state_payload: PortfolioSettings,
    applicant_address_ref: AddressUUID
    | None = Depends(
        EnsureAuthorized(
            _as=UserEntity.APPLICANT_DASHBOARD_USER, return_address_from_token=True
        )
    ),
    database_instance: Database = Depends(get_database_instance),
) -> Response:

    # - Check the state of the `datetime_to_allowed_changes` and see if datetime is way past the current time.
    portfolio_update_expiration_query: Select = select(
        [portfolio_settings.c.datetime_to_allowed_changes]
    ).where(portfolio_settings.c.from_user == applicant_address_ref)

    portfolio_expiration: datetime | None = await database_instance.fetch_val(
        portfolio_update_expiration_query
    )

    # - Check conditions regarding the datetime-based rate limitation of state change proposal.
    if portfolio_expiration is None:
        raise HTTPException(
            detail="There was no expiration invoked from this user's portfolio.",
            status_code=HTTPStatus.NOT_ACCEPTABLE,
        )

    if portfolio_expiration > datetime.now():
        raise HTTPException(
            detail="Rate limited. Please comeback later.",
            status_code=HTTPStatus.TOO_EARLY,
        )

    try:
        # - Update the database when `datetime_to_allowed_changes` were way past the current time.
        update_portfolio_state_query: Update = (
            portfolio_settings.update()
            .where(portfolio_settings.c.from_user == applicant_address_ref)
            .values(
                sharing_state=portfolio_state_payload.enable_sharing,
                expose_email_state=portfolio_state_payload.expose_email_info,
                show_files=portfolio_state_payload.show_files,
                datetime_to_allowed_changes=datetime.now()
                + timedelta(minutes=PORTFOLIO_MINUTE_TO_ALLOW_STATE_CHANGE),
            )
        )

        await database_instance.execute(update_portfolio_state_query)

    except IntegrityError:
        raise HTTPException(
            detail="There was an error processing your portfolio state change, please try again.",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    return Response(status_code=HTTPStatus.ACCEPTED)
