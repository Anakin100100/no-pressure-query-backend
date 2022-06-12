import email
import pytest
from fastapi import HTTPException
from services import user_service
from utils import testing_utils
from utils.database_utils import SessionLocal
from schemas.user_schema import UserCreate
from models import user_model
import uuid

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

def test_update_user_email_with_correct_unique_email():
    db = SessionLocal()
    user = testing_utils.create_user()
    old_email = user.email
    correct_new_email =  f"{uuid.uuid4()}@gmail.com".replace("-", "")
    user_service.update_user_email(db=db, user_id=user.id, new_email=correct_new_email)
    assert user_service.get_user(db=db, user_id=user.id).email == correct_new_email
    assert user_service.get_user_by_email(db=db, email=old_email) is None
    db.close()

def test_update_user_email_with_incorrecct_email():
    db = SessionLocal()
    user = testing_utils.create_user()
    incorrect_new_email =  "email_that_schould_not_be_accepted"
    with pytest.raises(HTTPException) as exception:
        user_service.update_user_email(db=db, user_id=user.id, new_email=incorrect_new_email)
        assert exception.detail == "incorrect email"
    #email should remain unchanged
    assert user_service.get_user(db=db, user_id=user.id).email == user.email
    assert user_service.get_user_by_email(db=db, email=user.email) is not None
    db.close()

def test_updateuser_email_with_existing_email():
    db = SessionLocal()
    user_1 = testing_utils.create_user()
    user_2 = testing_utils.create_user()
    with pytest.raises(HTTPException) as exception:
        user_service.update_user_email(db=db, user_id=user_1.id, new_email=user_2.email)
        assert exception.detail == "user with this email already exists"
    assert user_service.get_user(db=db, user_id=user_1.id).email == user_1.email
    assert user_service.get_user_by_email(db=db, email=user_1.email) is not None
    db.close()

