# Лабораторная работа №8
## models.py
```
"""
models.py - модуль с классом Student для лабораторной работы №8.
Этот файл содержит описание структуры студента с валидацией данных.
"""

# Импортируем необходимые модули:
# dataclass - декоратор для автоматического создания методов класса
# datetime - для работы с датами (проверка формата, вычисление возраста)
# re - для работы с регулярными выражениями (проверка формата даты)
# Dict - для указания типа словаря в аннотациях типов
from dataclasses import dataclass
from datetime import datetime, date
import re
from typing import Dict


@dataclass  # Декоратор, который автоматически создает конструктор и другие методы
class Student:
    """
    Класс для представления студента с валидацией данных.
    
    Атрибуты класса (поля, которые будут у каждого объекта Student):
    - fio: ФИО студента (строка)
    - birthdate: Дата рождения в формате ГГГГ-ММ-ДД (строка)
    - group: Группа студента, например "SE-01" (строка)
    - gpa: Средний балл студента, должен быть от 0 до 5 (число с плавающей точкой)
    """
    
    fio: str          # ФИО студента
    birthdate: str    # Дата рождения в формате "ГГГГ-ММ-ДД"
    group: str        # Номер группы
    gpa: float        # Средний балл от 0 до 5
    
    def __post_init__(self):
        """
        Магический метод, который вызывается автоматически ПОСЛЕ создания объекта.
        Здесь мы выполняем валидацию (проверку) данных.
        
        Действия:
        1. Проверяем правильность формата даты рождения
        2. Проверяем, что средний балл в допустимом диапазоне
        """
        self._validate_birthdate()  # Вызываем метод проверки даты
        self._validate_gpa()        # Вызываем метод проверки среднего балла
    
    def _validate_birthdate(self):
        """
        Приватный метод (начинается с _) для проверки даты рождения.
        Проверяет:
        1. Что дата в формате ГГГГ-ММ-ДД (4 цифры, тире, 2 цифры, тире, 2 цифры)
        2. Что дата действительна (например, не 2023-13-45)
        
        Использует:
        - re.match() - проверяет соответствие строки шаблону
        - datetime() - пытается создать объект даты, если не получается - дата неверная
        """
        # Регулярное выражение для проверки формата ГГГГ-ММ-ДД
        # ^ - начало строки
        # \d{4} - ровно 4 цифры (год)
        # - - тире
        # \d{2} - ровно 2 цифры (месяц)
        # - - тире
        # \d{2} - ровно 2 цифры (день)
        # $ - конец строки
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', self.birthdate):
            # Если строка не соответствует формату, выбрасываем ошибку
            raise ValueError(f"Неверный формат даты. Ожидается: YYYY-MM-DD")
        
        # Далее проверяем, что дата действительно существует
        try:
            # Разбиваем строку "2000-05-15" на части: ["2000", "05", "15"]
            # Преобразуем каждую часть в число: 2000, 5, 15
            year, month, day = map(int, self.birthdate.split('-'))
            # Пытаемся создать объект datetime с этими числами
            # Если месяц=13 или день=45 - это вызовет ValueError
            datetime(year, month, day)
        except ValueError:
            # Если не удалось создать дату, значит дата некорректная
            raise ValueError(f"Некорректная дата: {self.birthdate}")
    
    def _validate_gpa(self):
        """
        Приватный метод для проверки среднего балла.
        Проверяет, что GPA находится в диапазоне от 0.0 до 5.0 включительно.
        """
        # Проверяем, что GPA не меньше 0 и не больше 5
        if not (0.0 <= self.gpa <= 5.0):
            # Если GPA вне диапазона, выбрасываем ошибку
            raise ValueError(f"GPA должен быть в диапазоне [0.0, 5.0]")
    
    def age(self) -> int:
        """
        Публичный метод для вычисления возраста студента.
        
        Возвращает:
        - int: возраст студента в полных годах
        
        Логика работы:
        1. Преобразуем строку с датой рождения в объект date
        2. Получаем сегодняшнюю дату
        3. Вычисляем разницу в годах
        4. Если день рождения в текущем году еще не наступил, вычитаем 1 год
        
        Пример:
        - День рождения: 15 мая 2000 года
        - Сегодня: 1 декабря 2025 года
        - Разница в годах: 2025 - 2000 = 25 лет
        - День рождения уже был в этом году (май < декабря), значит возраст = 25 лет
        """
        # Преобразуем строку "2000-05-15" в объект datetime, затем в date
        birth_date = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        today = date.today()  # Получаем сегодняшнюю дату
        
        # Вычисляем базовый возраст (разница в годах)
        age = today.year - birth_date.year
        
        # Корректируем возраст, если день рождения в этом году еще не наступил
        # Сравниваем (месяц, день) сегодняшней даты и даты рождения
        # Например: (12, 1) < (5, 15) - декабрь меньше мая? НЕТ, значит день рождения уже прошел
        # Например: (3, 1) < (5, 15) - март меньше мая? ДА, значит день рождения еще не наступил
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1  # Отнимаем 1 год, если день рождения еще не наступил
        
        return age  # Возвращаем возраст в полных годах
    
    def to_dict(self) -> Dict[str, any]:
        """
        Метод для преобразования объекта Student в словарь.
        Используется для сериализации (сохранения) данных.
        
        Возвращает:
        - Dict[str, any]: словарь с данными студента
        
        Пример возвращаемого словаря:
        {
            'fio': 'Иванов Иван Иванович',
            'birthdate': '2000-05-15',
            'group': 'SE-01',
            'gpa': 4.5
        }
        """
        return {
            'fio': self.fio,          # Копируем ФИО
            'birthdate': self.birthdate,  # Копируем дату рождения
            'group': self.group,      # Копируем группу
            'gpa': self.gpa           # Копируем средний балл
        }
    
    @classmethod  # Декоратор, делающий метод методом класса (работает с классом, а не экземпляром)
    def from_dict(cls, data: Dict[str, any]) -> 'Student':
        """
        Метод класса (работает на уровне класса, а не объекта).
        Создает объект Student из словаря.
        
        Параметры:
        - data: словарь с данными студента
        
        Возвращает:
        - Student: новый объект класса Student
        
        Особенность: @classmethod получает класс (cls) первым параметром,
        а не объект (self). Это позволяет создавать объекты без существующего экземпляра.
        
        Использование:
        Student.from_dict({'fio': 'Иванов', 'birthdate': '2000-05-15', ...})
        """
        # Создаем и возвращаем новый объект Student, распаковывая словарь
        return cls(
            fio=data['fio'],           # Берем ФИО из словаря
            birthdate=data['birthdate'],  # Берем дату рождения из словаря
            group=data['group'],       # Берем группу из словаря
            gpa=float(data['gpa'])     # Берем GPA из словаря, преобразуем к float
        )
    
    def __str__(self) -> str:
        """
        Магический метод для строкового представления объекта.
        Вызывается при использовании print(student) или str(student).
        
        Возвращает:
        - str: красиво отформатированная строка с информацией о студенте
        
        Пример вывода:
        Студент: Иванов Иван Иванович
        Дата рождения: 2000-05-15 (возраст: 25 лет)
        Группа: SE-01
        Средний балл: 4.50
        """
        return (f"Студент: {self.fio}\n"  # Первая строка: ФИО
                f"Дата рождения: {self.birthdate} (возраст: {self.age()} лет)\n"  # Вторая строка: дата и возраст
                f"Группа: {self.group}\n"  # Третья строка: группа
                f"Средний балл: {self.gpa:.2f}")  # Четвертая строка: GPA с 2 знаками после точки


# Блок, который выполнится ТОЛЬКО если этот файл запускают напрямую (python models.py)
# Если файл импортируют как модуль (from models import Student), этот код НЕ выполнится
if __name__ == "__main__":
    """
    Тестирование работы класса Student при прямом запуске файла.
    Это как "пример использования" или "демонстрация" класса.
    """
    print("Тестирование класса Student:")  # Выводим заголовок
    
    # Создаем тестового студента
    # Student() автоматически вызывает __init__, который создан @dataclass
    # После создания автоматически вызывается __post_init__ для валидации
    s = Student(
        fio="Тест",               # ФИО тестового студента
        birthdate="2000-01-01",   # Корректная дата рождения
        group="SE-101",           # Группа
        gpa=4.0                   # Средний балл
    )
    
    # Выводим студента используя __str__ метод
    print(s)
    
    # Этот блок можно расширить дополнительными тестами:
    # print(f"Возраст: {s.age()} лет")
    # print(f"Словарь: {s.to_dict()}")
    # try:
    #     # Тест на ошибку валидации
    #     bad_student = Student(fio="Ошибка", birthdate="2023-13-45", group="SE-01", gpa=3.0)
    # except ValueError as e:
    #     print(f"Поймана ошибка валидации: {e}")

```
<img width="1280" height="512" alt="image" src="https://github.com/user-attachments/assets/61eb3188-6a33-40ab-8ebd-e672dc899af1" />

