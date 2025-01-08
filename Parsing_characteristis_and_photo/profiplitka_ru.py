from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import requests

# Настраиваем заголовок User-Agent
chrome_options = Options()
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Указываем путь к WebDriver через Service
webdriver_path = r"C:\Users\Administrator\Documents\install\chromedriver\chromedriver.exe"  # Замените на ваш путь
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Отправляем запрос через requests для проверки
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}


# Открываем страницу через Selenium
driver.get("https://profiplitka.ru")
cookies = driver.get_cookies()

# Конвертируем cookies в формат requests
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# Выполняем запрос с cookies
response = session.get("https://profiplitka.ru/search/?searchstring=Belleza+Denis+Grande+Shapetouch+60x120", headers=headers)
print(response.status_code)
print(response.text)
