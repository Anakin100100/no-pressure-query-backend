import sys

sys.path.append("../no-pressure-query-backend")

from main import app
from fastapi.testclient import TestClient
import models
import uuid


def create_user() -> models.User:
    email = f"{uuid.uuid4()}@gmail.com".replace("-", "")
    password = "test_password"
    client = TestClient(app)
    r = client.post(
        "/users/",
        json={"email": email, "password": password, "first_name": "test_first_name", "last_name": "test_last_name"},
    )
    response = r.json()
    user = models.User(**response)
    return user


def get_token(user: models.User) -> str:
    client = TestClient(app)
    r = client.post(
        "/api/token", data={"username": user.email, "password": "test_password"}
    )
    response = r.json()
    return response["access_token"]
