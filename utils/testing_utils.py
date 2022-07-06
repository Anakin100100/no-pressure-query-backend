import sys

from schemas import user_schema

sys.path.append("../no-pressure-query-backend")

from main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import schemas.survey_schema as survey_schema
import services.survey_service as survey_service

import uuid
import models.user_model as user_model


    
def create_user(email: str = None, password: str = "test_password") -> user_model.User:
    if email is None:
        email = f"{uuid.uuid4()}@gmail.com".replace("-", "")
    client = TestClient(app)
    r = client.post(
        "/api/users/",
        json={"email": email, "password": password, "first_name": "test_first_name", "last_name": "test_last_name"},
    )
    response = r.json()
    user = user_model.User(**response)
    return user


def get_token(user: user_model.User, password: str = "test_password") -> str:
    client = TestClient(app)
    r = client.post(
        "/api/token", data={"username": user.email, "password": password}
    )
    response = r.json()
    return response["access_token"]


def create_survey(user: user_schema.User, db: Session, name: str="Test"):
    survey = survey_schema.SurveyCreate(name=name)
    return survey_service.create_survey(user=user, db=db, survey=survey)
