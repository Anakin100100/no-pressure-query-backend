from sqlalchemy.orm import Session
import passlib.hash as hash
import schemas
import models.user_model as user_model


def get_user(db: Session, user_id: int) -> user_model.User:
    """
    Get a user by id
    """
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> user_model.User:
    """
    Get a user by email
    """
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> user_model.User:
    """
    Create a new user
    """
    hashed_password = hash.bcrypt.hash(user.password)
    db_user = user_model.User(email=user.email, hashed_password=hashed_password, first_name=user.first_name, last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
