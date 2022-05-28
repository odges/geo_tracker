from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text as as_text
from geoalchemy2 import Geometry
from core.orm import Base


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(Unicode(255), nullable=False)


class GeoSessionRecord(Base):
    __tablename__ = "session_record"

    id = Column(
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        server_default=as_text("uuid_generate_v4()"),
    )
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    datetime_start_at = Column(DateTime(), default=func.now())


class LocationPoint(Base):
    __tablename__ = "location"

    id = Column(
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        server_default=as_text("uuid_generate_v4()"),
    )
    point = Column(Geometry("POINT"), nullable=False)
    datetime_at = Column(DateTime(), default=func.now(), nullable=False)
    session_id = Column(
        UUID(as_uuid=True), ForeignKey("session_record.id"), nullable=False
    )
