import openpyxl
import openai
from openai import OpenAI
import sys
from pathlib import Path
# Определяем путь к корневой папке проекта (Data-analyzis)
project_root = Path(__file__).resolve().parent.parent
# Добавляем путь к корню проекта в sys.path
sys.path.append(str(project_root / "AI_genegator"))
# Теперь можно импортировать api_key из config
from config import api_key


# Установите ваш API-ключ OpenAI
openai.api_key = api_key

excel_path = "for_parsing_try.xlsx"

client = OpenAI(api_key=api_key)



# Функция для получения свойств товара от ChatGPT
def get_characteristics(brand, collection, product):
    message = 'Собери все указанные характеристики для товара ' + product + ' фабрики ' + brand + ' коллекции ' + collection
    # print(message)
    content = 'Ты контент-менеджер. Найди в интернете технические характеристики и фото этого товара. Проанализируй фото и информацию о товаре. Составь ответ в виде словаря.'
    try:
        chat_completion = client.chat.completions.create(
            model="chatgpt-4o-latest",
            max_tokens=300,
            temperature=0.1,
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
        # Извлекаем описание из ответа
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Ошибка при обработке запроса для {product}: {e}")

        # print(f"Ошибка при обработке запроса для {product}: {e}")
        # return "Ошибка при генерации описания"



# Открываем Excel-файл
workbook = openpyxl.load_workbook(excel_path)
sheet = workbook.active

# список характеристик
selected_headers = []

# Указываем индексы столбцов, заголовки которых нужно собрать
columns_to_collect = list(range(9, 31))
print(columns_to_collect)

# Сбор заголовков
for col_index in columns_to_collect:
    header = sheet.cell(row=41, column=col_index).value  # Извлекаем значение из первой строки
    if header:  # Проверяем, что заголовок не пустой
        selected_headers.append(header)

print(f'список характеристик: {selected_headers}')

i = 0
try:
    # Проход по строкам
    for row in sheet.iter_rows(min_row=41, max_row=sheet.max_row, min_col=2, max_col=30):
        i += 1
        brand = row[3].value  # Бренд
        collection = row[4].value  # Коллекция
        product = row[5].value  # Товар
        print(f"Бренд: {brand}; Коллекция: {collection}; Товар: {product}")

        if product:
            print(f"{i}. Обрабатываю: товар - {product}")
            try:
                description = get_characteristics(brand, collection, product)
            except RuntimeError as e:
                print(e)
                break  # Прерываем цикл при ошибке
            row[-2].value = description  # Записываем описание в столбец "Описание"

finally:
    # Сохраняем изменения в Excel-файле независимо от результата
    workbook.save(excel_path)
    print(f"Описание сохранено в {excel_path}.")
