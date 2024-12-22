from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Укажите путь к драйверу Chrome
webdriver_path = r"C:\Users\Administrator\Documents\install\chromedriver\chromedriver.exe"

# Настройка сервиса для драйвера Chrome
service = Service(webdriver_path)

# Инициализация браузера
driver = webdriver.Chrome(service=service)

# Открываем сайт
driver.get("https://www.google.com")
print("Браузер запущен!")

# Закрываем браузер
driver.quit()
