from flask import jsonify
from google import genai

client = genai.Client()

def get_llm_answer_logic(request):
    # ... = request.args.get('...')
    prompt = 'Explain how AI works in a few words'
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt
    )

    dummy_data = {'prompt': prompt, 'response': response.text}
    return jsonify(dummy_data), 200
