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

from datetime import datetime, timedelta
from http import HTTPStatus
from sqlite3 import IntegrityError

from blueprint.models import auth_codes
from blueprint.schemas import GenerateAuthInput
from core.constants import BaseAPI, NodeAPI, RequestPayloadContext, UserEntity
from core.email import EmailService, get_email_instance
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
                f"Inferred role is not allowed! There should only be one {UserEntity.MASTER_NODE_USER}.",
                [each_enum.value for each_enum in UserEntity],
            ),
            status_code=HTTPStatus.FORBIDDEN,
        )

    if auth_instance.verify(x_passcode):
        generated_token: str = generate_auth_token()

        await email_instance.send(
            content=f"<html><body><h1>Auth Code as Folioblock's Archival Miner Node!</h1><p>Thank you for taking interest! To continue, please enter the authentication code for the registration. <b>DO NOT SHARE THIS TO ANYONE.</b></p><br><br><h4>Auth Code: {generated_token}<b></b></h4><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
            subject="Register Auth Code for Archival Miner Node Registration @ Folioblocks",
            to=payload.email,
        )

        try:
            insert_generated_token_query: Insert = auth_codes.insert().values(
                code=generated_token,
                account_type=payload.role,
                to_email=payload.email,
                expiration=datetime.now() + timedelta(days=2),
            )

            await db_instance.execute(insert_generated_token_query)

        except IntegrityError as e:
            raise HTTPException(
                detail=f"The email you entered already has an `auth_token`! If you think this is a mistake, please contact the developers. | Additional Info: {e}",
                status_code=HTTPStatus.FORBIDDEN,
            )

        return {"detail": "Invocation of the email for registration were successful."}

    raise HTTPException(
        detail="Invalid passcode.", status_code=HTTPStatus.NOT_ACCEPTABLE
    )
