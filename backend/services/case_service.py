from datetime import datetime

from flask import jsonify
from generated.models import PreventionCase, PreventionQuestion
from persistence.database import get_session

# {'customer': {'firstname': 'Alexander', 'lastname': 'Peter', 'email': 'alexpeter95@hotmail.com'}, 
# 'building_info': {'facade': 'Stein', 'roof': 'Keine Dachfenster', 'basement': 'Kellergrube vorhanden', 'heating': 'Íl / Gas'}, 
# 'damage': 'yes', 'damage_desc': 'Bei starkem Regen lief mein Keller voll.', 'specific_questions': 
# [{'question': 'Beschreiben Sie bitte prõzise, auf welchem Weg und an welchen Stellen das Wasser bei Starkregenereignissen in Ihren Keller eingedrungen ist und welche Vorkehrungen oder baulichen Anpassungen Sie bereits getroffen haben, um dies zuk³nftig zu verhindern?', 'answer': 'Ja'}, 
# {'question': 'Wie ist die Oberflõchenentwõsserung auf Ihrem Grundst³ck gestaltet, insbesondere im Bereich um das Gebõude und bei Lichtschõchten oder Kellerabgõngen? Gibt es Gefõlle, Drainagen oder Sammelsysteme, die Oberflõchenwasser vom Haus wegleiten?', 'answer': 'Nein'}, {'question': 'Welches Material und Alter haben Ihr Dach (inkl. Eindeckung, Dachfenster, Solaranlagen) und Ihre Fassade? Sind diese Bauteile sowie alle externen Anbauten (z.B. Rolllõden, Antennen, Vordõcher) auf ihre Widerstandsfõhigkeit gegen³ber starkem Wind und Hagel gepr³ft oder gewartet worden?', 'answer': 'Vielleicht'}, {'question': 'Welche technischen Installationen (z.B. Heizung, Elektrik, Íltank) befinden sich im Keller und sind diese gegen Wassereintritt gesch³tzt oder leicht versetzbar? Verf³gt Ihr Gebõude ³ber R³ckstauventile oder Pumpensysteme zur Abwasserableitung?', 'answer': 'Kannst du die Frage wiederholen'}, {'question': 'Gibt es auf Ihrem Grundst³ck oder in unmittelbarer Nõhe des Gebõudes Bõume, die bei Sturm auf das Gebõude fallen k÷nnten, oder andere lose Gegenstõnde/Strukturen im Aussenbereich, die eine Gefahr darstellen k÷nnten?', 'answer': '?'}]}


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
