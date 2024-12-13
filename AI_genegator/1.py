import openai
import os
from openai import OpenAI
from config import api_key

# Установите ваш API ключ
api_key = api_key

# Инициализация клиента OpenAI
openai.api_key = api_key

client = OpenAI(
    api_key=api_key,  # This is the default and can be omitted
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-4o",
)
# print(response.choices[0].message["content"])
