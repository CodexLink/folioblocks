"""
FolioBlocks Backend Database Models (models).py

TODO:

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the gnu general public license as published by the free software foundation, either version 3 of the license, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. see the gnu general public license for more details.
you should have received a copy of the gnu general public license along with FolioBlocks. if not, see <https://www.gnu.org/licenses/>.
"""

from enum import Enum
from typing import Any
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm.relationships import RelationshipProperty
from node.utils.constants import Activity, BlacklistDuration, TokenType, UserType

DeclarativeModel: DeclarativeMeta = declarative_base()

# TODO: We might wanna create a key where it combines all of the certain fields
# ! And when it was inserted for reset password, it show resulted to that!


class User(DeclarativeModel):
    __tablename__ = "users"

    uaddr = Column(
        String(38), default=lambda: ("fl:" + uuid4().hex), unique=True, primary_key=True
    )
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)

    username = Column(String(24), nullable=False)
    password = Column(String(56), nullable=False)  # TODO: Should be hashed.

    email = Column(String(128), unique=True, nullable=False)

    user_type = Column(UserType.AS_USER, Enum(UserType), nullable=False)
    user_activity = Column(Activity.OFFLINE, Enum(Activity), nullable=False)

    date_registered = Column(DateTime, default=datetime.now())
    date_updated = Column(DateTime, onupdate=datetime.now())


class BlacklistedUsers(DeclarativeModel):
    __tablename__ = "blacklisted_users"

    user = Column(String(38), nullable=False)
    user_reference: RelationshipProperty[Any] = relationship(User, foreign_keys=[user])
    reason = Column(Text, nullable=False)
    classified_duration = Column(BlacklistDuration.WARN_1, Enum(BlacklistDuration), nullable=False)
    expiration = Column(DateTime, nullable=True)
    issued = Column(DateTime, default=datetime.now())


class Tokens(DeclarativeModel):
    __tablename__ = "tokens"

    from_user = Column(String(38), nullable=False)
    user_reference: RelationshipProperty[Any] = relationship(User, foreign_keys=[from_user])
    token = Column(Text, nullable=False) # TODO: I don't know how many characters are there in JWT token.
    state = Column(TokenType.RECENTLY_CREATED, Enum(TokenType), nullable=False)
    expiration = Column(DateTime, nullable=True)
    issued = Column(DateTime, default=datetime.now())
