"""
Admin API — Exclusive endpoints for allowing actions that requires authorization from higher-ups to allow users for use of the platform.

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
from sqlite3 import IntegrityError

from blueprint.models import auth_codes, users
from blueprint.schemas import GenerateAuthInput
from core.constants import BaseAPI, NodeAPI, RequestPayloadContext, UserEntity
from databases import Database
from fastapi import APIRouter, Header, HTTPException
from sqlalchemy import func, select
from sqlalchemy.sql.expression import Insert, Select, Update
from .core.constants import ASYNC_TARGET_LOOP
from utils.email import EmailService, get_email_instance
from utils.processors import save_database_state_to_volume_storage
from logging import getLogger, Logger

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

admin_router = APIRouter(
    prefix="/admin",
    tags=[BaseAPI.ADMIN.value],
)


@admin_router.post(
    "/generate_auth",
    tags=[NodeAPI.GENERAL_NODE_API.value],
    summary="Generates token for registration of user as node or as a normal user.",
    description="An exclusive API endpoint that generates token for users to register. This should be triggered by an admin.",
    status_code=HTTPStatus.ACCEPTED,
)
async def generate_auth_token_for_other_nodes(
    *,
    payload: GenerateAuthInput,
    x_passcode: str = Header(
        ...,
        description="The special passcode that allows the generation of `auth_code`.",
    ),
) -> RequestPayloadContext:

    # ! We cannot append these dependencies from the function due to circular import dependencies.
    from core.dependencies import (
        PasscodeTOTP,
        generate_auth_token,
        get_database_instance,
        get_totp_instance,
    )

    auth_instance: PasscodeTOTP | None = get_totp_instance()
    email_instance: EmailService | None = get_email_instance()
    database_instance: Database | None = get_database_instance()
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
                f"Requesting an auth code through this role ({UserEntity.STUDENT_DASHBOARD_USER.value}) is not allowed.",
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

                # - Last check the given email from the authentication code table ('auth_codes').
                check_existing_user_via_auth_token_query: Select = select(
                    [func.count(), auth_codes.c.expiration]
                ).where(auth_codes.c.to_email == payload.email)

                user_context_from_auth_codes = await database_instance.fetch_val(
                    check_existing_user_via_auth_token_query
                )

                if (
                    user_context_from_auth_codes
                    and datetime.now() < user_context_from_auth_codes.expiration
                ):
                    raise HTTPException(
                        detail="The email associated from this request already has an authentication code!",
                        status_code=HTTPStatus.FORBIDDEN,
                    )
                elif (
                    user_context_from_auth_codes
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
                "detail": f"Invocation of the email for registration as a {payload.role.value} were successful."
            }

        else:
            raise HTTPException(
                detail="Invalid TOTP passcode.", status_code=HTTPStatus.NOT_ACCEPTABLE
            )
