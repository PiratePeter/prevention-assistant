import json
from google import genai


client = genai.Client()


def gen_recommendation_logic(data: dict)-> dict[str, str]:
    """
    Generates a recommendation based on the provided data.
    :param data: Dictionary containing risks and previous claims description
    """
    merged_context = json_to_string(data)
    
    prompt = (
        "Generate a mail to a building owner in the canton of Bern, Switzerland, "
        "recommending preventative actions to mitigate future damage from natural forces. "
        "The recommendation should be based on the following context:\n\n"
        f"{merged_context}\n\n"
        "The recommendation should be a JSON object with a single key, 'recommendation', "
        "whose value is a string representing the recommendation. "
        "Ensure the recommendation is clear, concise, and directly related to the risks identified. "
        "The recommendation should cover a range of relevant aspects related to building construction, "
        "maintenance, and surrounding environment to best evaluate risks and recommend effective mitigation measures. "
        "Ensure the recommendation mail text is in high german (minor adaptions to Switzerland ß->ss, etc.), "
        "and is tailored to the specific risk levels identified in the context. "
        "Ensure the recommendation is actionable and provides valuable insights for the building owner. "
        "For more complex actions, recommend a well-known craftsman in the area to perform the work. "
        "The mail will be verified by a human insurance agent and sent in the name of the insurance company. "
        "Return only the formated recommendation mail text as a JSON object and keep it really concise."
    )

    print(f"Prompt for recommendation generation:\n{prompt}\n")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt
    )

    response_text = response.text.strip()
    if not response_text.startswith('{') or not response_text.endswith('}'):
        response_text = response_text.replace("```json", "").replace("```", "")

    try:
        response_json = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Response is not valid JSON: {response_text}") from e
    if not isinstance(response_json["recommendation"], str):
        raise ValueError(f"Response is not a recommendation str: {response_json}")
    return response_json


def json_to_string(data, indent=0):
    """
    Recursively converts dicts/lists into a readable string.
    """
    pad = "  " * indent
    output = []

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                output.append(f"{pad}{key}:")
                output.append(json_to_string(value, indent + 1))
            else:
                output.append(f"{pad}{key}: {value}")

    elif isinstance(data, list):
        for idx, item in enumerate(data, 1):
            output.append(f"{pad}- Item {idx}:")
            output.append(json_to_string(item, indent + 1))

    else:  # primitive
        output.append(f"{pad}{data}")

    return "\n".join(output)


if __name__ == "__main__":
    # Example usage
    data = {"damage": "yes",
            "damage_desc": "Wasserschaden im Keller durch Rohrbruch",
            "building_info": {
                "facade": "Holz",
                "basement": "Beton",
                "roof": "Ziegel",
                "heating": "Wärmepumpe"
            },
            "specific_questions": [
                {"question": "Baujahr des Gebäudes?", "answer": "1998" },
                {"question": "Hat es eine Solaranlage?", "answer": "Ja, 12 kWp"},
                {"question": "Wie viele Etagen?", "answer": "3" }
            ],
            "customer": {
                "firstname": "Luca",
                "lastname": "Müller",
                "email": "luca.mueller@example.com"
            }
        }
    
    try:
        recommendation = gen_recommendation_logic(data)
        print("Generated Recommendation:", recommendation)
    except Exception as e:
        print(f"Error: {str(e)}")
