"""
Node Component, Dashboard API
This section contains API endpoints for the dashboard. Dashboard API is only available on Node API with a role of Master Node. As a developer, I do understand the consequences of a node running 3 set of APIs, but to cut costs, I need to deploy it this way. In ideal world, this is not acceptable.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

from base64 import urlsafe_b64encode
from datetime import datetime, timedelta
from http import HTTPStatus
from logging import Logger, getLogger
from pathlib import Path
from sqlite3 import IntegrityError
from typing import Any, Mapping

from aiofiles import open as aopen
from blueprint.models import portfolio_settings, tx_content_mappings, users
from blueprint.schemas import (
    ApplicantEditableProperties,
    DashboardContext,
    Portfolio,
    PortfolioSettings,
    Student,
)
from core.blockchain import BlockchainMechanism, get_blockchain_instance
from core.constants import (
    ASYNC_TARGET_LOOP,
    PORTFOLIO_MINUTES_TO_ALLOW_STATE_CHANGE,
    USER_AVATAR_FOLDER_NAME,
    AddressUUID,
    BaseAPI,
    DashboardAPI,
    TransactionContextMappingType,
    UserEntity,
)
from core.dependencies import EnsureAuthorized, get_database_instance
from databases import Database
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query
from fastapi import Path as PathParams
from fastapi import Response, UploadFile
from sqlalchemy import func, select
from sqlalchemy.sql.expression import Select, Update
from starlette.datastructures import UploadFile as StarletteUploadFile
from cryptography.fernet import Fernet

from core.constants import (
    FILE_PAYLOAD_TO_ADDRESS_CHAR_LIMIT_MAX,
    FILE_PAYLOAD_TO_ADDRESS_CHAR_LIMIT_MIN,
    FILE_PAYLOAD_TO_ADDRESS_START_TRUNCATION_INDEX,
    USER_FILES_FOLDER_NAME,
    HashUUID,
    TransactionActions,
)
from core.constants import FILE_PAYLOAD_TIMESTAMP_FORMAT_AS_KEY
from blueprint.schemas import PortfolioLoadedContext
from blueprint.schemas import DashboardApplicant, DashboardOrganization

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
        [
            users.c.first_name,
            users.c.last_name,
            users.c.username,
            users.c.type,
            users.c.association,
        ]
    ).where(users.c.unique_address == entity_address_ref)

    user_basic_context = await database_instance.fetch_one(get_user_basic_context_query)

    if user_basic_context is None:
        raise HTTPException(
            detail="No information is provided from the user, but does exists.",
            status_code=HTTPStatus.NOT_FOUND,
        )

    resolved_reports: DashboardApplicant | DashboardOrganization | None = None

    if user_basic_context.type is UserEntity.ORGANIZATION_DASHBOARD_USER:
        # - Get reports from the `users` for the the number of associated people from the association.
        get_associates_query: Select = select([users.c.unique_address]).where(
            users.c.association == user_basic_context.association
        )

        associates = await database_instance.fetch_all(get_associates_query)

        # - Get reports from the `tx_content_mapping` for the number of associated logs and extra.
        associate_log_count: int = 0
        associate_extra_count: int = 0

        for each_associate in associates:
            get_associated_logs_query: Select = select([func.count()]).where(
                (tx_content_mappings.c.address_ref == each_associate.unique_address)
                & (
                    tx_content_mappings.c.content_type
                    == TransactionContextMappingType.APPLICANT_LOG
                )
            )

            associate_logs_count = await database_instance.fetch_val(
                get_associated_logs_query
            )

            if associate_log_count is not None and isinstance(associate_log_count, int):
                associate_log_count += associate_logs_count

            get_associated_extra_query: Select = select([func.count()]).where(
                (tx_content_mappings.c.address_ref == each_associate.unique_address)
                & (
                    tx_content_mappings.c.content_type
                    == TransactionContextMappingType.APPLICANT_ADDITIONAL
                )
            )

            associate_extra_related = await database_instance.fetch_val(
                get_associated_extra_query
            )

            if associate_extra_related is not None and isinstance(
                associate_extra_related, int
            ):
                associate_extra_count += associate_extra_related

        # - Get the overall count of the transaction to get the calculation fine.
        get_overall_tx_count_query: Select = select([func.count()]).select_from(
            tx_content_mappings
        )

        overall_tx_count = await database_instance.fetch_val(get_overall_tx_count_query)

        # - Get the overall user count from the system.
        get_overall_user_count_query: Select = select([func.count()]).select_from(users)

        user_count = await database_instance.fetch_val(get_overall_user_count_query)

        resolved_reports = DashboardOrganization(
            total_associated=len(associates),
            total_users=user_count,
            total_associated_logs=associate_log_count,
            total_associated_extra=associate_extra_count,
            total_overall_info_outside=overall_tx_count,
        )

    elif user_basic_context.type is UserEntity.APPLICANT_DASHBOARD_USER:
        # - Get count of associated logs from this applicant.
        get_logs_associated_count_query: Select = select([func.count()]).where(
            (tx_content_mappings.c.address_ref == entity_address_ref)
            & (
                tx_content_mappings.c.content_type
                == TransactionContextMappingType.APPLICANT_LOG
            )
        )

        logs_count = await database_instance.fetch_val(get_logs_associated_count_query)

        # - Get count of associated extra from this applicant.
        get_extra_associated_count_query: Select = select([func.count()]).where(
            (tx_content_mappings.c.address_ref == entity_address_ref)
            & (
                tx_content_mappings.c.content_type
                == TransactionContextMappingType.APPLICANT_ADDITIONAL
            )
        )

        extra_count = await database_instance.fetch_val(
            get_extra_associated_count_query
        )

        # - Get the overall count of the transaction to get the calculation fine.
        overall_tx_count_query: Select = select([func.count()]).select_from(
            tx_content_mappings
        )

        overall_tx_count = await database_instance.fetch_val(overall_tx_count_query)

        # - Get portfolio of this user for client-side calculation.
        get_portfolio_context_query: Select = portfolio_settings.select().where(
            portfolio_settings.c.from_user == entity_address_ref
        )

        portfolio_context = await database_instance.fetch_one(
            get_portfolio_context_query
        )

        resolved_reports = DashboardApplicant(
            extra_associated_count=extra_count,
            logs_associated_count=logs_count,
            total_txs_overall=overall_tx_count,
            portfolio=PortfolioSettings(
                enable_sharing=portfolio_context.sharing_state,
                expose_email_info=portfolio_context.expose_email_state,
                show_files=portfolio_context.show_files,
            ),
        )

    else:
        raise HTTPException(
            detail="Cannot parse this user's information due to its role unqualified to access the dashboard.",
            status_code=HTTPStatus.FORBIDDEN,
        )

    return DashboardContext(
        address=entity_address_ref,
        first_name=user_basic_context.first_name,
        last_name=user_basic_context.last_name,
        username=user_basic_context.username,
        role=user_basic_context.type,
        reports=resolved_reports,
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
            users.c.last_name,
            users.c.unique_address,
            users.c.program,
            users.c.date_registered,
        ]
    ).where(
        (users.c.association == association_address_ref)
        & (users.c.type == UserEntity.APPLICANT_DASHBOARD_USER)
    )

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
        [users.c.avatar, users.c.description, users.c.skills, users.c.preferred_role]
    ).where(users.c.unique_address == applicant_address_ref)

    editable_infos = await database_instance.fetch_one(get_editable_info_query)

    return ApplicantEditableProperties(
        avatar=editable_infos.avatar,
        description=editable_infos.description,
        personal_skills=editable_infos.skills,
        preferred_role=editable_infos.preferred_role,
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
    avatar: UploadFile | None = File(None, title="The avatar of this user."),
    description: str
    | None = Form(None, title="The description that basically describes the user."),
    personal_skills: str
    | None = Form(
        None,
        title="Skills that can be displayed from the portfolio to show extra bits of this user.",
    ),
    preferred_role: str
    | None = Form(None, title="The student's preference over something to work on."),
) -> Response:
    # * State variables.
    resolved_avatar_dir: str = ""

    if applicant_address_ref is None:
        raise HTTPException(
            detail="Cannot update the user profile because it doesn't exists or you are not authorized.",
            status_code=HTTPStatus.NOT_FOUND,
        )

    # - Check for the fields.
    if (
        avatar is None
        and description is None
        and personal_skills is None
        and preferred_role is None
    ):
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
                skills=personal_skills,
                preferred_role=preferred_role,
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
    response_model=Portfolio,
    summary="Renders the portfolio of this applicant.",
    description="An API-exclusive to applicants where they can view their portfolio.",
)
async def get_portfolio(
    blockchain_instance: BlockchainMechanism | None = Depends(get_blockchain_instance),
    database_instance: Database = Depends(get_database_instance),
    returned_address_ref: AddressUUID
    | None = Depends(
        EnsureAuthorized(
            _as=[
                UserEntity.ORGANIZATION_DASHBOARD_USER,
                UserEntity.APPLICANT_DASHBOARD_USER,
            ],
            return_address_from_token=True,
            allow_anonymous=True,
        )
    ),
    address: AddressUUID
    | None = Query(
        None,
        title="The address of the applicant, which should render their portfolio, if allowed.",
    ),
) -> Portfolio:
    if not isinstance(blockchain_instance, BlockchainMechanism):
        raise HTTPException(
            detail="Blockchain module is initializing, please try again later.",
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        )

    # * State variables.
    authorized_anonymous_user: bool = False
    authorized_org_user: bool = False
    confirmed_applicant_address: Any  # ! I don't know how to type-hint this.

    # ! Regardless of who accessed this endpoint, the portfolio is applied for both `AnonymousUsers` and `AuthenticatedApplicantUsers`.
    # # Condition
    # @o For [1] 'anonymous users', they need to fill the `address` query parameter. Otherwise return `HTTPException`.
    # @o For [2] authenticated users such as applicant, there's no need to fill the `address` query parameter, though if there is, it will get prohitibited for explicitly doing it.
    # @o For [3] authenticated users such as organization, there's a need to fill the `address` query parameter, and ensure that address is associated from the organization's association address, otherwise, it will return an `HTTPException`.

    # - [0] Resolution the condition upon various roles.

    # - Condition wherein the user is not authenticated and there's no `address` query parameter value.

    if address is None and returned_address_ref is None:
        raise HTTPException(
            detail="Failed to access portfolio as the parameter is empty or the user is not authorized to do so.",
            status_code=HTTPStatus.NOT_FOUND,
        )

    # - This condition assumes that the 'anonymous' user tries to access the portfolio of someone else with reference from the `address` query parameter.
    elif address is not None and returned_address_ref is None:
        authorized_anonymous_user = True

    # - Condition where we check that the `portfolio address is specified` but there is an authentication wherein the authorizer returns an address.
    # @o This is where we handle whether this accessor is an organization member or just an applicant.

    else:  # * Resolutes to checking the `returned_address_ref` while dynamically checking the `address` based on the scope of `APPLICANT_DASHBOARD_USER` and `ORGANIZATION_DASHBOARD_USER`.
        # elif address is not None and returned_address_ref is not None:

        # - Check the address first by getting its type.
        validate_user_type_query: Select = select([users.c.type]).where(
            users.c.unique_address == returned_address_ref
        )

        fetched_user_type: UserEntity | None = await database_instance.fetch_val(
            validate_user_type_query
        )

        if fetched_user_type is None:
            raise HTTPException(
                detail="Specified portfolio address not found.",
                status_code=HTTPStatus.NOT_FOUND,
            )

        # - Resolve user's type and check on what to do.
        if (
            fetched_user_type is UserEntity.ORGANIZATION_DASHBOARD_USER
            and returned_address_ref is not None
            and address is not None
        ):
            authorized_org_user = True  # * Allow organizations to access this portfolio, as long it belongs to their organization.

            # - Check if this organization associates within the address.
            get_org_association_address_query: Select = select(
                [users.c.association]
            ).where(users.c.unique_address == returned_address_ref)

            org_assocation_address = await database_instance.fetch_val(
                get_org_association_address_query
            )

            if org_assocation_address is None:
                raise HTTPException(
                    detail="Failed to get the association of then authenticated user. This should not be possible, please report this issue to the developers to get it fixed.",
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                )

            get_address_association_query: Select = select([users.c.association]).where(
                users.c.unique_address == address
                if address is not None
                else returned_address_ref
            )

            applicant_address_association = await database_instance.fetch_val(
                get_address_association_query
            )

            if applicant_address_association is None:
                raise HTTPException(
                    detail="Portfolio's association address does not exists. This is not possible, please report this to the developers to get it fixed.",
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                )

            if applicant_address_association != org_assocation_address:
                raise HTTPException(
                    detail="The referred portfolio address does not associate from this organization's association address. Not allowed.",
                    status_code=HTTPStatus.FORBIDDEN,
                )

            logger.info(
                "Dashboard API, Portfolio Parser | Association address for both organization and applicant is correct."
            )

        elif (
            fetched_user_type is UserEntity.APPLICANT_DASHBOARD_USER
            and returned_address_ref is not None
            and address is None
        ):

            # - By this point, the applicant was mostly validated due to `return_address_ref` and `fetched_user_type` queries.

            logger.info(
                "Dashboard API, Portfolio Parser | Applicant case already validates `unique_address` and `type`. Proceeding by doing nothing on this case ..."
            )

        else:
            raise HTTPException(
                detail="Failed to proceed due to conditions being unmet. Either an explicit address is invoked when applicant is authenticated, or does organization tried to access with context missing. Please contact the developers if you think this is a mistake.",
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

    # - [1] Check if applicant has a `APPLICANT_BASE` tx_mapping with a variety of conditions handled.

    # @o Condition for the organization accessing the portfolio.
    if authorized_anonymous_user or authorized_org_user:
        # - Check if the specified portfolio exists.
        check_portfolio_validity_query: Select = select(
            [tx_content_mappings.c.address_ref]
        ).where(
            (
                tx_content_mappings.c.address_ref
                == (address if address is not None else returned_address_ref)
            )
            & (
                tx_content_mappings.c.content_type
                == TransactionContextMappingType.APPLICANT_BASE
            )
        )

        result_portfolio_context = await database_instance.fetch_val(
            check_portfolio_validity_query
        )  # ! I cannot type hint this for some reason.

        if result_portfolio_context is None:
            raise HTTPException(
                detail="Portfolio not found.", status_code=HTTPStatus.NOT_FOUND
            )

        # - From here, handle organization members wherein the `address` should be their association.
        # @o The reason why is that, this user may have been looking from the inserter context of the organization view.

        if authorized_org_user and not authorized_anonymous_user:
            # - Get the association address of the applicant first.
            get_applicant_association_addresss_ref_query: Select = select(
                [users.c.association]
            ).where(users.c.unique_address == result_portfolio_context)

            applicant_association_ref: str | None = await database_instance.fetch_val(
                get_applicant_association_addresss_ref_query
            )

            if applicant_association_ref is None:
                raise HTTPException(
                    detail="Association address reference does not exist. Please report this to the developers as this shouldn't be possible.",
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                )

            # - Since the authorizer returns the address of the user who accessed this endpoint, get its association.
            get_org_association_query: Select = select([users.c.association]).where(
                users.c.unique_address
                == (address if address is not None else returned_address_ref)
            )

            org_association_ref: str | None = await database_instance.fetch_val(
                get_org_association_query
            )

            if org_association_ref is None:
                raise HTTPException(
                    detail="Organization doesn't have an association reference, please report this to the developers as this shouldn't be possible.",
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                )

            # # Compare the organization's association reference against the applicant's association reference.
            if org_association_ref != applicant_association_ref:
                raise HTTPException(
                    detail="The organization's association reference does not match from this applicant, access denied.",
                    status_code=HTTPStatus.CONFLICT,
                )

        confirmed_applicant_address = result_portfolio_context

        logger.info(
            f"Applicant Portfolio Access: via {'Organization' if authorized_org_user and not authorized_anonymous_user else 'Anonymous / Direct link'} context."
        )

    else:  # * Resolves to `authorized_anonymous_user` and `authorized_org_user` being None.

        # - Check if this applicant has its own transaction mapping.
        get_tx_ref_applicant_query: Select = select(
            [tx_content_mappings.c.address_ref]
        ).where(
            (
                tx_content_mappings.c.address_ref
                == (address if address is not None else returned_address_ref)
            )
            & (
                tx_content_mappings.c.content_type
                == TransactionContextMappingType.APPLICANT_BASE
            )
        )

        tx_ref_applicant = await database_instance.fetch_val(get_tx_ref_applicant_query)

        if tx_ref_applicant is None:
            raise HTTPException(
                detail=f"Applicant transaction mapping not found. This may be you are an organization and not an authorized `{UserEntity.APPLICANT_DASHBOARD_USER.name}`.",
                status_code=HTTPStatus.NOT_FOUND,
            )

        confirmed_applicant_address = tx_ref_applicant

    # - [2] Load the portfolio properties.
    # ! This will not be used for rendering the share button state.
    # ! This was fetched to better render the portfolio from its current state.
    print(confirmed_applicant_address)
    get_portfolio_properties_query: Select = select(
        [
            portfolio_settings.c.sharing_state,
            portfolio_settings.c.expose_email_state,
            portfolio_settings.c.show_files,
        ]
    ).where(portfolio_settings.c.from_user == confirmed_applicant_address)

    portfolio_properties = await database_instance.fetch_one(
        get_portfolio_properties_query
    )

    if portfolio_properties is None:
        raise HTTPException(
            detail="Portfolio settings for this applicant does not exists. Schema may be outdated.",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    # - Check if this was an anonymous and not an organization or anyone else.
    if authorized_anonymous_user and not authorized_org_user:
        if not portfolio_properties.sharing_state:
            raise HTTPException(
                detail="Anonymous access not allowed from this portoflio.",
                status_code=HTTPStatus.FORBIDDEN,
            )

    # - [3] Fetch references of the `APPLICANT_LOG` and `APPLICANT_EXTRA` on the `tx_content_mappings` table.
    # * Seperated the query because we need to display both of them distinctively.
    tx_log_applicant_refs_query: Select = tx_content_mappings.select().where(
        (tx_content_mappings.c.address_ref == confirmed_applicant_address)
        & (
            tx_content_mappings.c.content_type
            == TransactionContextMappingType.APPLICANT_LOG
        )
    )
    tx_extra_applicant_refs_query: Select = tx_content_mappings.select().where(
        (tx_content_mappings.c.address_ref == confirmed_applicant_address)
        & (
            tx_content_mappings.c.content_type
            == TransactionContextMappingType.APPLICANT_ADDITIONAL
        )
    )
    tx_log_applicant_refs: list[Mapping] = await database_instance.fetch_all(
        tx_log_applicant_refs_query
    )
    tx_extra_applicant_refs: list[Mapping] = await database_instance.fetch_all(
        tx_extra_applicant_refs_query
    )

    # - [4] Fetch those `logs` and `extras` inside the blockchain system.
    # - [5] If possible, filter the retrieved content by checking the conditions based from the portfolio settings, whether to hide a data or not.
    # @o Type-hint and container variables.
    resolved_tx_logs_container: list[PortfolioLoadedContext] = []
    resolved_tx_extra_container: list[PortfolioLoadedContext] = []

    if tx_log_applicant_refs is not None:
        for log_info in tx_log_applicant_refs:
            print(log_info)
            resolved_tx_info: PortfolioLoadedContext | None = (
                await blockchain_instance.get_content_from_chain(
                    block_index=log_info.block_no_ref,
                    tx_target=log_info.tx_ref,
                    tx_timestamp=log_info.timestamp,
                    show_file=portfolio_properties.show_files,
                )
            )

            if resolved_tx_info is not None:
                resolved_tx_logs_container.append(resolved_tx_info)

    if tx_extra_applicant_refs is not None:
        for extra_info in tx_extra_applicant_refs:
            resolved_tx_extra: PortfolioLoadedContext | None = await blockchain_instance.get_content_from_chain(
                block_index=extra_info.block_no_ref,
                tx_target=extra_info.tx_ref,
                tx_timestamp=extra_info.timestamp,
                show_file=False,  # * Default, since `extra` fields, contain nothing.
            )

            if resolved_tx_extra is not None:
                resolved_tx_extra_container.append(resolved_tx_extra)

    # - [6] Resolve other attributes that is out of `log` and `extra` fields.
    # @o Type-hints.

    get_user_basic_info_query: Select = select(
        [
            users.c.association,
            users.c.avatar,
            users.c.description,
            users.c.email,
            users.c.preferred_role,
            users.c.program,
            users.c.skills,
        ]
    ).where(users.c.unique_address == confirmed_applicant_address)
    resolved_user_basic_info = await database_instance.fetch_one(
        get_user_basic_info_query
    )
    # - [7] Sort the containers.
    resolved_tx_logs_container.sort(
        key=lambda tx_context: tx_context.context.timestamp, reverse=True
    )
    resolved_tx_extra_container.sort(
        key=lambda tx_context: tx_context.context.timestamp, reverse=True
    )

    # - [8] Return the pydantic model.
    return Portfolio(
        address=confirmed_applicant_address,
        email=resolved_user_basic_info.email
        if portfolio_properties.expose_email_state
        else None,
        program=resolved_user_basic_info.program,
        preferred_role=resolved_user_basic_info.preferred_role,
        association=resolved_user_basic_info.association,
        avatar=resolved_user_basic_info.avatar,
        description=resolved_user_basic_info.description,
        personal_skills=resolved_user_basic_info.skills,
        logs=resolved_tx_logs_container,
        extra=resolved_tx_extra_container,
    )


@dashboard_router.get(
    "/portfolio/{address_ref}/file/{file_hash}",
    tags=[DashboardAPI.APPLICANT_API],
    summary="Returns the file in raw form.",
    description="An API endpoint that returns file resources with respect to the portfolio's setting regarding file resource accessibility.",
)
async def get_portfolio_file(
    database_instance: Database = Depends(get_database_instance),
    address_ref: AddressUUID = PathParams(
        ..., title="The address reference from the portfolio."
    ),
    file_hash: HashUUID = PathParams(
        ...,
        title="The transaction hash from where the file was located, plus the actual filename.",
    ),
) -> Response:
    # # This endpoint doesn't care who you are at this point. Since address were specified, portfolio settings are going to be the dependency of the endpoint whether, to return a file or not.
    # - [1] Get the applicant address.
    validate_user_address_query: Select = select([func.count()]).where(
        users.c.unique_address == address_ref
    )

    user_address_is_valid = await database_instance.fetch_val(
        validate_user_address_query
    )

    if not user_address_is_valid:
        raise HTTPException(
            detail="Address specified not found.", status_code=HTTPStatus.NOT_FOUND
        )

    # - [2] Get portfolio settings.
    get_address_portfolio_query: Select = portfolio_settings.select().where(
        portfolio_settings.c.from_user == address_ref
    )

    address_portfolio = await database_instance.fetch_one(get_address_portfolio_query)

    if address_portfolio is None:
        raise HTTPException(
            detail="Portfolio of this address does not exist. This is not possible and is not user's fault, please contact the developer regarding this issue to get it resolved.",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    # - [3] Obligatory, check if the portfolio settings states that sharing is allowed, states to look at is `sharing_state` and `show_files`.
    if not address_portfolio.sharing_state or not address_portfolio.show_files:
        raise HTTPException(
            detail="Address specified prohibit access of the file.",
            status_code=HTTPStatus.FORBIDDEN,
        )

    # - [4] If it's allowed, check for the transaction mapping.
    try:
        splitted_file_hash_ref: list[str] = file_hash.split("_")

        # ! Divide the path parameter into the following variables.
        resolved_filename: str = splitted_file_hash_ref[0]
        resolved_tx_hash: str = splitted_file_hash_ref[1]
    except IndexError:
        raise HTTPException(
            detail="File not found.", status_code=HTTPStatus.NOT_ACCEPTABLE
        )

    # * Get the transaction mapping.
    get_tx_ref_query: Select = tx_content_mappings.select().where(
        tx_content_mappings.c.tx_ref == resolved_tx_hash
    )

    tx_ref = await database_instance.fetch_one(get_tx_ref_query)

    if tx_ref is None:
        raise HTTPException(
            detail="Content mapping does not exists. This is not possible, please contact the developers to get it resolved.",
            status_code=HTTPStatus.NOT_FOUND,
        )

    # - [5] Check if the file exists.
    final_resolve_path_to_file: Path = Path(
        f"{USER_FILES_FOLDER_NAME}/{resolved_filename}"
    )

    if not final_resolve_path_to_file.exists():
        raise HTTPException(
            detail="File was not found.", status_code=HTTPStatus.NOT_FOUND
        )

    # - [6] Decrypt the file.
    # @o Since the file has a cryptic filename, by looking at the method `insert_external_transaction` under the condition of handling the file from the `TransactionActions.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO` with an instance of a pydantic model of `ApplicantLogTransaction`, which has an actual instance of `StarletteFileUpload`, a.k.a `UploadFile` from the `file` field.
    # * We can see that we can decrypt the file.

    datetime_from_encryption: str = tx_ref.timestamp.strftime(
        FILE_PAYLOAD_TIMESTAMP_FORMAT_AS_KEY
    )
    transaction_action_ref_length: int = len(str(TransactionActions.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO.value))  # type: ignore # ! No other transaction action can be specified.

    address_truncation_for_key: int = (
        FILE_PAYLOAD_TO_ADDRESS_CHAR_LIMIT_MAX
        if transaction_action_ref_length == 2
        else FILE_PAYLOAD_TO_ADDRESS_CHAR_LIMIT_MIN
    )

    constructed_key_to_decrypt: bytes = f"{str(TransactionActions.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO.value)}{address_ref[FILE_PAYLOAD_TO_ADDRESS_START_TRUNCATION_INDEX:-address_truncation_for_key]}{datetime_from_encryption}".encode(
        "utf-8"
    )

    decrypted_file_content: bytes = b""
    async with aopen(final_resolve_path_to_file, "rb") as file_decrypter:
        file_read_content: bytes = await file_decrypter.read()

        decrypter_instance: Fernet = Fernet(
            key=urlsafe_b64encode(constructed_key_to_decrypt)
        )
        decrypted_file_content: bytes = decrypter_instance.decrypt(file_read_content)

    return Response(content=decrypted_file_content, media_type="application/pdf")


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
            == TransactionContextMappingType.APPLICANT_BASE
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

    portfolio_states = await database_instance.fetch_one(get_portfolio_state_query)

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
            detail=f"Rate-limited, expires at {portfolio_expiration}. Please comeback later.",
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
                + timedelta(minutes=PORTFOLIO_MINUTES_TO_ALLOW_STATE_CHANGE),
            )
        )

        await database_instance.execute(update_portfolio_state_query)

    except IntegrityError:
        raise HTTPException(
            detail="There was an error processing your portfolio state change, please try again.",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    return Response(status_code=HTTPStatus.ACCEPTED)
