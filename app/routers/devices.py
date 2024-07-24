from .. import crud, schemas
from ..dependencies import CommonDB, DependsActiveUser

from fastapi import APIRouter, status

router = APIRouter()


@router.post("/", response_model=schemas.Device)
async def create_device_for_user(
    device: schemas.DeviceCreate,
    current_user: DependsActiveUser,
    db: CommonDB,
):
    return crud.create_device(db=db, device=device, user_id=current_user.id)


@router.put("/{device_id}", status_code=status.HTTP_200_OK)
def update_device(
    device: schemas.DeviceCreate,
    current_user: DependsActiveUser,
    db: CommonDB,
    device_id: int,
):
    return crud.update_device(db, current_user, device, device_id)


@router.get("/", response_model=list[schemas.Device])
async def read_own_devices(
    db: CommonDB,
    current_user: DependsActiveUser,
    skip: int = 0,
    limit: int = 100,
):
    return crud.get_own_devices(db, current_user, skip, limit)
