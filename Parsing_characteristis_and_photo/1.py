import openpyxl

# Настройте путь к вашему файлу Excel
excel_path = "Ozon/ОЗОН Equipe_try.xlsx"
# Открываем таблицу Excel
workbook = openpyxl.load_workbook(excel_path)
sheet = workbook.active

row_number = 6

value = sheet.cell(row=row_number, column=36).value

print(f"значение: {value}")

