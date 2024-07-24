from .. import crud, schemas
from ..dependencies import CommonDB, DependsActiveUser

from fastapi import APIRouter, status, HTTPException

router = APIRouter()


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: CommonDB):
    db_user = crud.get_user_by_email(db, user.email) or crud.get_user_by_username(
        db, user.username
    )
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered"
        )
    return crud.create_user(db=db, user=user)


@router.put("/me", status_code=status.HTTP_200_OK)
def update_user(
    db: CommonDB, current_user: DependsActiveUser, update_user: schemas.UserBase
):
    crud.update_user(db, current_user, update_user)


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: DependsActiveUser):
    return current_user
