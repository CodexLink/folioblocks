"""
Admin API — Exclusive endpoints for allowing actions that requires authentication from higher-ups to allow users for use of the platform.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""


"""
# Further Notice
This endpoint should be used for generating users as a associate/organization or as a node. When running this endpoint, ensure that you look for

"""

from asyncio import gather
from datetime import datetime, timedelta
from http import HTTPStatus
from logging import Logger, getLogger
from sqlite3 import IntegrityError

from blueprint.models import auth_codes, users
from blueprint.schemas import GenerateAuthInput
from core.constants import (
    ASYNC_TARGET_LOOP,
    BaseAPI,
    NodeAPI,
    RequestPayloadContext,
    UserEntity,
)
from databases import Database
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import func, select
from sqlalchemy.sql.expression import Insert, Select, Update
from core.dependencies import EnsureAuthorized
from utils.email import EmailService, get_email_instance
from utils.processors import save_database_state_to_volume_storage

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

admin_router = APIRouter(
    prefix="/admin",
    tags=[BaseAPI.ADMIN.value],
)


@admin_router.post(
    "/generate_auth",
    tags=[NodeAPI.GENERAL_NODE_API.value],
    summary="Generates token for the registration of the user as a node or as a normal user.",
    description="An exclusive API endpoint that generates token for users to register. This should be triggered by an admin.",
    status_code=HTTPStatus.ACCEPTED,
)
async def generate_auth_token_for_entities(
    *,
    payload: GenerateAuthInput,
    x_passcode: str = Header(
        ...,
        description="The special passcode that allows the generation of `auth_code`.",
    ),
    authorizer_address=Depends(
        EnsureAuthorized(
            _as=[
                UserEntity.MASTER_NODE_USER,
                UserEntity.ORGANIZATION_DASHBOARD_USER,
            ],
            return_address_from_token=True,
        )
    ),
) -> RequestPayloadContext:

    # ! We cannot append these dependencies from the function due to circular import dependencies.
    from core.dependencies import (
        PasscodeTOTP,
        generate_auth_token,
        get_database_instance,
        get_totp_instance,
    )

    database_instance: Database = (
        get_database_instance()
    )  # - Prioritize this instance before any other.

    # - Get necessary information from this address.
    authorizer_address_info_query: Select = select(
        [users.c.association, users.c.type, users.c.date_registered]
    ).where(
        (users.c.unique_address == authorizer_address)
        & (
            (users.c.type == UserEntity.MASTER_NODE_USER)
            | (users.c.type == UserEntity.ORGANIZATION_DASHBOARD_USER)
        )
    )

    authorizer_address_info = await database_instance.fetch_one(
        authorizer_address_info_query
    )

    if authorizer_address_info is None:
        raise HTTPException(
            detail="User attributes were not found. This is not possible due to being able to be authenticated in the first-layer. Please report this problem from the administrator.",
            status_code=HTTPStatus.NOT_FOUND,
        )

    # - Only handle for the organization, since it has multiple association entries.
    # ! For the case of the master node, we don't need to do some extra validation.
    if authorizer_address_info.type is UserEntity.ORGANIZATION_DASHBOARD_USER:  # type: ignore
        # - Filter out these users by getting the their address and the date.
        validate_date_registration_from_associates_query: Select = select(
            [func.count()]
        ).where(
            (users.c.date_registered < authorizer_address_info.date_registered)
            & (users.c.association == authorizer_address_info.association)
        )  # type: ignore

        # - Compare this address against others from their address.
        covered_by_date_associates = await database_instance.fetch_val(
            validate_date_registration_from_associates_query
        )

        if covered_by_date_associates:
            raise HTTPException(
                detail="You are not authorized to create the authentication code. Please ask the creator of the organization from the system.",
                status_code=HTTPStatus.UNAUTHORIZED,
            )

    auth_instance: PasscodeTOTP | None = get_totp_instance()
    email_instance: EmailService | None = get_email_instance()
    require_new_token: bool = False  # * A switch for allowing a token to be renewed by sending a new email with a new code.

    if auth_instance is None or email_instance is None or database_instance is None:
        raise HTTPException(
            detail="Instance is not yet ready. This means, the system is not yet ready to take special requests. Try again later.",
            status_code=HTTPStatus.ACCEPTED,
        )

    if payload.role is UserEntity.MASTER_NODE_USER:
        raise HTTPException(
            detail=(
                f"Role not allowed! There should only be one {UserEntity.MASTER_NODE_USER.value}.",
            ),
            status_code=HTTPStatus.FORBIDDEN,
        )

    elif payload.role is UserEntity.STUDENT_DASHBOARD_USER:
        raise HTTPException(
            detail=(
                f"Requesting an authentication code through this role ('{UserEntity.STUDENT_DASHBOARD_USER.value}') is not allowed.",
            ),
            status_code=HTTPStatus.FORBIDDEN,
        )

    else:
        if auth_instance.verify(x_passcode):
            generated_token: str = generate_auth_token()

            try:
                # - First check, check if this user was already an existing user via checking the 'users' table.
                check_existing_user_via_users_query: Select = select(
                    [func.count()]
                ).where(users.c.email == payload.email)

                user_email_exists_via_users = await database_instance.fetch_val(
                    check_existing_user_via_users_query
                )

                if user_email_exists_via_users:
                    raise HTTPException(
                        detail="Cannot create authentication code due to the user already existing from the system! Please check and get their login credentials checked.",
                        status_code=HTTPStatus.FORBIDDEN,
                    )

                # - Last step, check the given email from the authentication code table ('auth_codes').
                check_existing_user_via_auth_token_query: Select = select(
                    [func.count(), auth_codes.c.expiration]
                ).where(auth_codes.c.to_email == payload.email)

                user_context_from_auth_codes = await database_instance.fetch_one(
                    check_existing_user_via_auth_token_query
                )

                if (
                    user_context_from_auth_codes.count
                    and datetime.now() < user_context_from_auth_codes.expiration
                ):
                    raise HTTPException(
                        detail="The email associated from this request already has an authentication code!",
                        status_code=HTTPStatus.FORBIDDEN,
                    )
                elif (
                    user_context_from_auth_codes.count
                    and datetime.now() >= user_context_from_auth_codes.expiration
                ):
                    require_new_token = True
                    logger.warning(
                        "An expired authentication code has been detected from one of the queried email, renewal will be processed. Check for the log regarding email services sending a renewed token."
                    )

                # - Handle new token to be renewal or literally a new one.
                if require_new_token:
                    update_expired_token_query: Update = (
                        auth_codes.update()
                        .where(auth_codes.c.to_email == payload.email)
                        .values(token=generated_token)
                    )
                    await gather(
                        database_instance.execute(update_expired_token_query),
                        save_database_state_to_volume_storage(),
                    )

                else:
                    insert_generated_token_query: Insert = auth_codes.insert().values(
                        code=generated_token,
                        account_type=payload.role,
                        to_email=payload.email,
                        expiration=datetime.now() + timedelta(days=2),
                    )
                    await gather(
                        database_instance.execute(insert_generated_token_query),
                        save_database_state_to_volume_storage(),
                    )

                # ! Do not change this, regardless of the token's existence and its state.
                # - I have no time for that.
                await email_instance.send(
                    content=f"<html><body><h1>Auth Code for the Folioblock's {payload.role.value}!</h1><p>Thank you for taking part in our ecosystem! To register, please enter the following auth code. Remember, <b>do not share this code to anyone.</b></p><h4>Auth Code: {generated_token}<b></b></h4><br><p>Didn't know who sent this? Please consult your representives of your organization / institution regarding this matter.</p><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
                    subject=f"Auth Code for Registration as a {payload.role.value} at Folioblocks",
                    to=payload.email,
                )

            except IntegrityError as e:
                raise HTTPException(
                    detail=f"Cannot provide anymore authentication token to the requested user. Please report the following error: {e}",
                    status_code=HTTPStatus.FORBIDDEN,
                )

            logger.info(
                "Authentication code has been sent from one the requested users. Check preceeding logs for more information."
            )

            return {
                "detail": f"Invocation of the email for a registration as a '{payload.role.value}' were successful. Advise to check their email."
            }

        else:
            raise HTTPException(
                detail="Invalid TOTP passcode.", status_code=HTTPStatus.NOT_ACCEPTABLE
            )
