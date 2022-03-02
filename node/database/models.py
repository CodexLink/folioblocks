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
from utils.constants import SQLUserEntity
from utils.constants import (
    Activity,
    BlacklistDuration,
    GroupType,
    TokenType,
)

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
    Column("group", GroupType, default=GroupType.ORGANIZATION, nullable=False),
    Column("date_added", DateTime, default=func.now())
    # TODO
    # "associates" = relationship("User", back_populates="association")
)

users = Table(
    "users",
    model_metadata,
    Column(
        "uaddr",
        String(64),
        nullable=False,
        primary_key=True,
        autoincrement=False,
    ),
    Column("first_name", String(32), nullable=True),
    Column("last_name", String(32), nullable=True),
    # TODO: I'm not sure if ths would work.
    # association = relationship(
    #     Association, back_populates="associates"
    # )
    Column("username", String(24), unique=True, nullable=False),
    Column("password", String(64), nullable=False),  # ! Expects hashed.
    Column("email", String(128), unique=True, nullable=False),
    Column("user_type", SQLUserEntity, server_default=SQLUserEntity.DASHBOARD),
    Column("user_activity", Activity, server_default=Activity.OFFLINE),
    Column("date_registered", DateTime, server_default=func.now()),
)

blacklisted_users = Table(
    "blacklisted_users",
    model_metadata,
    Column("id", Integer, primary_key=True),
    Column("user", String(38), ForeignKey("users.uaddr"), nullable=False),
    # relationship("user_ref", User, foreign_keys=[user]),
    Column("reason", Text, nullable=False),
    Column("duration", BlacklistDuration, server_default=BlacklistDuration.WARN_1),
    Column("expiration", DateTime, nullable=True),
    Column("issued_on", DateTime, server_default=func.now()),
)

tokens = Table(
    "tokens",
    model_metadata,
    Column("id", Integer, primary_key=True),
    # from_user = Column(String(38), ForeignKey("users.uaddr"), nullable=False)
    # user_ref = relationship(User, foreign_keys=[from_user])
    Column(
        "token", Text, nullable=False
    ),  # TODO: I don't know how many characters are there in JWT token.
    Column(
        "state", TokenType, server_default=TokenType.RECENTLY_CREATED, nullable=False
    ),
    Column("expiration", DateTime, nullable=True),
    Column("issued", DateTime, server_default=func.now()),
)

# TODO: Need checker function for asserting if the user is a Node Type.
# ! This is just a preparation for the blockchain system approach.
# class QueueTasks(DeclarativeModel):
#     __tablename__ = "queued_tasks"

#     id = Column(Integer, primary_key=True)
