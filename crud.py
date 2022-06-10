from sqlalchemy.orm import Session
import passlib.hash as hash
import models, schemas


def get_user(db: Session, user_id: int) -> models.User:
    """
    Get a user by id
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    """
    Get a user by email
    """
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Create a new user
    """
    hashed_password = hash.bcrypt.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
