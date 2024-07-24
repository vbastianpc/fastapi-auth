from typing import Annotated
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from .database import Base


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
timestamp = Annotated[
    datetime, mapped_column(nullable=False, server_default=func.current_timestamp())
]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[timestamp]  # type: ignore[misc]

    devices = relationship("Device", back_populates="owner")


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[intpk]
    name: Mapped[str]
    mac: Mapped[str]
    ip: Mapped[str]
    last_active_datetime: Mapped[timestamp]
    notified: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner = relationship("User", back_populates="devices")
