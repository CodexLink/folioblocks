"""
Async Email Handler (email.py) | Contains async-compatible class that can be invoked within the core of the folioblocks (main.py) and its components.

Please note that their logging reference is seperate but their formatting should be consistent.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""


from asyncio import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import Logger, getLogger
from os import environ as env

from aiosmtplib import (
    SMTP,
    SMTPConnectTimeoutError,
    SMTPException,
    SMTPReadTimeoutError,
    SMTPRecipientRefused,
    SMTPRecipientsRefused,
    SMTPResponseException,
    SMTPTimeoutError,
)
from pydantic import EmailStr
from utils.processors import unconventional_terminate

from core.constants import (
    ASYNC_TARGET_LOOP,
    AUTH_ENV_FILE_NAME,
    DEFAULT_SMTP_ATTEMPT_MAX_RETRIES,
    DEFAULT_SMTP_PORT,
    DEFAULT_SMTP_TIMEOUT_CONNECTION,
    DEFAULT_SMTP_URL,
    INFINITE_TIMER,
    CredentialContext,
    IPPort,
    URLAddress,
)

logger: Logger = getLogger(ASYNC_TARGET_LOOP)


class EmailService:
    def __init__(
        self,
        *,
        url: URLAddress,
        port: IPPort,
        username: CredentialContext | None,
        password: CredentialContext | None,
        max_retries: int = DEFAULT_SMTP_ATTEMPT_MAX_RETRIES,
    ) -> None:

        # - Validate if there's crdentials.
        if any(
            credential is None or not isinstance(credential, str)
            for credential in [username, password]
        ):
            unconventional_terminate(
                message="Email instance can't be instantiated due to possibly non-existent credentials. The following are required: [address (EMAIL_ADDRESS), pwd (EMAIL_PWD)]."
            )
        else:
            self.username: CredentialContext = CredentialContext(username)  # type: ignore # - Statement already checked from `if` clause.
            self.password: CredentialContext = CredentialContext(password)  # type: ignore # - Statement already checked from `if` clause.

        self.connection_validated: bool = False  # ! A switch that we can use to tick whether the first connection from the email service would fail or not. When email fails on initialization fail with `unconventional_terminate` method.
        self.max_retries = max_retries
        self.url = URLAddress(url)
        self.port = IPPort(port)

        self._email_service: SMTP = SMTP(
            hostname=self.url,
            port=self.port,
            username=self.username,
            password=self.password,
            use_tls=True,
        )

    async def connect(self) -> None:
        from utils.processors import (
            unconventional_terminate,
        )  # @o Circulate imports occur when implemented on the top of the file.

        retries_count: int = 1  # - Protect the constant for iteration purposes.

        if not self.connection_validated:
            logger.warning(
                "Email service establishing first-time connection from this instance. It may fail or otherwise."
            )

        while retries_count <= self.max_retries:
            try:
                logger.info(
                    f"Attempt #{retries_count} | Attempting to connect AT email service ({self.url}) at port {self.port}."
                )

                await self._email_service.connect(
                    timeout=DEFAULT_SMTP_TIMEOUT_CONNECTION
                )
                logger.info("SMTP email service connected ...")

                await self._email_service.ehlo()
                logger.debug(
                    f"SMTP send EHLO packets to {self.url} to initiate service ..."
                )

                self.connection_validated = True
                logger.info(f"SMTP email service acknowledged and ready.")
                return

            except SMTPException as e:
                # When service is not possible, then data senders will automatically return and log that it is not possible due to is_connected: False.
                logger.critical(
                    f"Failed to connect at email services. | Additional Info: {e}."
                )

                if not self.connection_validated:
                    unconventional_terminate(
                        message=f"Failed on email instance, refer to the previous log and please check the credentials in  `{AUTH_ENV_FILE_NAME}` file or your internet connection, then try again.",
                        early=True,
                    )
                    await sleep(INFINITE_TIMER)

                if retries_count + 1 <= self.max_retries:
                    logger.warning(
                        f"Attempting to reconnect email services ... | Attempt #{retries_count + 1} out of {self.max_retries}"
                    )

                retries_count += 1
                continue

        unconventional_terminate(
            message=f"Attempt count for retrying to connect to email services has been depleted. Email service failed at connecting due to potentially false credentials or service is not responding. Do CTRL+BREAK to encrypt the file back and check your environment.",
        )
        await sleep(INFINITE_TIMER)

    async def send(
        self,
        *,
        content: str,
        subject: str,
        to: EmailStr,
    ) -> None:
        # @o There should be an extra argument, but I will keep it this way, for now.
        for _ in range(0, self.max_retries):
            if not self._email_service.is_connected:
                logger.warning(
                    "Connection to the email service is not available or the connetion is dead, re-connecting ..."
                )

                await self.connect()

            message_instance = MIMEMultipart("alternative")

            message_instance["From"] = env.get("EMAIL_SERVER_ADDRESS")
            message_instance["To"] = to
            message_instance["Subject"] = subject

            message_context: MIMEText = MIMEText(content, "html", "utf-8")

            message_instance.attach(message_context)

            try:
                await self._email_service.send_message(message_instance)

                logger.info(
                    f"Message has been sent. (Subject: {subject} | From: {message_instance['From']} | To: {to[:5]} ...)"
                )
                break

            except (
                SMTPRecipientRefused,
                SMTPRecipientsRefused,
                SMTPResponseException,
            ) as e:
                logger.critical(
                    f"Cannot send email due to error in the process. Info: {e} | From: {message_instance['From']} | To: {to[:5]}"
                )
                break

            except (
                SMTPTimeoutError,
                SMTPReadTimeoutError,
                SMTPConnectTimeoutError,
            ) as e:
                logger.warning(
                    f"Cannot send email due to disruption of service. Re-attempting... | Info: {e}"
                )
                continue

    def close(self) -> None:
        return self._email_service.close()

    @property
    def is_connected(self) -> bool:
        return self._email_service.is_connected


"""
# Kudos to Helios for the logic: https://stackoverflow.com/questions/63189935/is-it-possible-to-use-the-same-object-in-multiple-files

* By the time I code this, I can't comprehend basic logic anymore because I'm tired. But I do have knowledge about global variables, it's just that for this case we are actually sharing this instance across the whole system.

"""
email_service: EmailService


def get_email_instance() -> EmailService:
    global email_service

    try:
        globals()[
            "email_service"
        ]  # - Only attempt to call this, otherwise just return the reference that is declared outside from this function.

    except KeyError:
        logger.debug("Initializing or returning emails service instance ...")

        email_service = EmailService(
            url=URLAddress(DEFAULT_SMTP_URL),
            port=IPPort(DEFAULT_SMTP_PORT),
            username=CredentialContext(env.get("EMAIL_SERVER_ADDRESS", "")),
            password=CredentialContext(env.get("EMAIL_SERVER_PWD", "")),
            max_retries=DEFAULT_SMTP_ATTEMPT_MAX_RETRIES,
        )

    return email_service
