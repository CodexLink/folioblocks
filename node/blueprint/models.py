"""
FolioBlocks Backend Database Models (models).py

TODO:

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the gnu general public license as published by the free software foundation, either version 3 of the license, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. see the gnu general public license for more details.
you should have received a copy of the gnu general public license along with FolioBlocks. if not, see <https://www.gnu.org/licenses/>.
"""

from typing import Final

from core.constants import (
    AssociatedNodeStatus,
    ConsensusNegotiationStatus,
    OrganizationType,
    TokenStatus,
    TransactionContextMappingType,
    UserActivityState,
    UserEntity,
)
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, MetaData, String, Table, Text, false, func
from sqlalchemy.orm import relationship

"""
    @o Notes:
    - SQLAlchemy doesn't use enum.Enum as their Enum.
    - Therefore, I have to subclass sqlalchemy.Enum as `SQLEnum` and subclass it to all classified enums that will be used in the database.
    - Their use-case on non-database is possible since their `dir()` shows that we can access items just like what we have in enum.Enum.

    - # !! Creation of tables is in the core.py.
    - # ! Unsupported: Running engine.all(engine=engine) is not possible as it is blocking when using sqlite+aiosqlite as protocol.
    - The use case of DeclarativeModel (declarative_base()) is not possible and is not supported by encode/databases.
    - An example of instantiating `sqlalchemy.Metadata()` is only possible. Though even we are going to use encode/databases with SQLAlchemy ORM, then I'm not sure why they didn't support it.
"""

model_metadata: MetaData = MetaData()

associations = Table(
    "associations",
    model_metadata,
    Column("id", Integer, primary_key=True),
    Column("address", String(38), nullable=False, unique=True),
    Column("name", String(64), nullable=False),
    Column(
        "group",
        SQLEnum(OrganizationType),
        server_default=OrganizationType.ORGANIZATION.name,
        nullable=False,
    ),
    Column("date_added", DateTime, default=func.now()),
)


file_signatures = Table(
    "file_signatures",
    model_metadata,
    Column("id", Integer, primary_key=True),
    Column("filename", String(64), nullable=False, unique=True),
    Column("hash_signature", Text, nullable=False, unique=True),
)

users = Table(
    "users",
    model_metadata,
    Column(
        "unique_address",
        String(32),
        nullable=False,
        primary_key=True,
        autoincrement=False,
    ),
    Column("avatar", Text, nullable=True, unique=False),
    Column("description", Text, nullable=True, unique=False),
    Column("skills", Text, nullable=True, unique=False),
    Column("program", Text, nullable=True, unique=False),
    Column("first_name", String(32), nullable=True),
    Column("last_name", String(32), nullable=True),
    Column("preferred_role", String(32), nullable=True),
    Column(
        "association", ForeignKey("associations.address"), nullable=True, unique=False
    ),
    Column("username", String(24), nullable=False, unique=True),
    Column("password", String(64), nullable=False),
    Column("email", String(128), nullable=False, unique=True),
    Column("type", SQLEnum(UserEntity), nullable=False, unique=False),
    Column(
        "activity",
        SQLEnum(UserActivityState),
        server_default=UserActivityState.OFFLINE.name,
    ),
    Column("date_registered", DateTime, nullable=False),
)

users.association_ref = relationship(associations, foreign_keys="association")  # type: ignore

# ! The following element will be used throughout to refer to the user.
user_addr_ref: Final[str] = "users.unique_address"

associated_nodes = Table(
    "associated_nodes",
    model_metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "user_address",
        ForeignKey(user_addr_ref),
        nullable=False,
        unique=False,
    ),
    Column("certificate", Text, unique=False, nullable=False),
    Column(
        "status",
        SQLEnum(AssociatedNodeStatus),
        nullable=True,
        server_default=AssociatedNodeStatus.CURRENTLY_AVAILABLE.name,
    ),
    Column("source_address", String(15), nullable=False, unique=False),
    Column("source_port", Integer, nullable=False, unique=False),
    Column("consensus_sleep_expiration", DateTime, nullable=True, unique=False),
)

associated_nodes.user_ref = relationship(  # type: ignore
    associated_nodes, foreign_keys="user_address"
)

