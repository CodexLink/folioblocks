"""
Admin API — Exclusive endpoints for allowing actions that requires authorization from higher-ups to allow users for use of the platform.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""


"""
# Further Notice
This endpoint should be used for generating users as a organization or as a node. When running this endpoint, ensure that you look for

"""

from datetime import datetime, timedelta
from http import HTTPStatus

from blueprint.models import auth_codes
from blueprint.schemas import GenerateAuthInput
from core.constants import BaseAPI, NodeAPI, UserEntity
from core.email import EmailService, get_email_instance
from databases import Database
from email_validator import EmailNotValidError, EmailSyntaxError, validate_email
from fastapi import APIRouter, Header, HTTPException

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
) -> None:
    from core.dependencies import (
        PasscodeTOTP,
        generate_auth_token,
        get_db_instance,
        get_totp_instance,
    )

    auth_instance: PasscodeTOTP | None = get_totp_instance()
    email_instance: EmailService | None = get_email_instance()
    db_instance: Database | None = get_db_instance()

    print(
        auth_instance is None
        or email_instance is None
        or email_instance.is_connected
        or db_instance is None
    )

    if (
        auth_instance is None
        or email_instance is None
        or email_instance.is_connected
        or db_instance is None
    ):
        raise HTTPException(
            detail="Instance is not yet ready. This means, the system is not yet ready to take special requests. Try again later.",
            status_code=HTTPStatus.ACCEPTED,
        )

    if payload.role_to_infer == UserEntity.MASTER_NODE_USER:
        raise HTTPException(
            detail=(
                f"Inferred role is not allowed! There should only be one {UserEntity.MASTER_NODE_USER}.",
                [each_enum.value for each_enum in UserEntity],
            ),
            status_code=HTTPStatus.FORBIDDEN,
        )

    if payload.email is not None:
        try:
            validate_email(payload.email)
        except (EmailNotValidError, EmailSyntaxError) as e:
            raise HTTPException(
                status_code=HTTPStatus.NOT_ACCEPTABLE,
                detail=f"Input for the E-mail address is invalid! | Info: {e}",
            )
    else:
        raise HTTPException(
            detail=f" E-mail address is not supplied.",
            status_code=HTTPStatus.NO_CONTENT,
        )

    if auth_instance.verify(x_passcode):
        generated_token: str = generate_auth_token()

        insert_generated_token_stmt = auth_codes.insert().values(
            code=generated_token,
            account_type=payload.role_to_infer,
            to_email=payload.email,
            expiration=datetime.now() + timedelta(days=2),
        )  # # LOOKOUT FOR THE ERROR HERE.

        await db_instance.execute(insert_generated_token_stmt)
        await email_instance.send(
            content=f"<html><body><h1>Auth Code as Folioblock's Archival Miner Node!</h1><p>Thank you for taking interest! To continue, please enter the authentication code for the registration. <b>DO NOT SHARE THIS TO ANYONE.</b></p><br><br><h4>Auth Code: {generated_token}<b></b></h4><br><a href='https://github.com/CodexLink/folioblocks'>Learn the development progression on Github.</a></body></html>",
            subject="Register Auth Code for Archival Miner Node Registration @ Folioblocks",
            to=payload.email,
        )
        return

    raise HTTPException(
        detail="Invalid passcode.", status_code=HTTPStatus.NOT_ACCEPTABLE
    )
