from sqlalchemy import update, exists
from sqlalchemy.orm import Session
import bcrypt
from fastapi import HTTPException, status

from . import models, schemas


def hash_password(password: str):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode()


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        password=plain_password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8"),
    )


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).one_or_none()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).one_or_none()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).one_or_none()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def authenticate_user(db: Session, username: str, password: str) -> models.User | None:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, current_user: schemas.User, user: schemas.UserBase):
    stmt = (
        update(models.User)
        .where(models.User.id == current_user.id)
        .values(**user.model_dump())
    )
    db.execute(stmt)
    db.commit()


def get_devices(db: Session, skip: int = 0, limit: int = 100) -> list[models.Device]:
    return db.query(models.Device).offset(skip).limit(limit).all()


def get_devices_by_user_id(
    db: Session, user_id: int | None = None, skip: int = 0, limit: int = 100
) -> list[models.Device]:
    return (
        db.query(models.Device)
        .where(models.User.id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_own_devices(
    db: Session, user: schemas.User, skip: int = 0, limit: int = 100
) -> list[models.Device]:
    return (
        db.query(models.Device)
        .where(models.Device.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_device(db: Session, device: schemas.DeviceCreate, user_id: int):
    db_device = models.Device(**device.model_dump(), user_id=user_id)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def update_device(
    db: Session, user: schemas.User, device: schemas.DeviceCreate, device_id: int
) -> models.Device:
    cond = (models.Device.id == device_id, models.Device.user_id == user.id)
    if db.query(exists().where(*cond)).scalar():
        stmt = update(models.Device).where(*cond).values(**device.model_dump())
        db.execute(stmt)
        db.commit()
        return db.query(models.Device).filter(*cond).one()
    elif db.query(exists().where(cond[0])).scalar():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You are not the owner of device_id={device_id}.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"device_id={device_id} does not exists.",
        )
