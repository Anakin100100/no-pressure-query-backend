from services import user_service
from utils import testing_utils
from utils.database_utils import SessionLocal
from schemas.user_schema import UserCreate

def test_get_user():
    user = testing_utils.create_user()
    db = SessionLocal()
    user_from_db = user_service.get_user(db, user.id)
    db.close()
    assert user_from_db.id == user.id
    assert user_from_db.email == user.email
    assert user_from_db.first_name == user.first_name
    assert user_from_db.last_name == user.last_name

def test_get_user_by_email():
    user = testing_utils.create_user()
    db = SessionLocal()
    user_from_db = user_service.get_user_by_email(db, user.email)
    db.close()
    assert user_from_db.id == user.id
    assert user_from_db.email == user.email
    assert user_from_db.first_name == user.first_name
    assert user_from_db.last_name == user.last_name


def test_create_user():
    user_data = UserCreate(email="testemail@gmail.com", password="testpassword", first_name="testfirstname", last_name="testlastname")
    db = SessionLocal()
    user_from_db = user_service.create_user(db, user_data)
    db.close()
    assert user_from_db.email == user_data.email
    assert user_from_db.first_name == user_data.first_name
    assert user_from_db.last_name == user_data.last_name
    assert user_from_db.hashed_password != user_data.password
