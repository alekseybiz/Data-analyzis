from selenium import webdriver

# Укажите путь к драйверу Chrome
webdriver_path = r"C:\Users\Administrator\Documents\install\chromedriver\chromedriver.exe"

# Инициализация браузера
driver = webdriver.Chrome(executable_path=webdriver_path)

# Открываем сайт
driver.get("https://www.google.com")
print("Браузер запущен!")

# Закрываем браузер
driver.quit()