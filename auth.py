from fastapi import Depends, FastAPI, HTTPException
import fastapi
import jwt
from sqlalchemy.orm import Session

import models, schemas
import fastapi.security as security
from main import get_db, oauth2schema, JWT_SECRET


# Dependency
async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2schema)
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(detail="Invalid token", status_code=401)

    return schemas.User.from_orm(user)
