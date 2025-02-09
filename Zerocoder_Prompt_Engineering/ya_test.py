import requests
from config import api_url, api_key




headers = {
    "Authorization": f"Api-key <api_key>",
    "Content-Type": "application/json"
}

data = {
    "modelUri": "gpt://b1g56h2p36fq4g7gub7l/yandexgpt/latest",
      "completionOptions": {
        "stream": False,
        "temperature": 0,
        "maxTokens": "200"
      },
      "messages": [
        {
          "role": "system",
          "text": "Исправь грамматические, орфографические и пунктуационные ошибки в тексте. Сохраняй исходный порядок слов."
        },
        {
          "role": "user",
          "text": "Нейросети помогают человеку работать быстрее и эффективнее но опосения что искуственный интелек заменит человека - пока преждевремены"
        }
      ]
}

response = requests.post(api_url, headers=headers, json=data)

if response.status_code == 200:
    print(response
          .json()
          .get("result")
          .get("alternatives")[0]
          .get("message")
          .get("text")
          )
else:
    print(f"Error: {response.status_code} - {response.text}")