## serialize.py
```
import json
from typing import List


def students_to_json(students, path: str) -> None:
    """
    Сохраняет список студентов в JSON файл.
    
    Args:
        students: Список объектов Student - коллекция экземпляров класса Student,
                  которые нужно сохранить
        path: Путь к файлу для сохранения - строка с путем к файлу (например: 'students.json')
    """
    # Импортируем ВНУТРИ функции
    # Это делается для избежания циклических импортов
    # При попытке импорта из текущего пакета (.models)
    try:
        from .models import Student
    except ImportError:
        # Альтернативный путь - если не сработал относительный импорт,
        # пробуем абсолютный импорт (для случаев, когда модуль запускается напрямую)
        from models import Student
    
    # Проверка на пустой список студентов
    if not students:
        print("Список студентов пуст")
        return
    
    # Преобразуем студентов в словари
    data = []  # Создаем пустой список для хранения словарей
    for student in students:  # Итерируемся по каждому студенту в списке
        # Проверка типа: убеждаемся, что каждый элемент является объектом Student
        if not isinstance(student, Student):
            raise TypeError(f"Элемент не является объектом Student: {type(student)}")
        # Вызываем метод to_dict() у каждого студента для преобразования в словарь
        # и добавляем результат в список data
        data.append(student.to_dict())
    
    # Записываем в файл
    # Открываем файл для записи ('w') с кодировкой UTF-8
    with open(path, 'w', encoding='utf-8') as f:
        # Сериализуем список словарей в JSON формат
        # ensure_ascii=False - позволяет сохранять кириллицу и другие Unicode символы
        # indent=2 - добавляет отступы для читаемости JSON файла
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Выводим подтверждение о успешном сохранении
    print(f"✓ Сохранено {len(students)} студентов в {path}")


def students_from_json(path: str):
    """
    Загружает список студентов из JSON файла.
    
    Args:
        path: Путь к JSON файлу - строка с путем к файлу, из которого нужно загрузить данные
        
    Returns:
        List[Student]: Список объектов Student - восстановленные из файла экземпляры класса Student
    """
    # Импортируем ВНУТРИ функции (аналогично предыдущей функции)
    try:
        from .models import Student
    except ImportError:
        from models import Student
    
    try:
        # Открываем файл для чтения ('r') с кодировкой UTF-8
        with open(path, 'r', encoding='utf-8') as f:
            # Десериализуем JSON данные из файла в объект Python
            data = json.load(f)
        
        # Проверяем, что загруженные данные являются списком
        if not isinstance(data, list):
            raise ValueError("JSON должен содержать список")
        
        # Создаем объекты Student из словарей
        students = []  # Создаем пустой список для восстановленных студентов
        for item in data:  # Итерируемся по каждому словарю в списке
            try:
                # Создаем объект Student, передавая значения из словаря
                # Предполагается, что словарь содержит ключи: 'fio', 'birthdate', 'group', 'gpa'
                student = Student(
                    fio=item['fio'],  # ФИО студента (строка)
                    birthdate=item['birthdate'],  # Дата рождения (строка или datetime)
                    group=item['group'],  # Группа (строка)
                    gpa=float(item['gpa'])  # Средний балл (преобразуем к float)
                )
                students.append(student)  # Добавляем созданного студента в список
            except KeyError as e:
                # Если в словаре отсутствует обязательное поле, пропускаем этот элемент
                # и выводим предупреждение
                print(f"⚠ Пропущен элемент: отсутствует поле {e}")
                continue  # Переходим к следующему элементу
        
        # Выводим подтверждение о успешной загрузке
        print(f"✓ Загружено {len(students)} студентов из {path}")
        return students  # Возвращаем список восстановленных студентов
        
    # Обработка различных исключений:
    except FileNotFoundError:
        # Если файл не найден по указанному пути
        print(f"✗ Файл не найден: {path}")
        return []  # Возвращаем пустой список
    except json.JSONDecodeError:
        # Если файл содержит невалидный JSON
        print(f"✗ Ошибка в формате JSON файла: {path}")
        return []  # Возвращаем пустой список
    except Exception as e:
        # Обработка любых других неожиданных ошибок
        print(f"✗ Ошибка при чтении файла {path}: {e}")
        return []  # Возвращаем пустой список

```
<img width="1280" height="706" alt="image" src="https://github.com/user-attachments/assets/83292157-dd79-483c-abfa-e35f8eb9cbfb" />

