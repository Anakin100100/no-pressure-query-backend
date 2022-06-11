import sys

sys.path.append("../no-pressure-query-backend")

from main import app
from fastapi.testclient import TestClient

import testing_utils


def test_read_correctly_created_user():
    client = TestClient(app)
    user = testing_utils.create_user()
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == user.email
    assert response.json()["id"] == user.id


def test_non_existing_user():
    client = TestClient(app)
    # Wrong id
    response = client.get(f"/users/{-1230320}")
    assert response.status_code == 400
    assert response.json()["detail"] == "User does not exist"
