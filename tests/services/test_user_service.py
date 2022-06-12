import pytest
from fastapi import HTTPException
from services import user_service
from utils import testing_utils
from utils.database_utils import SessionLocal
from schemas.user_schema import UserCreate
from models import user_model

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

def test_delete_user():
    user = testing_utils.create_user()
    db = SessionLocal()
    num_users_before_delete = db.query(user_model.User).count()
    user_service.delete_user(db=db, user_id=user.id)
    num_users_after_delete = db.query(user_model.User).count()
    db.close()
    assert num_users_after_delete - num_users_before_delete == -1
    assert user_service.get_user(db=db, user_id=user.id) == None 
    assert user_service.get_user_by_email(db=db, email=user.email) == None

def test_delete_non_existant_user():
    db = SessionLocal()
    num_users_before_delete = db.query(user_model.User).count()
    with pytest.raises(HTTPException):
        #User with this id cannot exist in the db
        user_service.delete_user(db=db, user_id=-200)
    num_users_after_delete = db.query(user_model.User).count()
    assert num_users_after_delete - num_users_before_delete == 0
    db.close()
