from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends

from .database import get_db
from . import schemas, auth

CommonDB = Annotated[Session, Depends(get_db)]
DependsActiveUser = Annotated[schemas.User, Depends(auth.get_current_active_user)]
