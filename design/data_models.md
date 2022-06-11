User:
    has_many: 
        - surveys
        - question_answers
    
    email: string, required, unique
    hashed_password: string, required
    first_name: string, required
    last_name: string, required

Survey:
    belongs_to: 
        - user
    has_many:
        - survey_questions
        
SurveyQuestion
    belongs_to
        - survey

    has_many:
        - available_answers
    question_type: enum, required
    #The question type should aid us in writing unit tests and ensuring data validity
    #For "single_choice_question" we can have multiple available answers but only one of 
    #them can contain an answer for a particular user
    #For "multiple_choice_question" we can have multiple available answers and multiple #AvalableAnswers can have answers from a single user
    #For "text_question" we can have one avaiable answer and it can have only one answer from
    #one user
    #For "weighted_ranking" we can have multiple avaliable answers and each it must have
    #a QuestionAnswer that from each user
    
AvailableAnswer
    belongs_to:
        - survey_question
    has_many:
        - question_answers

    weight: integer, required, default: 1

QuestionAnswer
    belongs_to:
        - available_answer
        - user 
    answer: string, required
