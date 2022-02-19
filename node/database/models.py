"""
FolioBlocks Backend Database Models (models).py

TODO:

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the gnu general public license as published by the free software foundation, either version 3 of the license, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. see the gnu general public license for more details.
you should have received a copy of the gnu general public license along with FolioBlocks. if not, see <https://www.gnu.org/licenses/>.
"""

if __name__ == "__main__":
    pass

from enum import Enum
from typing import Any
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from utils.constants import (
    Activity,
    BlacklistDuration,
    GroupType,
    TokenType,
    UserType,
    SQLEnum,
)
from main import logger

DeclarativeModel: DeclarativeMeta = declarative_base()

# TODO: We might wanna create a key where it combines all of the certain fields
# ! And when it was inserted for reset password, it show resulted to that!

"""
    Notes:
    - SQLAlchemy doesn't use enum.Enum as their Enum.
    - Therefore, I have to subclass sqlalchemy.Enum as SQLEnum and subclass it to all classified enums that will be used in the database.
    - Their use-case on non-database is possible since their `dir()` shows that we can access items just like what we have in enum.Enum.

"""


class Association(DeclarativeModel):
    __tablename__ = "associations"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    group = Column(GroupType, default=GroupType.ORGANIZATION, nullable=False)
    date_added = Column(DateTime, default=datetime.now())

    associates = relationship("User", back_populates="association")


class User(DeclarativeModel):
    __tablename__ = "users"

    uaddr = Column(
        String(38), default=lambda: ("fl:" + uuid4().hex), unique=True, primary_key=True
    )
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    association = relationship(
        Association, back_populates="associates"
    )  # TODO: I'm not sure if ths would work.

    username = Column(String(24), nullable=False)
    password = Column(String(64), nullable=False)  # TODO: Should be hashed.

    email = Column(String(128), unique=True, nullable=False)

    user_type = Column(UserType, default=UserType.AS_USER)
    user_activity = Column(Activity, default=Activity.OFFLINE)

    date_registered = Column(DateTime, default=datetime.now())
    date_updated = Column(DateTime, onupdate=datetime.now())


class BlacklistedUser(DeclarativeModel):
    __tablename__ = "blacklisted_users"

    id = Column(Integer, primary_key=True)
    user = Column(String(38), ForeignKey("users.uaddr"), nullable=False)
    user_ref = relationship(User, foreign_keys=[user])
    reason = Column(Text, nullable=False)
    classified_duration = Column(BlacklistDuration, default=BlacklistDuration.WARN_1)
    expiration = Column(DateTime, nullable=True)
    issued = Column(DateTime, default=datetime.now())


class Tokens(DeclarativeModel):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    from_user = Column(String(38), ForeignKey("users.uaddr"), nullable=False)
    user_ref = relationship(User, foreign_keys=[from_user])
    token = Column(
        Text, nullable=False
    )  # TODO: I don't know how many characters are there in JWT token.
    state = Column(TokenType, default=TokenType.RECENTLY_CREATED, nullable=False)
    expiration = Column(DateTime, nullable=True)
    issued = Column(DateTime, default=datetime.now())


# TODO: Need checker function for asserting if the user is a Node Type.
# ! This is just a preparation for the blockchain system approach.
class QueueTasks(DeclarativeModel):
    __tablename__ = "queued_tasks"

    id = Column(Integer, primary_key=True)


DeclarativeModel.metadata.create_all(bind=sql_engine)
