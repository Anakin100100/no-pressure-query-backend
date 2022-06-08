import sys

sys.path.append("../no-pressure-query-backend")

from main import app
from fastapi.testclient import TestClient
import models
import uuid


def create_user():
    email = f"test_email{uuid.uuid4()}"
    password = "test_password"
    client = TestClient(app)
    r = client.post(
        "/users/",
        json={"email": email, "password": password},
    )
    response = r.json()
    print(response)
    user = models.User(**response)
    return user


def get_token(user: models.User):
    client = TestClient(app)
    r = client.post(
        "/api/token", data={"username": user.email, "password": "test_password"}
    )
    response = r.json()
    return response["access_token"]
