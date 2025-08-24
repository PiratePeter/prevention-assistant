from flask import jsonify
from google import genai

client = genai.Client()


def get_llm_answer_logic(request):
    data = request.json
    prompt = data.get('prompt')
    preventions = data.get('preventions')

    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt + "\n\n" + preventions
    )

    return_data = {'preventions': response.text}
    return jsonify(return_data), 200
