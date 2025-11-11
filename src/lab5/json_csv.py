import json   # Импортируем библиотеку для работы с JSON файлами
import csv    # Импортируем библиотеку для работы с CSV файлами
from pathlib import Path  # Используем модуль Path для удобной работы с путями файлов

# Функция для проверки расширения файла
def check_file_extension(file_path: str, expected_extensions: tuple) -> bool:
    """
    Проверяет расширение файла на совпадение с ожидаемым списком расширений.
    :param file_path: полный путь к файлу
    :param expected_extensions: кортеж ожидаемых расширений
    :return: True, если расширение совпадает, иначе False
    """
    # Получаем суффикс файла и сравниваем его с ожидаемыми расширениями
    return any(Path(file_path).suffix.lower().endswith(ext) for ext in expected_extensions)

# Функция для преобразования JSON файла в CSV файл
def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Преобразует содержимое JSON файла в CSV файл.
    :param json_path: путь к исходному JSON файлу
    :param csv_path: путь к результирующему CSV файлу
    """

    # Проверяем расширение входящего файла
    if not check_file_extension(json_path, ('.json',)):
        raise ValueError(f"Входной файл '{json_path}' не является JSON.")

    # Проверяем расширение выходящего файла
    if not check_file_extension(csv_path, ('.csv',)):
        raise ValueError(f"Выходной файл '{csv_path}' не является CSV.")

    # Создаем объект пути для JSON файла
    json_file = Path(json_path)
    
    # Проверяем существование JSON файла
    if not json_file.exists():  
        # Если файл не существует, поднимаем исключение
        raise FileNotFoundError(f"Файл {json_path} не найден.")  # [1]
    
    # Открываем JSON файл для чтения
    with json_file.open('r', encoding='utf-8') as f:
        # Загружаем данные из JSON файла
        data = json.load(f)  # [2]
        
    # Проверяем структуру данных (список словарей)
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        # Поднимаем ошибку, если структура неверная
        raise ValueError("JSON должен содержать список словарей.")  # [3]
    
    # Определяем заголовки столбцов путем объединения всех ключей из каждого элемента списка
    headers = set()                   # [4]
    for item in data:
        headers.update(item.keys())   # Добавляем ключи текущего элемента в общий набор
    headers = sorted(headers)         # Сортируем заголовки для упорядоченности
    
    # Открываем CSV файл для записи
    with Path(csv_path).open('w', newline='', encoding='utf-8') as f:
        # Создаем объект DictWriter для записи словарей в CSV
        writer = csv.DictWriter(f, fieldnames=headers)  # [5]
        # Записываем строку заголовков
        writer.writeheader()                           # [6]
        # Записываем строки данных
        writer.writerows(data)                         # [7]

# Функция для преобразования CSV файла в JSON файл
def csv_to_json(csv_path: str, json_path: str) -> None:
    """
    Преобразует содержимое CSV файла в JSON файл.
    :param csv_path: путь к исходному CSV файлу
    :param json_path: путь к результирующему JSON файлу
    """

    # Проверяем расширение входящего файла
    if not check_file_extension(csv_path, ('.csv',)):
        raise ValueError(f"Входной файл '{csv_path}' не является CSV.")

    # Проверяем расширение выходящего файла
    if not check_file_extension(json_path, ('.json',)):
        raise ValueError(f"Выходной файл '{json_path}' не является JSON.")

    # Создаем объект пути для CSV файла
    csv_file = Path(csv_path)
    
    # Проверяем существование CSV файла
    if not csv_file.exists():
        # Если файл не существует, поднимаем исключение
        raise FileNotFoundError(f"Файл {csv_path} не найден.")  # [8]
    
    # Открываем CSV файл для чтения
    with csv_file.open('r', encoding='utf-8') as f:
        # Читаем CSV файл строка за строкой, создавая словарь для каждой строки
        reader = csv.DictReader(f)                       # [9]
        # Преобразуем прочитанные строки в список словарей
        data = list(reader)                              # [10]
    
    # Проверяем наличие данных в списке
    if not data:
        # Поднимаем ошибку, если CSV файл пустой
        raise ValueError("CSV-файл пуст.")               # [11]
    
    # Открываем JSON файл для записи
    with Path(json_path).open('w', encoding='utf-8') as f:
        # Записываем преобразованные данные в JSON файл
        json.dump(data, f, ensure_ascii=False, indent=2) # [12]

# Основная секция программы
if __name__ == "__main__":
    # Выполняем преобразование JSON->CSV и CSV->JSON
    json_to_csv("data/samples/people.json", "data/out/people_from_json.csv")  # [13]
    csv_to_json("data/samples/people.csv", "data/out/people_from_csv.json")   # [14]# [27]