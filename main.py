from fastapi import Depends, FastAPI, HTTPException
import fastapi
from sqlalchemy.orm import Session
import utils.auth_utils as auth_utils
from utils.database_utils import get_db
import re
from fastapi.middleware.cors import CORSMiddleware

import schemas.user_schema as user_schema
from utils.database_utils import Base
import services.user_service as user_service
import services.survey_service as survey_service
from utils.database_utils import engine
import fastapi.security as security
import schemas.survey_schema as survey_schema
import models.survey_model as survey_model

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/token")

email_regex = "^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$"


@app.post("/api/users/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
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
    if len(user.first_name) < 3:
        raise HTTPException(
            status_code=400, detail="First name must be at least 2 characters"
        )
    if len(user.last_name) < 3:
        raise HTTPException(
            status_code=400, detail="Last name must be at least 2 characters"
        )
    db_created_user = user_service.create_user(db=db, user=user)
    return user_schema.User.from_orm(db_created_user)


@app.get("/users/me", response_model=user_schema.User)
async def read_user_return_token(
    user: user_schema.User = Depends(auth_utils.get_current_user),
):
    return user


@app.get("/users/{user_id}", response_model=user_schema.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    return user_schema.User.from_orm(db_user)


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

@app.get("/users/delete_user/{delete_user_id}")
async def delete_user(
    delete_user_id: int,
    user: user_schema.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    if user.id != delete_user_id:
        raise HTTPException(status_code=400, detail="You can only delete your own account")
    user_service.delete_user(db=db, user_id=delete_user_id)
    return {
        "message": "user has been successfully deleted"
    }

@app.get("/users/update_user_email/{update_user_id}")
async def update_user_email(
    new_email: str,
    update_user_id: int,
    user: user_schema.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    if user.id != update_user_id:
        raise HTTPException(status_code=400, detail="You can only update your own account")
    user_service.update_user_email(db=db, user_id=update_user_id, new_email=new_email)
    return {
        "message": "user has been successfully updated"
    }

@app.get("/users/update_user_first_name/{update_user_id}")
async def update_user_first_name(
    new_first_name: str,
    update_user_id: int,
    user: user_schema.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    if user.id != update_user_id:
        raise HTTPException(status_code=400, detail="You can only update your own account")
    user_service.update_first_name(db=db, user_id=update_user_id, new_first_name=new_first_name)
    return {
        "message": "user has been successfully updated"
    }

@app.get("/users/update_user_last_name/{update_user_id}")
async def update_user_first_name(
    new_last_name: str,
    update_user_id: int,
    user: user_schema.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    if user.id != update_user_id:
        raise HTTPException(status_code=400, detail="You can only update your own account")
    user_service.update_last_name(db=db, user_id=update_user_id, new_last_name=new_last_name)
    return {
        "message": "user has been successfully updated"
    }

@app.get("/surveys/create", response_model=survey_schema.Survey)
async def create_survey(survey: survey_schema.SurveyCreate, user=Depends(auth_utils.get_current_user), db=Depends(get_db)):
    return survey_schema.Survey.from_orm(survey_service.create_survey(user=user, db=db, survey=survey))
