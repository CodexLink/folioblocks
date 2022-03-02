"""
FolioBlocks Backend Database Models (models).py

TODO:

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the gnu general public license as published by the free software foundation, either version 3 of the license, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. see the gnu general public license for more details.
you should have received a copy of the gnu general public license along with FolioBlocks. if not, see <https://www.gnu.org/licenses/>.
"""

from pydantic import BaseModel, EmailStr
from sqlalchemy import DateTime

from database.models import Associations
from ..utils.constants import Activity, UserEntity


class UserBase(BaseModel):
    uaddr: str
    association: Associations | None  # Would this work?
    user_type: UserEntity
    user_activity: Activity
    date_registered: DateTime  # We may use the datetime.datetime here.
    date_updated: DateTime


class UserCreate(UserBase):
    first_name: str
    last_name: str
    username: str
    password: str
    email: EmailStr


class User(UserCreate, UserBase):  # Not sure if this would work.
    class Config:
        orm_mode = True
