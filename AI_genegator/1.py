import openai
from config import api_key

# Установите ваш API-ключ
openai.api_key = api_key

# Запрос списка моделей
try:
    models = openai.Model.list()
    print("Доступные модели:")
    for model in models['data']:
        print(model['id'])
except Exception as e:
    print(f"Ошибка: {e}")
