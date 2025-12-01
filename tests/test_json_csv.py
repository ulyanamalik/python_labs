import pytest
import json
import csv
from pathlib import Path
import sys
import os

# Добавляем корневую директорию проекта в путь поиска модулей Python
# Это позволяет импортировать модули из папки src как пакеты
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Импортируем функции для тестирования из модуля json_csv
from src.lab5.json_csv import json_to_csv, csv_to_json


def test_json_to_csv_roundtrip(tmp_path: Path):
    """
    Тестирует успешную конвертацию JSON → CSV (позитивный тест)

    Сценарий:
    1. Создаем тестовый JSON файл с данными
    2. Конвертируем в CSV
    3. Проверяем что CSV файл создан и содержит правильные данные
    """
    # Создаем временные файлы для теста
    src = tmp_path / "people.json"
    dst = tmp_path / "people.csv"

    # Тестовые данные для конвертации
    data = [
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 25},
    ]

    # Записываем JSON файл
    src.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    # Выполняем конвертацию
    json_to_csv(str(src), str(dst))

    # Читаем и проверяем результат
    with dst.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Проверки:
    assert len(rows) == 2  # Должно быть 2 записи
    assert rows[0]["name"] == "Alice"  # Первая запись - Alice
    assert rows[1]["age"] == "25"  # Возраст должен быть строкой (особенность CSV)


def test_csv_to_json_roundtrip(tmp_path: Path):
    """
    Тестирует успешную конвертацию CSV → JSON (позитивный тест)

    Сценарий:
    1. Создаем тестовый CSV файл с данными
    2. Конвертируем в JSON
    3. Проверяем что JSON файл создан и содержит правильные данные
    """
    # Создаем временные файлы для теста
    src = tmp_path / "people.csv"
    dst = tmp_path / "people.json"

    # Создаем CSV файл с тестовыми данными
    with src.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age"])
        writer.writeheader()  # Записываем заголовок
        writer.writerow({"name": "Alice", "age": "22"})  # Первая строка данных
        writer.writerow({"name": "Bob", "age": "25"})  # Вторая строка данных

    # Выполняем конвертацию
    csv_to_json(str(src), str(dst))

    # Читаем и проверяем результат
    data = json.loads(dst.read_text(encoding="utf-8"))

    # Проверки:
    assert isinstance(data, list)  # Результат должен быть списком
    assert len(data) == 2  # Должно быть 2 элемента
    assert data[0]["name"] == "Alice"  # Первый элемент - Alice
    assert data[1]["age"] == "25"  # Возраст сохраняется как строка


def test_json_to_csv_invalid_json(tmp_path: Path):
    """
    Тестирует обработку некорректного JSON файла (негативный тест)

    Сценарий:
    1. Создаем файл с некорректным JSON
    2. Пытаемся конвертировать
    3. Ожидаем ValueError
    """
    src = tmp_path / "broken.json"
    dst = tmp_path / "output.csv"

    # Создаем файл с некорректным JSON
    src.write_text("not a json", encoding="utf-8")

    # Проверяем что функция выбрасывает ValueError
    with pytest.raises(ValueError):
        json_to_csv(str(src), str(dst))


def test_csv_to_json_empty_file(tmp_path: Path):
    """
    Тестирует обработку пустого CSV файла (негативный тест)

    Сценарий:
    1. Создаем полностью пустой файл
    2. Пытаемся конвертировать
    3. Ожидаем ValueError
    """
    src = tmp_path / "empty.csv"
    dst = tmp_path / "output.json"

    # Создаем полностью пустой файл
    src.write_text("", encoding="utf-8")

    # Проверяем что функция выбрасывает ValueError
    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))


def test_missing_file():
    """
    Тестирует обработку отсутствующего файла (негативный тест)

    Сценарий:
    1. Пытаемся конвертировать несуществующий файл
    2. Ожидаем FileNotFoundError
    """
    # Пытаемся конвертировать несуществующий файл
    with pytest.raises(FileNotFoundError):
        json_to_csv("no_such_file.json", "output.csv")


def test_invalid_suffix_to_json(tmp_path: Path):
    """
    Тестирует обработку файла с неправильным расширением (негативный тест)

    Сценарий:
    1. Создаем файл с расширением .txt вместо .csv
    2. Пытаемся конвертировать как CSV
    3. Ожидаем ValueError из-за ошибки парсинга CSV
    """
    src = tmp_path / "input.txt"
    dst = tmp_path / "output.json"

    # Создаем файл с неправильным содержимым для CSV
    src.write_text("This is 100% json, trust me", encoding="utf-8")

    # Проверяем что функция выбрасывает ValueError
    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))


