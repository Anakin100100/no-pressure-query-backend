from collections import UserList
from operator import mod
from pyexpat import model
from signal import raise_signal
from fastapi import Depends, FastAPI, HTTPException
import fastapi
import jwt
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine
import fastapi.security as security

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "1283818238128381823"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def authenticate_user(email: str, password: str, db: Session):
    user = crud.get_user_by_email(db, email=email)
    if not user:
        return False

    if not user.verify_password(password=password):
        return False

    return user


async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")


# Dependency
async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2schema)
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(detail="Invalid token", status_code=401)

    return schemas.User.from_orm(user)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/me", response_model=schemas.User)
def read_user(user: schemas.User = Depends(get_current_user)):
    return user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/api/token")
async def generate_token(
    form_data: security.OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return fastapi.HTTPException(status_code=401, detail="Invalid credentials")

    return await create_token(user)
