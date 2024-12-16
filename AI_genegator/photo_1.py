import requests

subscription_key = "ВАШ_BING_API_KEY"
query = "Керамин Гламур керамическая плитка"


def search_images_bing(query, subscription_key):
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {
        "q": query,              # Запрос для поиска
        "count": 10,             # Количество результатов
        "imageType": "photo",    # Только фотографии
        "license": "public",     # Только общедоступные изображения
        "size": "large",         # Изображения большого размера
        "imageContent": "none"   # Исключение водяных знаков
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()  # Проверка на ошибки
    results = response.json()
    return [img["contentUrl"] for img in results.get("value", [])]


images = search_images_bing(query, subscription_key)

# Вывод результатов
for img_url in images:
    print(img_url)