from fastapi import Depends, FastAPI, HTTPException
import fastapi
from pydantic import HttpUrl
from sqlalchemy.orm import Session
import auth_utils
from database import get_db
import re

import crud, models, schemas
from database import engine
import fastapi.security as security

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "1283818238128381823"

email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if len(user.password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters"
        )
    if not re.match(email_regex, user.email):
        raise HTTPException(
            status_code=400, detail="Email must be a valid email address"
        )
    db_created_user = crud.create_user(db=db, user=user)
    return schemas.User.from_orm(db_created_user)


@app.get("/users/me", response_model=schemas.User)
async def read_user_return_token(
    user: schemas.User = Depends(auth_utils.get_current_user),
):
    return user


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    return schemas.User.from_orm(db_user)


@app.post("/api/token")
async def generate_token(
    form_data: security.OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = await auth_utils.authenticate_user(
        form_data.username, form_data.password, db
    )
    if not user:
        return fastapi.HTTPException(status_code=401, detail="Invalid credentials")

    return await auth_utils.create_token(user)


@app.get("/api")
async def read_root():
    return {"message": "Another message"}
