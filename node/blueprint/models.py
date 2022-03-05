"""
FolioBlocks Backend Database Models (models).py

TODO:

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the gnu general public license as published by the free software foundation, either version 3 of the license, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. see the gnu general public license for more details.
you should have received a copy of the gnu general public license along with FolioBlocks. if not, see <https://www.gnu.org/licenses/>.
"""

if __name__ == "__main__":  # TODO: ???
    pass


from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    func,
)

from sqlalchemy.orm import relationship
from core.constants import UserEntity
from core.constants import (
    UserActivityState,
    BlacklistDuration,
    GroupType,
    TokenStatus,
)
from sqlalchemy import Enum as SQLEnum

# TODO: We might wanna create a key where it combines all of the certain fields
# ! And when it was inserted for reset password, it should resulted to that!

"""
    Notes:
    - SQLAlchemy doesn't use enum.Enum as their Enum.
    - Therefore, I have to subclass sqlalchemy.Enum as SQLEnum and subclass it to all classified enums that will be used in the database.
    - Their use-case on non-database is possible since their `dir()` shows that we can access items just like what we have in enum.Enum.
    - # !! Creation of tables is in the core.py.
    - # ! Unsupported: Running engine.all(engine=engine) is not possible as it is blocking when using sqlite+aiosqlite as protocol.
    - The use case of DeclarativeModel (declarative_base()) is not possible and is not supported by encode/databases. An example of instantiating
    - sqlalchemy.Metadata() is only possible. Though even we are going to use encode/databases with SQLAlchemy ORM, then I'm not sure why they didn't support it.
"""

# DeclarativeModel: DeclarativeMeta = declarative_base()

model_metadata: MetaData = MetaData()

associations = Table(
    "associations",
    model_metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(64), nullable=False),
    Column(
        "group",
        SQLEnum(GroupType),
        server_default=GroupType.ORGANIZATION.name,
        nullable=False,
    ),
    Column("date_added", DateTime, default=func.now())
    # TODO
)
associations.associates = relationship("users", back_populates="association")  # type: ignore
users = Table(
    "users",
    model_metadata,
    Column(
        "unique_address",
        String(35),
        nullable=False,
        primary_key=True,
        autoincrement=False,
    ),
    Column("first_name", String(32), nullable=True),
    Column("last_name", String(32), nullable=True),
    # TODO: I'm not sure if ths would work.
    # association =
    Column("username", String(24), unique=True, nullable=False),
    Column("password", String(64), nullable=False),  # ! Expects hashed.
    Column("email", String(128), unique=True, nullable=False),
    Column(
        "user_type", SQLEnum(UserEntity), server_default=UserEntity.DASHBOARD_USER.name
    ),
    Column(
        "user_activity",
        SQLEnum(UserActivityState),
        server_default=UserActivityState.OFFLINE.name,
    ),
    Column("date_registered", DateTime, server_default=func.now()),
)

users.association = relationship(associations, back_populates="associates")  # type: ignore

blacklisted_users = Table(
    "blacklisted_users",
    model_metadata,
    Column("id", Integer, primary_key=True),
    Column("user", String(38), ForeignKey("users.unique_address"), nullable=False),
    Column("reason", Text, nullable=False),
    Column(
        "duration",
        SQLEnum(BlacklistDuration),
        server_default=BlacklistDuration.WARN_1.name,
    ),
    Column("expiration", DateTime, nullable=True),
    Column("issued_on", DateTime, server_default=func.now()),
)

blacklisted_users.user_ref = relationship(users, foreign_keys=["user"])  # type: ignore

tokens = Table(
    "tokens",
    model_metadata,
    Column("id", Integer, primary_key=True),
    Column("from_user", String(38), ForeignKey("users.unique_address"), nullable=False),
    Column("token", Text, nullable=False),
    Column(
        "state",
        SQLEnum(TokenStatus),
        server_default=TokenStatus.RECENTLY_CREATED.name,
        nullable=False,
    ),
    Column("expiration", DateTime, nullable=True),
    Column("issued", DateTime, server_default=func.now()),
)

tokens.user_ref = relationship(users, foreign_keys="from_user")  # type: ignore
# TODO: Need checker function for asserting if the user is a Node Type.
# ! This is just a preparation for the blockchain system approach.
# class QueueTasks(DeclarativeModel):
#     __tablename__ = "queued_tasks"

#     id = Column(Integer, primary_key=True)
