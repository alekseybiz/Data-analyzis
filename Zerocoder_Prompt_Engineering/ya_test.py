import requests

# Идентификатор ключа
# ajejpvmr7on96tb2aoo5
# Ваш секретный ключ
# AQVN08_ts-LpN1YlYwVpmnruQRuvzfcqL98IvKJD

# Идентификатор ключа
# ajeo1l2imjc6d4mpjon2
# Ваш секретный ключ
# AQVN2A1FK02GaS2Z4uLuDEw4UepfLbiuhZbUfmbm

# Идентификатор ключа
# aje2krirv7oep28dbh78
# Ваш секретный ключ
# AQVNwqblv58OyJDVxOjpipaRWvNstY-MaAYCA0oX


api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
api_key = "AQVNwqblv58OyJDVxOjpipaRWvNstY-MaAYCA0oX"

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