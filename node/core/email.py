"""
Async Email Handler (email.py) | Contains async-compatible class that can be invoked within the core of the folioblocks (main.py) and its components.

Please note that their logging reference is seperate but their formatting should be consistent.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""


from asyncio import sleep
from asyncio.windows_events import INFINITE
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import Logger, getLogger
from os import environ as env

from aiosmtplib import (
    SMTP,
    SMTPAuthenticationError,
    SMTPConnectError,
    SMTPServerDisconnected,
)
from pydantic import EmailStr
from utils.exceptions import InsufficientCredentials

from core.constants import (
    ASYNC_TARGET_LOOP,
    AUTH_ENV_FILE_NAME,
    DEFAULT_SMTP_CONNECT_MAX_RETRIES,
    DEFAULT_SMTP_PORT,
    DEFAULT_SMTP_URL,
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
        username: CredentialContext,
        password: CredentialContext,
        max_retries: int = DEFAULT_SMTP_CONNECT_MAX_RETRIES,
    ) -> None:

        self.url = URLAddress(url)
        self.port = IPPort(port)
        self.username: CredentialContext = CredentialContext(username)
        self.password: CredentialContext = CredentialContext(password)
        self.max_retries = max_retries

    async def connect(self) -> None:
        try:
            retries_count: int = 1  # - Protect the constant for iteration purposes.

            while retries_count <= self.max_retries:
                try:
                    logger.info(
                        f"Attempt #{retries_count} | Attempting to connect AT email service ({self.url}) at port {self.port}."
                    )

                    self._email_service: SMTP = SMTP(
                        hostname=self.url,
                        port=self.port,
                        username=self.username,
                        password=self.password,
                        use_tls=True,
                    )

                    await self._email_service.connect()
                    logger.info("SMTP email service connected ...")

                    await self._email_service.ehlo()
                    logger.debug(
                        f"SMTP send EHLO packets to {self.url} to initiate service ..."
                    )
                    logger.info(f"SMTP email service acknowledged and ready.")
                    return

                except (
                    SMTPAuthenticationError,
                    SMTPConnectError,
                    SMTPServerDisconnected,
                ) as e:
                    # When service is not possible, then data senders will automatically return and log that it is not possible due to is_connected: False.
                    logger.critical(
                        f"Failed to connect at email services. | Additional Info: {e}."
                    )

                    if retries_count + 1 <= self.max_retries:
                        logger.warning(
                            f"Attempting to reconnect email services ... | Attempt #{retries_count + 1} out of {self.max_retries}"
                        )

                    retries_count += 1
                    continue

            from utils.processors import (
                unconventional_terminate,
            )  # @o Circulate imports occur when implemented on the top.

            unconventional_terminate(
                message="Attempt count for retrying to connect to email services has been depleted. Email service failed at connecting due to potentially false credentials or service is not responding. Please check your `.env` file or your internet connection and try again. Do CTRL+BREAK to encrypt the file back and check your environment.",
                early=True,
            )
            await sleep(INFINITE)
        except InsufficientCredentials as e:
            logger.warning(
                f"There is no credentials due to non-existent environment file. ({AUTH_ENV_FILE_NAME}) | Additional Info: {e}"
            )

    async def send(
        self,
        *,
        content: str,
        subject: str,
        to: EmailStr,
    ) -> None:  # TODO: This should require a pydantic class for the message??????
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
        await self._email_service.send_message(message_instance)

        logger.info(
            f"Message has been sent. (Subject: {subject} | From: {message_instance['From']} | To: {to[:5]} ...)"
        )

    def close(self) -> None:
        return self._email_service.close()

    @property
    def is_connected(self) -> bool:
        return self._email_service.is_connected


"""
# Kudos to Helios for the logic: https://stackoverflow.com/questions/63189935/is-it-possible-to-use-the-same-object-in-multiple-files

* By the time I code this, I can't comprehend basic logic anymore because I'm tired. But I do have knowledge about global variables, it's just that for this case we are actually sharing this instance across the whole system.

"""
email_service: EmailService | None = None


def get_email_instance() -> EmailService | None:
    global email_service

    if email_service is None:
        address: str | None = env.get("EMAIL_SERVER_ADDRESS", None)
        pwd: str | None = env.get("EMAIL_SERVER_PWD", None)

        logger.debug("Initializing or returning emails service instance ...")

        if address is not None and pwd is not None:
            email_service = EmailService(
                url=URLAddress(DEFAULT_SMTP_URL),
                port=IPPort(DEFAULT_SMTP_PORT),
                username=CredentialContext(address),
                password=CredentialContext(pwd),
            )

            return None

        else:
            raise InsufficientCredentials(
                EmailService, ["address (EMAIL_ADDRESS)", "pwd (EMAIL_PWD)"]
            )

    else:
        return email_service