def test_json_to_csv_different_field_sets(tmp_path: Path):
    """
    Тестирует JSON → CSV когда объекты имеют разные наборы полей

    Сценарий:
    1. Создаем JSON где объекты имеют разные поля
    2. Конвертируем в CSV
    3. Проверяем что все поля присутствуют в заголовке
    """
    src = tmp_path / "test.json"
    dst = tmp_path / "test.csv"

    # Данные с разными наборами полей
    data = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "city": "Moscow"},  # Другой набор полей
        {"age": 30, "country": "Russia"},  # Еще один набор полей
    ]

    src.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    json_to_csv(str(src), str(dst))

    # Проверяем результат
    with dst.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Должны быть все возможные поля
    assert set(rows[0].keys()) == {"name", "age", "city", "country"}
    # Проверяем что отсутствующие значения - пустые строки
    assert rows[1]["age"] == ""  # У Bob нет возраста
    assert rows[0]["city"] == ""  # У Alice нет города


def test_csv_to_json_with_empty_values(tmp_path: Path):
    """
    Тестирует CSV → JSON с пустыми значениями в CSV

    Сценарий:
    1. Создаем CSV с пустыми ячейками
    2. Конвертируем в JSON
    3. Проверяем что пустые значения корректно обработаны
    """
    src = tmp_path / "test.csv"
    dst = tmp_path / "test.json"

    # Создаем CSV с пустыми значениями
    with src.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
        writer.writeheader()
        writer.writerow({"name": "Alice", "age": "25", "city": "Moscow"})
        writer.writerow({"name": "Bob", "age": "", "city": ""})  # Пустые значения
        writer.writerow({"name": "", "age": "30", "city": "SPb"})  # Пустое имя

    csv_to_json(str(src), str(dst))

    # Читаем и проверяем результат
    data = json.loads(dst.read_text(encoding="utf-8"))

    assert len(data) == 3
    assert data[1]["age"] == ""  # Пустое значение должно сохраниться
    assert data[1]["city"] == ""  # Пустое значение должно сохраниться
    assert data[2]["name"] == ""  # Пустое имя


def test_csv_to_json_only_header(tmp_path: Path):
    """
    Тестирует CSV → JSON когда файл содержит только заголовок

    Сценарий:
    1. Создаем CSV только с заголовком
    2. Пытаемся конвертировать
    3. Ожидаем ValueError
    """
    src = tmp_path / "header_only.csv"
    dst = tmp_path / "output.json"

    # Создаем CSV только с заголовком
    src.write_text("name,age,city\n", encoding="utf-8")

    # Проверяем что функция выбрасывает ValueError
    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))


def test_json_to_csv_empty_array(tmp_path: Path):
    """
    Тестирует JSON → CSV когда JSON содержит пустой массив

    Сценарий:
    1. Создаем JSON с пустым массивом
    2. Конвертируем в CSV
    3. Проверяем что CSV файл создан, но не содержит данных (только заголовок)
    """
    src = tmp_path / "empty_array.json"
    dst = tmp_path / "output.csv"

    # Создаем JSON с пустым массивом
    src.write_text("[]", encoding="utf-8")

    # Конвертируем - не должно быть ошибки
    json_to_csv(str(src), str(dst))

    # Проверяем что CSV файл создан
    assert dst.exists()

    # Читаем CSV
    with dst.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Должно быть 0 строк данных
    assert len(rows) == 0


def test_csv_to_json_file_not_found():
    """
    Тестирует CSV → JSON когда файл не существует

    Сценарий:
    1. Пытаемся конвертировать несуществующий CSV файл
    2. Ожидаем FileNotFoundError
    """
    # Пытаемся конвертировать несуществующий файл
    with pytest.raises(FileNotFoundError):
        csv_to_json("no_such_file.csv", "output.json")


def test_json_to_csv_empty_file(tmp_path: Path):
    """
    Тестирует JSON → CSV когда JSON файл пустой (не содержит ничего)

    Сценарий:
    1. Создаем полностью пустой файл
    2. Пытаемся конвертировать
    3. Ожидаем ValueError
    """
    src = tmp_path / "empty.json"
    dst = tmp_path / "output.csv"

    # Создаем полностью пустой файл
    src.write_text("", encoding="utf-8")

    # Проверяем что функция выбрасывает ValueError
    with pytest.raises(ValueError):
        json_to_csv(str(src), str(dst))
