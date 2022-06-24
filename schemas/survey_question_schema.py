from pydantic import BaseModel
from models.survey_question_model import SurveyQuestionEnum
import orjson


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class SurveyQuestionBase(BaseModel):
    question_type: SurveyQuestionEnum
    question_text: str


class SurveyQuestionCreate(SurveyQuestionBase):
    pass

class SurveyQuestion(SurveyQuestionBase):
    id: int

    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