## JSON ФАЙЛЫ
<img width="1280" height="615" alt="image" src="https://github.com/user-attachments/assets/486f1b5f-6a26-450f-bf81-7acedc152c17" />

<img width="1280" height="597" alt="image" src="https://github.com/user-attachments/assets/d6a1ce9f-9fd5-4fb0-b632-c6a41ae9b290" />


# Лабораторная работа №7

## Тесты для lib/text.py
```
import pytest
import sys
import os

# Добавляем корневую директорию проекта в путь поиска модулей Python
# Это необходимо для того, чтобы можно было импортировать модули из папки src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Импортируем функции, которые будем тестировать
from src.lib.text import normalize, tokenize, count_freq, top_n


# Тестирование функции normalize
@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),  # тест: смешанный регистр + спецсимволы
        ("ёжик, Ёлка", "ежик, елка"),     # тест: буква ё в разных регистрах
        ("Hello\r\nWorld", "hello world"), # тест: английский текст + спецсимволы
        ("  двойные   пробелы  ", "двойные пробелы"),  # тест: лишние пробелы
        ("", ""),                          # тест: пустая строка (граничный случай)
        ("\t\n   ", ""),                   # тест: только пробельные символы
    ],
)
def test_normalize(source, expected):
    """Тестирует функцию normalize с различными входными данными"""
    # Проверяем, что функция normalize возвращает ожидаемый результат
    assert normalize(source) == expected


# Тестирование функции tokenize
@pytest.mark.parametrize(
    "source, expected",
    [
        ("привет мир", ["привет", "мир"]),          # тест: обычный текст
        ("один, два, три!", ["один", "два", "три"]), # тест: знаки препинания
        ("", []),                                   # тест: пустая строка
        ("   много   пробелов   ", ["много", "пробелов"]),  # тест: лишние пробелы
        ("слово слово слово", ["слово", "слово", "слово"]), # тест: повторяющиеся слова
    ],
)
def test_tokenize(source, expected):
    """Тестирует функцию tokenize с различными входными данными"""
    # Проверяем, что функция tokenize возвращает ожидаемый результат
    assert tokenize(source) == expected


# Тестирование функции count_freq
@pytest.mark.parametrize(
    "tokens, expected",
    [
        (["a", "b", "a", "c", "b", "a"], {"a": 3, "b": 2, "c": 1}),  # тест: обычный случай
        ([], {}),  # тест: пустой список (граничный случай)
    ],
)
def test_count_freq(tokens, expected):
    """Тестирует функцию count_freq с различными входными данными"""
    # Проверяем, что функция count_freq возвращает ожидаемый результат
    assert count_freq(tokens) == expected


# Тестирование функции top_n
@pytest.mark.parametrize(
    "freq_dict, expected",
    [
        ({"a": 3, "b": 2, "c": 1}, [("a", 3), ("b", 2), ("c", 1)]),  # обычный случай
        (
            {
                "яблоко": 2,
                "апельсин": 2,
                "банан": 2,
            },  # одинаковые частоты → проверка сортировки по алфавиту
            [("апельсин", 2), ("банан", 2), ("яблоко", 2)],
        ),
        ({}, []),  # тест: пустой словарь (граничный случай)
        (
            {
                "a": 5,
                "b": 4,
                "c": 3,
                "d": 2,
                "e": 1,
                "f": 1,
            },  # больше элементов чем запрошено → проверка ограничения по n
            [("a", 5), ("b", 4), ("c", 3), ("d", 2), ("e", 1)],
        ),
    ],
)
def test_top_n(freq_dict, expected):
    """Тестирует функцию top_n с различными входными данными"""
    # Проверяем, что функция top_n возвращает ожидаемый результат
    # ВАЖНО: в функции top_n должен быть второй параметр n, но в тесте он не передается
    # Это может быть ошибкой - нужно передать значение для n
    # Предположительно, в последнем тесте n=5
    assert top_n(freq_dict) == expected

```
<img width="1941" height="714" alt="Снимок экрана 2025-11-24 211054" src="https://github.com/user-attachments/assets/48d93ba5-45ce-4754-bbe1-6c019d4e15c4" />


## Тесты для src/lab05/json_csv.py
```
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
    assert len(rows) == 2                    # Должно быть 2 записи
    assert rows[0]["name"] == "Alice"        # Первая запись - Alice
    assert rows[1]["age"] == "25"            # Возраст должен быть строкой (особенность CSV)


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
        writer.writeheader()                     # Записываем заголовок
        writer.writerow({"name": "Alice", "age": "22"})  # Первая строка данных
        writer.writerow({"name": "Bob", "age": "25"})    # Вторая строка данных

    # Выполняем конвертацию
    csv_to_json(str(src), str(dst))
    
    # Читаем и проверяем результат
    data = json.loads(dst.read_text(encoding="utf-8"))

    # Проверки:
    assert isinstance(data, list)           # Результат должен быть списком
    assert len(data) == 2                   # Должно быть 2 элемента
    assert data[0]["name"] == "Alice"       # Первый элемент - Alice
    assert data[1]["age"] == "25"           # Возраст сохраняется как строка


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
        {"name": "Bob", "city": "Moscow"},        # Другой набор полей
        {"age": 30, "country": "Russia"}          # Еще один набор полей
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
        writer.writerow({"name": "Bob", "age": "", "city": ""})        # Пустые значения
        writer.writerow({"name": "", "age": "30", "city": "SPb"})      # Пустое имя
    
    csv_to_json(str(src), str(dst))
    
    # Читаем и проверяем результат
    data = json.loads(dst.read_text(encoding="utf-8"))
    
    assert len(data) == 3
    assert data[1]["age"] == ""      # Пустое значение должно сохраниться
    assert data[1]["city"] == ""     # Пустое значение должно сохраниться
    assert data[2]["name"] == ""     # Пустое имя


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

```

