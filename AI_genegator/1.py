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
message = 'привет!'

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": message,
        }
    ],
    model="gpt-4o",
)

# Извлечение текста ответа
response_text = chat_completion.choices[0].message.content

# Печать только текста
print(response_text)