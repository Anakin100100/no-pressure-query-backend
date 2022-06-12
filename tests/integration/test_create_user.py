import sys

sys.path.append("../no-pressure-query-backend")

from main import app
from fastapi.testclient import TestClient
from services import user_service
import uuid

from utils.database_utils import SessionLocal
from datetime import datetime
import models.user_model as user_model


def test_create_user_with_correct_data():
    db = SessionLocal()
    client = TestClient(app)
    email = f"email_{datetime.now().strftime('%H%M%S%f')}@gmail.com"
    response = client.post(
        "/users/",
        json={"email": email, "password": "test_password", "first_name": "test", "last_name": "test"},
    )
    user = user_service.get_user(db=db, user_id=response.json()["id"])
    assert user.first_name == "test"
    assert user.last_name == "test"
    assert user.email == email
    db.close()
    assert response.status_code == 200
    assert response.json()["email"] == email
    assert response.json()["id"] >= 0
    assert response.json()["first_name"] == "test"
    assert response.json()["last_name"] == "test"


def test_create_user_with_incorrect_password():
    client = TestClient(app)
    email = f"email_{datetime.now().strftime('%H:%M:%S:%f')}"
    response = client.post(
        "/users/",
        json={"email": email, "password": "", "first_name": "test", "last_name": "test"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Password must be at least 8 characters"


def test_create_user_with_incorrect_email():
    client = TestClient(app)
    email = f"email{datetime.now().strftime('%H:%M:%S:%f')}_wrong_email"
    response = client.post(
        "/users/",
        json={"email": email, "password": "test_password", "first_name": "test", "last_name": "test"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email must be a valid email address"

def test_create_user_with_invalid_first_name():
    client = TestClient(app)
    email =  f"{uuid.uuid4()}@gmail.com".replace("-", "")
    response = client.post(
        "/users/",
        json={"email": email, "password": "test_password", "first_name": "", "last_name": "test"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "First name must be at least 2 characters"

def test_create_user_with_invalid_last_name():
    client = TestClient(app)
    email =  f"{uuid.uuid4()}@gmail.com".replace("-", "")
    response = client.post(
        "/users/",
        json={"email": email, "password": "test_password", "first_name": "test", "last_name": ""},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Last name must be at least 2 characters"