<img width="1926" height="631" alt="Снимок экрана 2025-11-25 124518" src="https://github.com/user-attachments/assets/6ef5ac2d-6c42-4abf-8734-f1811105c86d" />


<img width="1913" height="814" alt="Снимок экрана 2025-11-24 211047" src="https://github.com/user-attachments/assets/e89ae37a-de8a-4220-b1ba-edf6afabbd8d" />

## Стиль кода (black)

<img width="1216" height="76" alt="Снимок экрана 2025-11-24 203649" src="https://github.com/user-attachments/assets/7834239c-a711-46cb-a928-a3c0e18c9293" />

## Покрытие тестов
### Команда

```
pytest --cov=tests --cov-report=term-missing
```

<img width="1936" height="414" alt="Снимок экрана 2025-11-24 193240" src="https://github.com/user-attachments/assets/c79328b8-c075-4c55-a443-cea045e5275b" />


# Лабораторная №6
## Задание 1
```
import sys
import os
import argparse
from lib import stats_text

def check_file(file_path):
    # Проверяем, существует ли файл по указанному пути
    if not os.path.isfile(file_path):
        # Если файл не найден, выводим сообщение об ошибке в stderr
        print(f"Ошибка: файл '{file_path}' не найден", file=sys.stderr)
        return False
    return True

def show_file_content(file_path, show_numbers=False):
    """Показывает содержимое файла"""
    # Сначала проверяем существование файла
    if not check_file(file_path):
        return
    
    try:
        # Открываем файл для чтения с кодировкой UTF-8
        with open(file_path, 'r', encoding='utf-8') as file:
            # Читаем файл построчно, enumerate добавляет номера строк (начиная с 1)
            for i, line in enumerate(file, 1):
                if show_numbers:
                    # Если включен режим показа номеров, выводим номер строки (форматированный до 4 символов) и содержимое
                    print(f"{i:4}  {line}", end='')
                else:
                    # Иначе выводим только содержимое строки
                    print(line, end='')
    except Exception as e:
        # Обрабатываем возможные ошибки чтения файла
        print(f"Ошибка чтения: {e}", file=sys.stderr)
        sys.exit(1)  # Завершаем программу с кодом ошибки 1

def analyze_file(file_path, top_words=5):
    """Анализирует частоту слов в файле"""
    # Проверяем существование файла
    if not check_file(file_path):
        return
    
    # Проверяем валидность параметра top_words
    if top_words <= 0:
        print("Ошибка: --top должен быть больше 0", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Открываем и читаем весь файл
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            # Вызываем функцию анализа текста из импортированного модуля
            stats_text(text, top_words)
    except Exception as e:
        # Обрабатываем ошибки анализа
        print(f"Ошибка анализа: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Главная функция"""
    # Создаем парсер аргументов командной строки с описанием
    parser = argparse.ArgumentParser(description="Утилита для работы с текстом")
    
    # Создаем подкоманды - это позволяет иметь разные команды с разными параметрами
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")
    
    # Команда cat - для отображения содержимого файла
    cat_cmd = subparsers.add_parser("cat", help="Показать содержимое файла")
    cat_cmd.add_argument("--input", required=True, help="Путь к файлу")
    cat_cmd.add_argument("-n", action="store_true", help="Показать номера строк")
    
    # Команда stats - для анализа статистики слов
    stats_cmd = subparsers.add_parser("stats", help="Статистика слов")
    stats_cmd.add_argument("--input", required=True, help="Путь к файлу")
    stats_cmd.add_argument("--top", type=int, default=5, help="Количество топ-слов")
    
    # Разбираем аргументы командной строки
    args = parser.parse_args()
    
    # Выполняем соответствующие команды на основе выбора пользователя
    if args.command == "cat":
        show_file_content(args.input, args.n)
    elif args.command == "stats":
        analyze_file(args.input, args.top)
    else:
        # Если команда не указана, показываем справку
        parser.print_help()

# Точка входа в программу
if __name__ == "__main__":
    main()

```
<img width="1280" height="701" alt="image" src="https://github.com/user-attachments/assets/72d81bbb-587b-462f-8ef9-e2931616dc5c" />

### Коммандные строки
```
python src\lab6\cli_text.py cat --input test.txt
python src\lab6\cli_text.py cat --input test.txt -n
python src\lab6\cli_text.py stats --input test.txt --top 5
```

