
import openai
import time
import requests
import json

openai.api_key = json.load(open("dmypy.json")).get("openai_api_key", [])

def chatOpenAI(prompt, text):
    completions = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    )
    ans = completions.choices[0].message.content
    return ans

def chatCommon(prompt, text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai.api_key}',
    }
    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    return response.json()['choices'][0]['message']['content']


if __name__ == "__main__":
    print(openai.api_key)
