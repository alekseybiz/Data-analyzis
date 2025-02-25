import json

import requests


auth_key = ""
client_id = ""
scope = "GIGACHAT_API_PERS"
client_secret = ""

access_token = ""

# Получение токена доступа
# url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
# response = requests.post(
#     url=url,
#     data={
#         'grant_type': 'client_credentials',
#         'client_id': client_id,
#         'client_secret': client_secret
#     },
#     verify=False
# )
#
# token = response.json()['access_token']
# print(f"token: {token}")


url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

data = {
    'model': 'GigaChat-Pro',
    'messages': [
        {'role': 'user',
         'content': 'Расскажи анекдот про Yandex GPT'}
    ],
    'temperature': 0.5
}

headers = {
        'Authorization': f'Bearer {access_token}',
        # 'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

response = requests.post(url, headers=headers, json=data, verify=False) # Обязательно надо: verify=False

if response.status_code == 200:
    # print(response.json())
    print(response
          .json()
          # .get("choices")
          # .get("message")
          # .get("content")
          # .get("text")
          )
else:
    print(f"Error: {response.status_code} - {response.text}")