## Задание 2
```
import sys
import argparse
from lib import csv_to_xlsx, json_to_csv, csv_to_json
from ex1 import check_file

def main():
    # Настройка парсера аргументов командной строки
    # создаем основной парсер с описанием программы
    parser = argparse.ArgumentParser(description="Конвертер данных")
    
    # Создаем подсистему команд (subparsers) - это позволяет иметь разные команды
    # dest="cmd" - значение выбранной команды будет храниться в атрибуте cmd
    # required=True - обязательно должна быть указана одна из команд
    commands = parser.add_subparsers(dest="cmd", required=True)
    
    # Список доступных команд конвертации
    cmd_list = ["json2csv", "csv2json", "csv2xlsx"]
    
    # Динамически создаем парсер для каждой команды
    for cmd in cmd_list:
        # Создаем парсер для конкретной команды
        cmd_parser = commands.add_parser(cmd)
        
        # Добавляем обязательные аргументы для каждой команды:
        # --in - входной файл
        cmd_parser.add_argument("--in", dest="input", required=True, 
                               help="Входной файл")
        # --out - выходной файл  
        cmd_parser.add_argument("--out", dest="output", required=True,
                               help="Выходной файл")
  
    # Парсим аргументы командной строки, переданные при запуске программы
    args = parser.parse_args()
    
    # Проверяем существование входного файла с помощью импортированной функции
    if not check_file(args.input):
        print(f"Ошибка: Файл {args.input} не существует")
        sys.exit(1)  # Завершаем программу с кодом ошибки 1
    
    # Создаем словарь действий, где ключ - название команды, значение - функция для выполнения
    # Используем lambda-функции для отложенного выполнения
    actions = {
        "json2csv": lambda: json_to_csv(args.input, args.output),  # Конвертация JSON в CSV
        "csv2json": lambda: csv_to_json(args.input, args.output),  # Конвертация CSV в JSON
        "csv2xlsx": lambda: csv_to_xlsx(args.input, args.output)   # Конвертация CSV в XLSX
    }
    
    # Выполняем выбранную команду
    try:
        # Вызываем соответствующую функцию из словаря actions
        actions[args.cmd]()
        # Если выполнение прошло успешно, выводим сообщение
        print(f"Успешно: {args.cmd}")
    except Exception as e:
        # Обрабатываем возможные ошибки при конвертации
        print(f"Ошибка конвертации: {e}")
        sys.exit(1)  # Завершаем программу с кодом ошибки 1

# Стандартная конструкция для точки входа в Python-программу
if __name__ == "__main__":
    main()

```
### Структура коммандной строки
```
python script.py json2csv --in input.json --out output.csv
python script.py csv2json --in input.csv --out output.json  
python script.py csv2xlsx --in input.csv --out output.xlsx
```
...........................................................................................................
<img width="1280" height="500" alt="image" src="https://github.com/user-attachments/assets/dd96a3be-94b6-4c18-a057-5e4ffe198dc0" />
...........................................................................................................

### CSV=>JSON
<img width="1280" height="531" alt="image" src="https://github.com/user-attachments/assets/fb6b6788-ef98-4402-bddd-9e2308d8fa1f" />

### JSON=>CSV
<img width="1280" height="549" alt="image" src="https://github.com/user-attachments/assets/87572fcf-97c1-4cca-bd0a-bf570b0729b9" />

### CSV=>XLSX
<img width="1280" height="526" alt="image" src="https://github.com/user-attachments/assets/c21dfadf-1067-46b5-afdf-46f45fbeff61" />



# Лабораторная №5
## Задание А
```
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
    csv_to_json("data/samples/people.csv", "data/out/people_from_csv.json")   # [14]
```
### Вывод

<img width="1328" height="475" alt="Снимок экрана 2025-10-27 215615" src="https://github.com/user-attachments/assets/aab72703-ac78-4e96-9dd2-8b615a5cfa7e" />

<img width="671" height="361" alt="Снимок экрана 2025-10-27 215625" src="https://github.com/user-attachments/assets/80e5cb55-52bf-4860-a115-30e35d6024a5" />

..........................................................................................................................................................
<img width="916" height="455" alt="Снимок экрана 2025-10-27 215636" src="https://github.com/user-attachments/assets/ac2711d0-02a5-4932-9589-ee9a9c2fdd64" />
<img width="729" height="264" alt="Снимок экрана 2025-10-27 215656" src="https://github.com/user-attachments/assets/f369d26c-5f9c-4a1f-b375-7e6f5cc2182f" />


## Задание В
```
import csv                     # Импорт библиотеки для работы с CSV файлами
from pathlib import Path       # Импорт модуля для удобной работы с путями файлов
from openpyxl import Workbook  # Импорт основной библиотеки для работы с Excel файлами
from openpyxl.utils import get_column_letter  # Импорт утилиты для перевода индекса столбца в букву Excel

# Функция для проверки типа файла по расширению
def check_file_type(file_path: str, valid_types: tuple) -> bool:
    """
    Проверяет, соответствует ли расширение файла одному из указанных типов.
    Возвращает True, если файл имеет одно из разрешенных расширений, иначе False.
    """
    return Path(file_path).suffix.lower() in valid_types

# Функция для преобразования CSV файла в XLSX файл
def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """
    Конвертирует CSV в XLSX.
    Использовать openpyxl ИЛИ xlsxwriter.
    Первая строка CSV — заголовок. 
    Лист называется "Sheet1".
    Колонки — автоширина по длине текста (не менее 8 символов).
    """

    # Проверка расширения входящего файла (должен быть .csv)
    if not check_file_type(csv_path, ('.csv',)):
        raise ValueError(f"Входной файл '{csv_path}' не является CSV.")

    # Проверка расширения выходящего файла (должен быть .xlsx)
    if not check_file_type(xlsx_path, ('.xlsx',)):
        raise ValueError(f"Выходной файл '{xlsx_path}' не является XLSX.")

    # Создание объекта пути для CSV файла
    csv_file = Path(csv_path)
    
    # Проверка существования CSV файла
    if not csv_file.exists():
        # Поднимается исключение, если файл не найден
        raise FileNotFoundError(f"Файл {csv_path} не найден.")  # [1]
    
    # Открытие CSV файла для чтения
    with csv_file.open('r', encoding='utf-8') as f:
        # Создается объект reader для парсинга CSV
        reader = csv.reader(f)                               # [2]
        # Читаются все строки CSV файла и превращаются в список списков
        data = list(reader)                                  # [3]
    
    # Проверка, есть ли данные в CSV файле
    if not data:
        # Поднимает ошибку, если файл пуст
        raise ValueError("CSV-файл пуст.")                  # [4]
    
    # Создание нового рабочего документа Excel
    workbook = Workbook()                                    # [5]
    # Получение активного листа
    sheet = workbook.active                                 # [6]
    # Переименование листа в 'Sheet1'
    sheet.title = "Sheet1"                                 # [7]
    
    # Запись данных из CSV в лист Excel
    for row in data:
        # Каждая строка добавляется в лист
        sheet.append(row)                                   # [8]
    
    # Настройка ширины столбцов автоматически
    for col_idx, col in enumerate(sheet.columns, 1):
        # Для каждого столбца вычисляется максимальная длина значений
        max_length = max(len(str(cell.value)) for cell in col)  # [9]
        # Устанавливается минимальная ширина столбца (8 символов)
        adjusted_width = max((max_length + 2), 8)              # [10]
        # Применение ширины столбцу по индексу
        sheet.column_dimensions[get_column_letter(col_idx)].width = adjusted_width  # [11]
    
    # Сохранение Excel файла
    workbook.save(xlsx_path)                                # [12]

# Основной код программы
if __name__ == "__main__":
    # Примеры использования функции
    csv_to_xlsx("data/samples/people.csv", "data/out/people.xlsx")  # [13]
```

