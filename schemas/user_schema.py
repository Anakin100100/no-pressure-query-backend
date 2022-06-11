from pydantic import BaseModel
import orjson


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
