from sqlalchemy import Boolean as Boolean, ForeignKey as ForeignKey, Integer as Integer
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.relationships import RelationshipProperty
from typing import Any

DeclarativeModel: DeclarativeMeta

class User(DeclarativeModel):
    __tablename__: str
    uaddr: Any
    first_name: Any
    last_name: Any
    username: Any
    password: Any
    email: Any
    user_type: Any
    user_activity: Any
    date_registered: Any
    date_updated: Any

class BlacklistedUsers(DeclarativeModel):
    __tablename__: str
    user: Any
    user_reference: RelationshipProperty[Any]
    reason: Any
    classified_duration: Any
    expiration: Any
    issued: Any

class Tokens(DeclarativeModel):
    __tablename__: str
    from_user: Any
    user_reference: RelationshipProperty[Any]
    token: Any
    state: Any
    expiration: Any
    issued: Any
