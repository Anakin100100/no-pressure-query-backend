from main import app
from fastapi.testclient import TestClient

import utils.testing_utils as testing_utils
import services.user_service as user_service
from utils.database_utils import SessionLocal

def test_update_user_first_name_correctly_authenticated():
    client = TestClient(app)
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    #TODO refactor into a fixture
    new_first_name = "NewFirstName"   
    r = client.get(
        f"/users/update_user_first_name/{user.id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        params={
            "new_first_name": new_first_name
        }
    )
    assert r.status_code == 200
    assert r.json()["message"] == "user has been successfully updated"
    db = SessionLocal()
    assert user_service.get_user(db=db, user_id=user.id).first_name == new_first_name
    db.close()

def test_update_user_first_name_incorrectlly_authenticated():
    client = TestClient(app)
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    r = client.get(
        f"/users/update_user_first_name/{user.id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        params={
            "new_first_name": ""
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "First name must be at least 2 characters"
    db = SessionLocal()
    assert user_service.get_user(db=db, user_id=user.id).first_name == user.first_name
    db.close()

def test_update_user_first_name_correctly_unauthenticatd():
    client = TestClient(app)
    user = testing_utils.create_user()
    new_first_name = "NewFirstName"
    r = client.get(
        f"/users/update_user_first_name/{user.id}",
        headers={
            "Authorization": f"Bearer invalid_token"
        },
        params={
            "new_first_name": new_first_name
        }
    )
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid token"
    db = SessionLocal()
    assert user_service.get_user(db=db, user_id=user.id).first_name == user.first_name
    db.close()

def test_update_another_users_first_name_authenticated():
    client = TestClient(app)
    user_1 = testing_utils.create_user()
    user_2 = testing_utils.create_user()
    token = testing_utils.get_token(user_2)
    r = client.get(
        f"/users/update_user_first_name/{user_1.id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        params={
            "new_first_name":"SomeValidFirstName"
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "You can only update your own account"
    db = SessionLocal()
    assert user_service.get_user(db=db, user_id=user_1.id).first_name == user_1.first_name
    db.close()