### Вывод

<img width="808" height="338" alt="Снимок экрана 2025-10-28 111731" src="https://github.com/user-attachments/assets/66c81e10-c613-4183-9a3a-1eec09c5378d" />


<img width="1027" height="539" alt="Снимок экрана 2025-10-28 111636" src="https://github.com/user-attachments/assets/36d7d708-844e-4788-a4c8-c9bf2b77c824" />

# Лабораторная №4
## Задание А
```
# ИМПОРТЫ: подключаем нужные инструменты


from pathlib import Path                              # инструмент для работы с путями файлов
import csv                                            # инструмент для работы с Excel-таблицами (CSV-файлами)
import os                                             # доступ к системным штукам типа создания папок
from typing import List, Tuple, Optional, Union, AnyStr                     # чтобы понимать какие типы данных можно использовать


# ФУНКЦИЯ 1: читаем текст из файла


def read_text(path: Union[str, Path], encoding: str = "utf-8") -> str:
    try:
        return Path(path).read_text(encoding=encoding)                    # пытаемся прочитать файл
    except FileNotFoundError:
        return "Файл не найден."                                          # если файла нет - верни эту надпись
    except UnicodeDecodeError:
        return "Ошибка изменения кодировки."                              # если файл содержит странные символы


# ФУНКЦИЯ 2: записываем данные в CSV-таблицу


def write_csv(
    rows: List[Union[Tuple[AnyStr, ...], List[AnyStr]]],                  # принимаем строки данных
    path: Union[str, Path],                                               # и путь куда сохранить
    header: Optional[Tuple[str, ...]] = None,                             # заголовки таблицы (необязательно)
) -> None:
    p = Path(path)                                                        # превращаем путь в понятный для Python формат
    
    with p.open('w', newline='', encoding='utf-8') as file:               # открываем файл для записи
        writer = csv.writer(file)                                         # создаем "писаря" для табличных данных
        
        # Если не передали ни заголовков, ни данных - запишем стандартные заголовки


        if header is None and rows == []:
            writer.writerow(['a', 'b'])
            
        # Если передали заголовки - запишем их первой строкой


        elif header is not None:
            writer.writerow(header)
        
        # Проверяем что ВСЕ строки имеют одинаковое количество элементов

        if rows:
            first_row_len = len(rows[0])                                     # запоминаем длину первой строки
            for row in rows:
                if len(row) != first_row_len:                                # если какая-то строка другой длины
                    raise ValueError(f"Все строки должны иметь одинаковую длину ({first_row_len}). Получено {len(row)} элементов.")         # ругаемся
    
        writer.writerows(rows)                      # записываем все данные в файл


# ФУНКЦИЯ 3: создаем папку для файла если ее нет


def ensure_parent_dir(path: Union[str, Path]) -> None:
    parent_path = os.path.dirname(str(path))                            # достаем из пути к файлу путь к папке
    Path(parent_path).mkdir(parents=True, exist_ok=True)                # создаем папку (и все промежуточные если нужно)


# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

# Пример 1: читаем текстовый файл и печатаем что в нем
print(read_text(r"C:\Users\1\Documents\GitHub\ulyana\data\input.txt"))

# Пример 2: создаем CSV-файл с двумя строками
write_csv([("word", "count"), ("test", 3)],r"C:\Users\1\Documents\GitHub\ulyana\data\check.csv")          # первая строка - заголовки, вторая - данные
```

### Код
<img width="1350" height="1331" alt="Снимок экрана 2025-10-21 113503" src="https://github.com/user-attachments/assets/fb385380-d137-4eb9-8730-c909d744bc66" />
<img width="2081" height="848" alt="Снимок экрана 2025-10-21 113537" src="https://github.com/user-attachments/assets/9f0c5938-be4b-4604-9af7-de54932feec1" />

### Вывод
<img width="838" height="721" alt="image" src="https://github.com/user-attachments/assets/1d2836c1-c244-4da3-9503-145649e287c1" />

