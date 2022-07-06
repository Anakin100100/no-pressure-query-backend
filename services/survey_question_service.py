from sqlalchemy.orm import Session
import schemas.survey_question_schema as survey_question_schema
import schemas.survey_schema as survey_schema
import schemas.user_schema as user_schema
import models.survey_question_model as survey_question_model
from fastapi import HTTPException

def create_survey_question(db: Session, survey: survey_schema.Survey, survey_question_create: survey_question_schema.SurveyQuestionCreate, user: user_schema.User):
    if survey_question_create.question_text == None or survey_question_create.question_text == "":
        raise HTTPException(detail=f"Question text has to be a valid string, provided: {survey_question_create.question_type}", status_code=400)
    
    db_survey_question = survey_question_model.SurveyQuestion(survey_id=survey.id, question_type=survey_question_create.question_type, question_text=survey_question_create.question_text)
    db.add(db_survey_question)
    db.commit()
    db.refresh(db_survey_question)
    return db_survey_question
