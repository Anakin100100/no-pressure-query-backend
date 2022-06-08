from fastapi import Depends, FastAPI, HTTPException
import fastapi
from sqlalchemy.orm import Session
import auth
from database import get_db

import crud, models, schemas
from database import engine
import fastapi.security as security

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "1283818238128381823"


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
def read_user(user: schemas.User = Depends(auth.get_current_user)):
    return user


@app.post("/api/token")
async def generate_token(
    form_data: security.OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = await auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return fastapi.HTTPException(status_code=401, detail="Invalid credentials")

    return await auth.create_token(user)
