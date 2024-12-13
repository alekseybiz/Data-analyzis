import openai
from config import api_key, gpt_id

def get_gpt_response(api_key, prompt, model="gpt-4", max_tokens=500):
    """
    Отправляет запрос в OpenAI API и получает ответ.

    :param api_key: Ваш API-ключ OpenAI
    :param gpt_id: ID или endpoint вашего кастомного GPT
    :param prompt: Ввод текста (вопрос или запрос)
    :param model: Модель для использования (по умолчанию gpt-4)
    :param max_tokens: Максимальное количество токенов в ответе
    :return: Ответ модели
    """
    try:
        # Устанавливаем ключ API
        openai.api_key = api_key

        # Отправляем запрос в API
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )

        # Извлекаем текст из ответа
        return response.choices[0].message["content"].strip()

    except Exception as e:
        return f"Произошла ошибка: {e}"

# Пример использования
if __name__ == "__main__":

    # Вопрос для ChatGPT
    prompt = "Плитка Chicago Gray фабрики New Trend"

    # Получение ответа от модели
    answer = get_gpt_response(api_key, prompt)
    print(f"Ответ от GPT: {answer}")
