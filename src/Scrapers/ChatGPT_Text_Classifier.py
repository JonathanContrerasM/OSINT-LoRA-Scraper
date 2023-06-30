import requests
import json
import re
import os
from dotenv import load_dotenv


def chat_with_gpt3(question):
    load_dotenv()
    api_key = os.getenv("OPEN_AI_API_KEY")
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

    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response_json = response.json()

            print("Tried with ChatGPT")

            content = response_json['choices'][0]['message']['content']
            extracted_strings = re.findall(r'"([^"]*)"', content)

            return extracted_strings[0]
        except IndexError:
            print(f"ChatGPT failure on attempt {attempt + 1}, retrying...")

    print("ChatGPT failure after 3 attempts, switching to B-Mode")
    return 'ElectroSense'


def get_company_from_text(input_text):
    question = f"""
    i have this text string: 
    {input_text}
    In here is a company name.  Please only provide the company name and do not elaborate anything else. Just return the "company name" not even the company name is etc..."""

    response = chat_with_gpt3(question)
    print("Retrieved project name: " + response)
    return response
