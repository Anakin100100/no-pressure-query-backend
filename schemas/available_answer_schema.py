from pydantic import BaseModel
import orjson


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class AvailableAnswerBase(BaseModel):
    weigth: int = 1
    answer_text: str

class AvailableAnswerCreate(AvailableAnswerBase):
    pass

class AvailableAnswer(AvailableAnswerBase):
    id: int

    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
