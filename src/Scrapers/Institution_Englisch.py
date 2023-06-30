import requests
import json
import os
from dotenv import load_dotenv

# load environment variables once at the start of the script
load_dotenv()

api_key = os.getenv("OPEN_AI_API_KEY")


def chat_with_gpt3(question):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"Request to OpenAI failed with status {response.status_code}, response: {response.text}")
        return None
    response_json = response.json()

    if 'choices' in response_json:
        return response_json['choices'][0]['message']['content']
    else:
        return None


def update_institution_names(dataset):
    print("Updating institutions names to English...")

    checked_names = {}

    for entry in dataset:
        institution = entry.get('Institution')
        if institution and institution not in checked_names:
            question = "The following name of an institution, is this in English or in a different language?" + institution + ". if it is in English please return the same name. If it is not in English please return the name of the institution in English. Can you make sure to just return the name of the institution and dont say anything else."

            response = chat_with_gpt3(question)
            checked_names[institution] = response

        entry['Institution'] = checked_names.get(institution, institution)

    print("Finished updating institutions names to English")
    return dataset
