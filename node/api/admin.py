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

from blueprint.models import auth_codes
from blueprint.schemas import GenerateAuthInput
from core.constants import BaseAPI, NodeAPI, RequestPayloadContext, UserEntity
from utils.processors import save_database_state_to_volume_storage
from utils.email import EmailService, get_email_instance
from databases import Database
from fastapi import APIRouter, Header, HTTPException
from sqlalchemy.sql.expression import Insert

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
    db_instance: Database | None = get_database_instance()

    if auth_instance is None or email_instance is None or db_instance is None:
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
                insert_generated_token_query: Insert = auth_codes.insert().values(
                    code=generated_token,
                    account_type=payload.role,
                    to_email=payload.email,
                    expiration=datetime.now() + timedelta(days=2),
                )

                await gather(
                    db_instance.execute(insert_generated_token_query),
                    save_database_state_to_volume_storage(),
                )

                await email_instance.send(
                    content=f"<html><body><h1>Auth Code for the Folioblock's {payload.role.value}!</h1><p>Thank you for taking part in our ecosystem! To register, please enter the following auth code. Remember, <b>do not share this code to anyone.</b></p><h4>Auth Code: {generated_token}<b></b></h4><br><p>Didn't know who sent this? Please consult your representives of your organization / institution regarding this matter.</p><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
                    subject=f"Auth Code for Registration as a {payload.role.value} at Folioblocks",
                    to=payload.email,
                )

            except IntegrityError:
                raise HTTPException(
                    detail=f"Cannot provide anymore `auth_token` to this user due to an existing not expired token. Please check their email and try again.",
                    status_code=HTTPStatus.FORBIDDEN,
                )

            return {
                "detail": f"Invocation of the email for registration as a {payload.role.value} were successful."
            }

        else:
            raise HTTPException(
                detail="Invalid TOTP passcode.", status_code=HTTPStatus.NOT_ACCEPTABLE
            )
