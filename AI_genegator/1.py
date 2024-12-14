import openai
from openai import OpenAI
from config import api_key


# Инициализация клиента OpenAI
openai.api_key = api_key

client = OpenAI(
    api_key=api_key,  # This is the default and can be omitted
)
message = 'привет!'
content = 'Вы — профессиональный копирайтер с большим опытом. Ваши ответы должны быть экспертными, креативными и убедительными. Используйте лаконичные, информативные и привлекательные формулировки.'

chat_completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": content,
        },
        {
            "role": "user",
            "content": message,
        }
    ]
)

# Извлечение текста ответа
response_text = chat_completion.choices[0].message.content

print(response_text)