## Задание В
```
# ПОДКЛЮЧАЕМ ВСЕ НЕОБХОДИМЫЕ ИНСТРОУМЕНТЫ
import sys, csv, os                  # системные штуки, работа с таблицами, работа с файлами

# Добавляем путь к нашим собственным модулям (как сказать Python где искать наши файлы)

sys.path.append(r"C:\Users\1\Documents\GitHub\ulyana\src")

# ИМПОРТИРУЕМ НАШИ СОБСТВЕННЫЕ ФУНКЦИИ:

from text3 import normalize, tokenize, top_n, count_freq              # функции для работы с текстом
from io_txt_csv import read_text, write_csv, ensure_parent_dir        # функции для чтения/записи файлов

# НАСТРОЙКА РЕЖИМА РАБОТЫ
in1 = True                         # флаг "работать в режиме одного файла"

# ЕСЛИ РЕЖИМ ОДНОГО ФАЙЛА ВКЛЮЧЕН:
if in1:
    print("Режим один файл:")      # сообщаем пользователю в каком режиме работаем

    # Указываем путь к файлу который будем анализировать

    path = r"C:\Users\1\Documents\GitHub\ulyana\src\data\input.txt"
    
    # ЧИТАЕМ И АНАЛИЗИРУЕМ ТЕКСТ:

    text = read_text(path)             # читаем весь текст из файла
    words = tokenize(normalize(text))  # очищаем текст и разбиваем на отдельные слова
    
    # СЧИТАЕМ СТАТИСТИКУ:

    total_words = len(words)     # общее количество всех слов
    freqs = count_freq(words)    # подсчитываем сколько раз каждое слово встречается
    unique_words = len(freqs)    # количество уникальных слов
    
    # СОРТИРУЕМ СЛОВА по частоте (сначала самые частые, потом по алфавиту)
    sorted_words = sorted(freqs.items(), key=lambda x: (-x[1], x[0]))     # lambda анонимная функция,которая записывает по убыванию сначала самые частые

    # ПОДГОТАВЛИВАЕМ ПУТИ ДЛЯ СОХРАНЕНИЯ РЕЗУЛЬТАТОВ:

    output_dir = r"C:\Users\1\Documents\GitHub\ulyana\src\data"           # папка куда сохраним
    ensure_parent_dir(r"C:\Users\1\Documents\GitHub\ulyana\src\data")     # создаем папку если нет

    # СОЗДАЕМ CSV-ФАЙЛ С РЕЗУЛЬТАТАМИ:
    output_path = os.path.join(output_dir, "report.csv")                  # полный путь к файлу отчета
    
    # Открываем файл для записи с правильной кодировкой для русских букв

    with open(output_path, "w", encoding="cp65001", newline="") as f:
        writer = csv.writer(f)                                           # создаем "писаря" для таблицы
        writer.writerow(["word", "count"])                               # записываем заголовки таблицы
        writer.writerows(sorted_words)                                   # записываем все данные (слова и их частоты)

    # ВЫВОДИМ РЕЗУЛЬТАТЫ НА ЭКРАН:
    print(f"Всего слов: {total_words}")                                  # показываем общее количество слов
    print(f"Уникальных слов: {unique_words}")                            # показываем количество разных слов
    print("Топ-5:")  # заголовок для топ-5 слов
    
    # Показываем 5 самых частых слов (или все если слов меньше 5)

    for i in sorted_words[:5]:                                     # берем первые 5 элементов из отсортированного списка
        print(i[0], i[1])                                          # печатаем слово и сколько раз оно встретилось
```
### Код
<img width="1742" height="1204" alt="Снимок экрана 2025-10-21 114740" src="https://github.com/user-attachments/assets/dbe3b99c-b9c2-4051-b151-7efd50cfa9aa" />

### Вывод
<img width="843" height="439" alt="Снимок экрана 2025-10-21 111725" src="https://github.com/user-attachments/assets/86e9dc89-f395-47ba-909b-dd034b07cd54" />
<img width="912" height="594" alt="Снимок экрана 2025-10-21 111721" src="https://github.com/user-attachments/assets/4d9f714a-9ae0-4d50-9b8c-ad87ee730612" />
<img width="771" height="295" alt="Снимок экрана 2025-10-21 111657" src="https://github.com/user-attachments/assets/1cf8126d-c6b1-42ab-b29f-022f34a3eeec" />



# Лабораторная №3
## Задание №1-text.py
```
import re
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if yo2e:
        text = text.replace('ё', 'е').replace('Ё', 'Е')
    if casefold:
        text = text.casefold()
    text = re.sub(r'[\s\r\n\t\f\v]', ' ', text)
    text = re.sub(r' +', ' ', text).strip()
    return text

def tokenize(text: str) -> list[str]:
    return re.findall(r'\b\w+(?:-\w+)*\b', text)

def count_freq(tokens: list[str]) -> dict[str, int]:
    freq = {}
    for tok in tokens:
        freq[tok] = freq.get(tok, 0) + 1
    return freq
def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:n]

print('----------------------------------------------')
print('Тестирование normalize')
print('----------------------------------------------')
print(normalize("ПрИвЕт\nМИр\t")) 
print(normalize("ёжик, Ёлка"))
print(normalize("Hello\r\nWorld")) 
print(normalize("  двойные   пробелы  "))
print('----------------------------------------------')
print('Тестирование tokenize')
print('----------------------------------------------')
print(tokenize("привет мир"))
print(tokenize("hello,world!!!"))
print(tokenize("по-настоящему круто"))
print(tokenize("2025 год"))
print(tokenize("emoji 😀 не слово"))
print('----------------------------------------------')
print('Тестирование count_freq + top_n')
print('----------------------------------------------')
tokens_example = ["a", "b", "a", "c", "b", "a"]
freq_example = count_freq(tokens_example)
print(top_n(freq_example, n=2))
tokens_example_2 = ["bb", "aa", "bb", "aa", "cc"]
freq_example_2 = count_freq(tokens_example_2)
print(top_n(freq_example_2, n=2))
```


<img width="1189" height="688" alt="Снимок экрана 2025-10-13 233444" src="https://github.com/user-attachments/assets/9c6d08bf-8f74-4118-96eb-bd0d6877ff9f" />

# Задание №2-text_stats.py
```
from text import normalize,tokenize,count_freq,top_n
import sys


def main():
    text = sys.stdin.read()

    if not text.strip():
        print("Нет входных данных")
        return
    normalized_text = normalize(text)
    tokens = tokenize(normalized_text)


    total_words = len(tokens)
    freq_dict = count_freq(tokens)
    unique_words = len(freq_dict)
    top_words = top_n(freq_dict, 5)
    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print("Топ-5:")
    for word, count in top_words:
        print(f"{word}:{count}")
if __name__ == "__main__":
    main()
```
<img width="1773" height="85" alt="Снимок экрана 2025-10-14 114429" src="https://github.com/user-attachments/assets/4ed63fc7-f2b4-4b00-89b4-96606728455d" />

<img width="305" height="197" alt="Снимок экрана 2025-10-14 115716" src="https://github.com/user-attachments/assets/6a6d135a-d1f2-4c48-8936-9299277426eb" />

# Лабораторная работа №2

