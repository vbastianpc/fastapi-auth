from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, AfterValidator
from pydantic.networks import IPvAnyAddress
from pydantic_extra_types.mac_address import MacAddress

from .custom_validation import CheckPwd


class DeviceCreate(BaseModel):
    name: str
    mac: MacAddress
    ip: Annotated[IPvAnyAddress, AfterValidator(lambda x: str(x))]


class Device(DeviceCreate):
    id: int
    user_id: int
    last_active_datetime: datetime
    notified: bool
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: CheckPwd


class User(UserBase):
    id: int
    is_active: bool
    devices: list[Device] = []
    model_config = ConfigDict(from_attributes=True)


##


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    scopes: list[str]


class UserInDB(User):
    hashed_password: str


class ScopesInfo(BaseModel):
    ME: str = Field(default="Read and modify my own", frozen=True)
    ADMIN: str = Field(default="Read and modify all database", frozen=True)


class Scopes(BaseModel):
    ME: str = Field(default="ME", frozen=True)
    ADMIN: str = Field(default="ADMIN", frozen=True)


SCOPES = Scopes()
