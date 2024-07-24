from datetime import timedelta
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from . import crud, models, schemas, auth
from .database import engine
from .dependencies import CommonDB
from .routers import users, devices, admin


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(devices.router, prefix="/devices", tags=["devices"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])


@app.get("/")
async def basti() -> RedirectResponse:
    return RedirectResponse("/docs")


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: CommonDB,
) -> schemas.Token:
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
