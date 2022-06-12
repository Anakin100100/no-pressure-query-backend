from utils import auth_utils
from utils.database_utils import SessionLocal
from utils.testing_utils import create_user
from schemas import user_schema
from services import user_service
from utils.auth_utils import JWT_SECRET
import jwt
from fastapi import HTTPException
import pytest

@pytest.mark.asyncio
async def test_get_current_user_with_incorrect_token():
    db = SessionLocal()
    fake_token = "totally unauthentic token that should not work"
    with pytest.raises(HTTPException):
        _ = await auth_utils.get_current_user(db, fake_token)

@pytest.mark.asyncio
async def test_get_current_user_with_correct_token():
    db = SessionLocal()
    user_created = create_user()
    user_db_model = user_service.get_user(db=db, user_id=user_created.id)
    user_obj = user_schema.User.from_orm(user_db_model)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    print(token)
    current_user = await auth_utils.get_current_user(db=db, token=token)
    db.close()
    assert user_obj.id == current_user.id
    assert user_obj.email == current_user.email
    assert user_obj.first_name == current_user.first_name
    assert user_obj.last_name == current_user.last_name

@pytest.mark.asyncio
async def test_authenticate_user_with_correct_data():
    db = SessionLocal()
    user = create_user(password="a_specific_password")
    authenticated_user =  await auth_utils.authenticate_user(email=user.email, password="a_specific_password", db=db)
    db.close()
    assert authenticated_user.id == user.id
    assert authenticated_user.email == user.email
    assert authenticated_user.first_name == user.first_name
    assert authenticated_user.last_name == user.last_name

@pytest.mark.asyncio
async def test_authenticate_user_with_incorrect_password():
    db = SessionLocal()
    user = create_user(password="a_specific_password")
    db.close()
    assert await auth_utils.authenticate_user(email=user.email, password="wrong_password", db=db) == False

@pytest.mark.asyncio
async def test_authenticate_user_ith_incorrect_email():
    db = SessionLocal()
    _ = create_user(password="a_specific_password")
    db.close()
    assert await auth_utils.authenticate_user(email="wrongemail@gmail.com", password="a_specific_password", db=db) == False
    
@pytest.mark.asyncio
async def test_create_token():
    TEST_JWT_SECRET = "923994293942949"
    user_created = create_user(password="a_specific_password")
    db = SessionLocal()
    user_db_model = user_service.get_user(db=db, user_id=user_created.id)
    db.close()
    user_obj = user_schema.User.from_orm(user_db_model)
    token = await auth_utils.create_token(user_db_model, secret=TEST_JWT_SECRET)
    assert token["access_token"] == jwt.encode(user_obj.dict(), TEST_JWT_SECRET)
