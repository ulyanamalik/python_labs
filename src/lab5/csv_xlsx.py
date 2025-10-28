import csv
from pathlib import Path
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """
    Конвертирует CSV в XLSX.
    Использовать openpyxl ИЛИ xlsxwriter.
    Первая строка CSV — заголовок. 
    Лист называется "Sheet1".
    Колонки — автоширина по длине текста (не менее 8 символов).
    """
    # Проверка существования файла
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"Файл {csv_path} не найден.")

    with csv_file.open('r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    if not data:
        raise ValueError("CSV-файл пуст.")
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"

    # Запись данных в XLSX
    for row in data:
        sheet.append(row)

    # Установка автоширины колонок
    for col_idx, col in enumerate(sheet.columns, 1):
        max_length = max(len(str(cell.value)) for cell in col)
        adjusted_width = max((max_length + 2), 8)  # Минимальная ширина 8 символов
        sheet.column_dimensions[get_column_letter(col_idx)].width = adjusted_width

    # Сохранение XLSX-файла
    workbook.save(xlsx_path)

# Пример использования
if __name__ == "__main__":
    csv_to_xlsx("data/samples/people.csv", "data/out/people.xlsx")