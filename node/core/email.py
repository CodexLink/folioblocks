"""
Async Email Handler (email.py) | Contains async-compatible class that can be invoked within the core of the folioblocks (main.py) and its components.

Please note that their logging reference is seperate but their formatting should be consistent.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""


import asyncio
from aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailHandler:
	def __ainit__(self) -> None:
		pass

	def __init__(self) -> None:  # Do not make a user
		pass

	async def send(content, from, to): # This should require a pydantic class for the message.
		pass

	async def init(self) -> None:
		pass


	def close() -> None:
		pass
    # @classmethod

    pass
