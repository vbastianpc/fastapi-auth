from typing import Annotated

from .. import crud, schemas, auth
from ..dependencies import CommonDB

from fastapi import APIRouter, HTTPException, status, Security


DependsAdminUser = Annotated[
    schemas.User,
    Security(auth.get_current_active_user, scopes=schemas.SCOPES.model_dump()),
]

router = APIRouter(
    dependencies=[Security(auth.get_current_active_user, scopes=[schemas.SCOPES.ADMIN])]
)


@router.get("/users", response_model=list[schemas.User])
def read_users(db: CommonDB, skip: int = 0, limit: int = 100):
    """Get all users"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/devices", response_model=list[schemas.Device])
def read_devices(db: CommonDB, skip: int = 0, limit: int = 100):
    return crud.get_devices(db, skip, limit)


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: CommonDB):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.get("/{user_id}/devices", response_model=list[schemas.Device])
def read_devices_from_user(db: CommonDB, user_id: int, skip: int = 0, limit: int = 100):
    return crud.get_devices_by_user_id(db, user_id, skip=skip, limit=limit)
