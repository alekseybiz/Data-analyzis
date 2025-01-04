"""Пример обращения к GigaChat с помощью GigaChain"""
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

authorization_key = "YWJkMDc5N2QtMzA3OC00Yjg3LWE2Y2EtYmQ3MzRkNDAxYTBiOjg4NjE3ZTQyLTg5NzktNGM3Ny1iY2EyLTM0ODQ5ZTNjZWZiNA=="
# Авторизация в GigaChat
model = GigaChat(
    credentials=authorization_key,
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    # Отключает проверку наличия сертификатов НУЦ Минцифры
    verify_ssl_certs=False,
)

messages = [
    SystemMessage(
        content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
    )
]

while(True):
    user_input = input("Пользователь: ")
    if user_input == "пока":
      break
    messages.append(HumanMessage(content=user_input))
    res = model.invoke(messages)
    messages.append(res)
    print("GigaChat: ", res.content)