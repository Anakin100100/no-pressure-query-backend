from pydantic import BaseModel
import orjson


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class QuestionAnswerBase(BaseModel):
    answer: str

class QuestionAnswerCreate(QuestionAnswerBase):
    pass

class QuestionAnswer(QuestionAnswerBase):
    id: int

    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