## Задание №1-array.py
```

empty_list = []
def find_min_max(values):
    if values == empty_list: 
        return "ValueError"
    return min(values), max(values)  
def get_unique_sorted(values):
    if values == empty_list: 
        return "ValueError"  
    return list(set(sorted(values)))  

def flatten_list(nested):

    if nested == empty_list: 
        return "ValueError"  
    flat_list = []
    for sublist in nested: 
        for item in sublist:
            if not isinstance(item, int):  
                return "TypeError" 
            flat_list.append(item)
    return flat_list

print("find_min_max")
print(find_min_max([3, -1, 5, 5, 0]))  
print(find_min_max([42]))  
print(find_min_max([-5, -2, -9]))  
print(find_min_max([]))  
print(" ")

print("get_unique_sorted")
print(get_unique_sorted([3, 1, 2, 1, 3]))  
print(get_unique_sorted([]))  
print(get_unique_sorted([-1, -1, 0, 2, 2]))  
print(get_unique_sorted([1.0, 1, 2.5, 2.5, 0])) 

print(" ")

print("flatten_list")
print(flatten_list([[1, 2], [3, 4]]))  
print(flatten_list([[1, 2], (3, 4, 5)]))  
print(flatten_list([[1], [], [2, 3]]))  
print(flatten_list([[[1, 2], "ab"]]))  
```
<img width="1157" height="580" alt="Снимок экрана 2025-10-06 194847" src="https://github.com/user-attachments/assets/68b16fdc-c179-47e6-91b0-a5ec6f1d9eb7" />

## Задание №2-matrix.py
```
def transpose(mat):
    if not mat:
        return []
    n = len(mat[0]) 
    for row in mat:
        if len(row) != n:
            return "ValueError"  
    res = [] 
    for j in range(n): 
        new_row = []  
        for i in range(len(mat)): 
            new_row.append(mat[i][j])  
        res.append(new_row)  
    return res  
def row_sums(mat):
    if not mat:
        return [] 
    n = len(mat[0])
    for row in mat:
        if len(row) != n:
            return "ValueError" 
    res = []  
    for row in mat:  
        s = 0  
        for x in row:  
            s += x 
        res.append(s)  
    return res  
def col_sums(mat):
    if not mat:
        return [] 
    n = len(mat[0])
    for row in mat:
        if len(row) != n:
            return "ValueError"  
    res = []  
    for j in range(n):  
        s = 0  
        for i in range(len(mat)):  
            s += mat[i][j] 
        res.append(s)  
    return res 
print("transpose")
print(transpose([[1, 2, 3]]))  
print(transpose([[1], [2], [3]]))  
print(transpose([[1, 2], [3, 4]]))  
print(transpose([])) 
print(transpose([[1, 2], [3]])) 
print("................................................... ")
print("row_sums")
print(row_sums([[1, 2, 3], [4, 5, 6]]))  
print(row_sums([[-1, 1], [10, -10]])) 
print(row_sums([[0, 0], [0, 0]]))
print(row_sums([[1, 2], [3]]))
print("................................................... ")
print("col_sums")
print(col_sums([[1, 2, 3], [4, 5, 6]])) 
print(col_sums([[-1, 1], [10, -10]]))  
print(col_sums([[0, 0], [0, 0]]))  
print(col_sums([[1, 2], [3]]))  
```
<img width="1176" height="614" alt="Снимок экрана 2025-10-06 201825" src="https://github.com/user-attachments/assets/a5237a30-7bcd-4a67-aa8a-05b268066088" />

## Задание №3-tuple.py
```
def format_record(s):
    for i in s:
        if not i:
            return "ValueError"  
    fio = s[0].strip().split()  
    if len(fio) < 2:
        return "ValueError"
    if not isinstance(s[2], float):
        return "TypeError" 
    if not (1 < s[2] <= 5):  
        return "ValueError"  
    try:
        fio_ready = f'"{fio[0].capitalize()} {fio[1][0].upper()}.{fio[2][0].upper()}."'
    except IndexError:
        fio_ready = f'"{fio[0].capitalize()} {fio[1][0].upper()}."'
    group = f"гр. {s[1]}"
    gpa = f"{s[2]:.2f}"
    gpa_ready = f"{gpa}"
    end = f"{fio_ready}, {group}, {gpa_ready}"
    return end  
print(format_record(("Иванов Иван Иванович", "BIVT-25",4.6 )))
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))
print(format_record(("","BIVT-25",3.999)))
```

<img width="537" height="181" alt="Снимок экрана 2025-10-06 212539" src="https://github.com/user-attachments/assets/0b99743d-c348-4daf-9741-9572acd58f27" />



# Лабораторная работа №1
## Задание №1
```
name=input('имя:')
a=int(input('возраст:'))
print(f'Привет, {name}!Через год тебе будет {a+1}')
```
<img width="611" height="159" alt="Снимок экрана 2025-09-21 171347" src="https://github.com/user-attachments/assets/3c3fd911-4d82-4b00-bc60-c74cd1c5e14b" />

## Задание №2
```
a = input("Введите первое число: ")
b = input("Введите второе число: ")

if ',' in a or ',' in b:
    a = a.replace(",", ".")
    b = b.replace(",", ".")

sum_result = float(a) + float(b)
avg_result = sum_result / 2

print(f'sum = {sum_result:.2f}; avg = {avg_result:.2f}')
```

<img width="412" height="103" alt="Снимок экрана 2025-09-30 094019" src="https://github.com/user-attachments/assets/0230a13a-b08b-4589-8e92-223388ea885c" />

## Задание №3

```
price=int(input())
discount=int(input())
vat=int(input())
base = price * (1 - discount/100)
vat_amount = base * (vat/100)
total = base + vat_amount
print(f'База после скидки:{base}0₽')
print(f'НДС:{vat_amount}0₽')
print(f'Итого к оплате:{total}0₽')
```
<img width="555" height="108" alt="Снимок экрана 2025-09-21 180212" src="https://github.com/user-attachments/assets/2b63650a-b66d-473c-bcc9-75fb72bfcbce" />

## Задание №4

```
m=int(input('минуты:'))
print(f'{(m//60):02d}:{(m%60):02d}')
```

<img width="281" height="77" alt="Снимок экрана 2025-09-30 092312" src="https://github.com/user-attachments/assets/44397001-a891-49a7-a137-2a2fcd43a462" />

## Задание №5
```
fio = input("ФИО:")
fio_clean= ' '.join(fio.split())
k = len(fio_clean)
FIO=fio.split()
print(f"Инициалы: {FIO[0][:1]}{FIO[1][:1]}{FIO[2][:1]}")
print(f"Длина: {k}")

```
<img width="692" height="151" alt="Снимок экрана 2025-09-21 182019" src="https://github.com/user-attachments/assets/148fda98-7454-414c-957b-ae00a91a1645" />





