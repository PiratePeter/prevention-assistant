from datetime import datetime

from flask import jsonify
from generated.models import PreventionCase, PreventionQuestion
from persistence.database import get_session


def load_cases_logic(_):
    session = get_session()
    result = (
        session.query(PreventionCase)
        .all()
    )
    return (
        jsonify(
            [
                {
                    "ID": db_case.id,
                    "Vorname": db_case.firstname,
                    "Name": db_case.lastname,
                    "Datum": db_case.creation_time.strftime("%d.%m.%Y %H:%M"),
                }
                for db_case in result
            ],
        ),
        200,
    )
    
def load_case_logic(request):
    session = get_session()
    case_id = request.args.get('id')

    if not case_id:
        return jsonify({'error': 'case_id is required'}), 400

    db_questions = (
        session.query(PreventionQuestion)
        .filter(PreventionQuestion.prevention_case_id == case_id)
        .all()
    )

    db_case = (
        session.query(PreventionCase)
        .filter(PreventionCase.id == case_id)
        .first()
    )
    damage_desc = db_case.damage_desc
    response = {
        "damage":"Nein" if ""==damage_desc else "Ja",
        "damage_desc": damage_desc,
        "building_info":{
            "facade":db_case.facade,
            "basement":db_case.basement,
            "roof":db_case.roof,
            "heating":db_case.heating
        },
        "specific_questions":[
            {
                "question": db_question.question_text,
                "answer": db_question.answer_text,
            }
            for db_question in db_questions
        ],
        "customer":{
            "firstname":db_case.firstname,
            "lastname":db_case.lastname,
            "email":db_case.email
        },
        "preventions":"text" #TODO get preventions
    }

    return jsonify(response), 200

def save_case_logic(request):
    session = get_session()
    data = request.json
    timestamp = datetime.now()
    firstname = data.get('customer').get('firstname')
    lastname = data.get('customer').get('lastname')
    email = data.get('customer').get('email')
    facade = data.get('building_info').get('facade')
    roof = data.get('building_info').get('roof')
    basement = data.get('building_info').get('basement')
    heating = data.get('building_info').get('heating')
    damage_desc = data.get('damage_desc')
    questions = data.get('specific_questions')

    if not questions or not isinstance(questions, list):
        return jsonify({'error': 'Invalid payload'}), 400

    db_case = PreventionCase(
        creation_time = timestamp,
        firstname=firstname, 
        lastname=lastname, 
        email=email,
        facade=facade,
        roof=roof,
        basement=basement,
        heating=heating,
        damage_desc=damage_desc,
    )
    session.add(db_case)
    session.commit()

    db_questions = []
    for question in questions:
        db_question = PreventionQuestion(
            prevention_case_id=db_case.id,
            question_text=question['question'], 
            answer_text=question['answer']
        )
        db_questions.append(db_question)

    session.add_all(db_questions)
    session.commit()

    return jsonify({'message': 'Case saved successfully'}), 201
