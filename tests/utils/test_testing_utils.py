import sys

sys.path.append("../no-pressure-query-backend")

from main import JWT_SECRET
from utils import testing_utils
from utils.database_utils import SessionLocal
from services import user_service
from schemas import user_schema
from models import user_model
import jwt

def test_create_user():
    db = SessionLocal()
    num_users_before_user_create = db.query(user_model.User).count()
    user = testing_utils.create_user()
    num_users_after_user_create = db.query(user_model.User).count()
    db.close()
    assert num_users_after_user_create - num_users_before_user_create == 1

def test_get_token_with_specific_password():
    user = testing_utils.create_user(password="test_password")
    token = testing_utils.get_token(user, password="test_password")
    db = SessionLocal()
    user_db_model = user_service.get_user(db=db, user_id=user.id)
    db.close()
    user_obj = user_schema.User.from_orm(user_db_model)
    assert token == jwt.encode(user_obj.dict(), JWT_SECRET)

def test_get_token_without_password():
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    db = SessionLocal()
    user_db_model = user_service.get_user(db=db, user_id=user.id)
    db.close()
    user_obj = user_schema.User.from_orm(user_db_model)
    assert token == jwt.encode(user_obj.dict(), JWT_SECRET)

