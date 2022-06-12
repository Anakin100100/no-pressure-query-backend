import sys

sys.path.append("../no-pressure-query-backend")

from main import app
from fastapi.testclient import TestClient

import utils.testing_utils as testing_utils
import services.user_service as user_service
from utils.database_utils import SessionLocal

def test_delete_non_existant_user():
    client = TestClient(app)
    r = client.get(
        "/users/delete_user", data={"user_id": -200}
    )
    response = r.json()
    assert r.status_code == 400
    assert response["detail"] == "user with this id does not exist"

def test_delete_existing_user():
    client = TestClient(app)
    user = testing_utils.create_user()
    r = client.get(
        "/users/delete_user", data={"user_id": user.id}
    )
    assert r.status_code == 200
    db = SessionLocal()
    assert user_service.get_user(db=db, user_id=user.id) is None
    db.close()