auth_codes = Table(
    "auth_codes",
    model_metadata,
    Column("id", Integer, primary_key=True),
    Column("generated_by", ForeignKey(user_addr_ref), nullable=True),
    Column(
        "code", String(64), nullable=False, unique=True
    ),  # @o 64 characters because token_hex-based restriction is not enforced, meaning its resultant length is unpredictable for some reason.
    Column("account_type", SQLEnum(UserEntity), nullable=False),
    Column("to_email", String(128), nullable=False, unique=True),
    Column("is_used", Boolean, server_default=false()),
    Column("expiration", DateTime, server_default=func.now()),
)

auth_codes.user_ref = relationship(users, foreign_keys="generated_by")  # type: ignore

consensus_negotiation = Table(
    "consensus_negotiation",
    model_metadata,
    Column("id", Integer, primary_key=True),
    Column("block_no_ref", Integer, nullable=False, unique=True),
    Column("consensus_negotiation_id", String(11), nullable=False, unique=True),
    Column("peer_address", ForeignKey(user_addr_ref), nullable=False, unique=False),
    Column(
        "status",
        SQLEnum(ConsensusNegotiationStatus),
        nullable=False,
        server_default=ConsensusNegotiationStatus.ON_PROGRESS.name,
        unique=False,
    ),
    Column(
        "date_negotiation",
        DateTime,
        nullable=False,
        server_default=func.now(),
        unique=False,
    ),
)

consensus_negotiation.peer_address_ref = relationship(users, foreign_keys="peer_address")  # type: ignore

portfolio_settings = Table(
    "portfolio_settings",
    model_metadata,
    Column("id", Integer, primary_key=True),
    Column("from_user", ForeignKey(user_addr_ref), nullable=False),
    Column("sharing_state", Boolean, server_default=false()),
    Column("expose_email_state", Boolean, server_default=false()),
    Column("show_files", Boolean, server_default=false()),
    Column("datetime_to_allowed_changes", DateTime, server_default=func.now()),
)

portfolio_settings.user_ref = relationship(users, foreign_keys="from_user")  # type: ignore

tokens = Table(
    "tokens",
    model_metadata,
    Column("id", Integer, primary_key=True),
    Column("from_user", String(32), ForeignKey(user_addr_ref), nullable=False),
    Column(
        "token", Text, nullable=False
    ),  # # For some reason, SQL doesn't like anything more than 128 when asserting its UNIQUE.
    Column(
        "state",
        SQLEnum(TokenStatus),
        server_default=TokenStatus.CREATED_FOR_USE.name,
        nullable=False,
    ),
    Column("expiration", DateTime, nullable=True),
    Column("issued", DateTime, server_default=func.now()),
)

tokens.user_ref = relationship(users, foreign_keys="from_user")  # type: ignore

"""
# Regarding Transaction Content Mapping

@o This model does not adapt semantically on the approach of ManyToOne. (Many addresses, there can only be one unique transaction)

- `address_ref` - Refers to the user itself.
- `block_no_ref` - Secondary reference from where the master node will look at.
- `tx_ref` - The actual transaction where the content will be resolved.

! Note
* For multiple transactions, previous `tx_ref` referring to the same `address_ref` with respect to the `content_type` will be only be displayed as reference, not the actual content. This situation only applies to fields for `log` and `extra` under Applicant and Organization scope.
* Replacement of the existing data (Base structure) for the Applicant and Organization scope will be prohibited when there's an existing entry of the following (under Enum `TransactionContextMappingType`): APPLICANT_INFO, and SCHOOL_INFO.
* Updating any entries unspecified from the statement #2, does not resort to updating existing data, but should rather log the actual state instead.
"""

tx_content_mappings = Table(
    "tx_content_mappings",
    model_metadata,
    Column("id", Integer, primary_key=True),
    Column("address_ref", ForeignKey(user_addr_ref), nullable=False, unique=False),
    Column("block_no_ref", Integer, nullable=False, unique=False),
    Column("tx_ref", String(64), nullable=False, unique=False),
    Column(
        "content_type",
        SQLEnum(TransactionContextMappingType),
        nullable=False,
        unique=False,
    ),
    Column("timestamp", DateTime, nullable=False),
)

tx_content_mappings.address_user_ref = relationship(users, foreign_keys="address_ref")  # type: ignore
