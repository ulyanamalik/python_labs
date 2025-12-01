#!/usr/bin/env python3
"""Тестовый скрипт для проверки лабораторной работы №8"""

import sys
import os
import json

# Добавляем src в путь Python
sys.path.insert(0, 'src')

print("="*60)
print("ТЕСТИРОВАНИЕ ЛАБОРАТОРНОЙ РАБОТЫ №8")
print("="*60)

try:
    from lab8.models import Student
    from lab8.serialize import students_to_json, students_from_json
    print(" Модули успешно импортированы")
except ImportError as e:
    print(f" Ошибка импорта: {e}")
    sys.exit(1)

# Тест 1: Класс Student
print("\n1. Тестирование класса Student:")
student = Student(
    fio="Иванов Иван Иванович",
    birthdate="2000-05-15",
    group="SE-01",
    gpa=4.5
)
print(f"   Создан: {student}")
print(f"   Возраст: {student.age()} лет")
print(f"   Словарь: {student.to_dict()}")

# Тест 2: Валидация
print("\n2. Тестирование валидации:")
try:
    Student(fio="Тест", birthdate="2023-13-45", group="SE-01", gpa=3.0)
    print("   ✗ Ожидалась ошибка даты")
except ValueError as e:
    print(f"   ✓ Валидация даты: {e}")

try:
    Student(fio="Тест", birthdate="2000-01-01", group="SE-01", gpa=6.0)
    print("   ✗ Ожидалась ошибка GPA")
except ValueError as e:
    print(f"    Валидация GPA: {e}")

# Тест 3: Сериализация
print("\n3. Тестирование сериализации:")
students = [student]

os.makedirs("data/lab8", exist_ok=True)

output_path = "data/lab8/test_output.json"
students_to_json(students, output_path)
print(f"    Данные сохранены в {output_path}")

loaded = students_from_json(output_path)
print(f"   Загружено студентов: {len(loaded)}")

# Проверяем содержимое входного файла
input_path = "data/lab8/students_input.json"
print(f"\n4. Проверка входного файла {input_path}:")
if os.path.exists(input_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Проверяем, что файл не пустой
            if content.strip():
                data = json.loads(content)
                print(f"    Файл содержит валидный JSON")
                print(f"   Количество записей: {len(data)}")
                
                # Загружаем студентов из входного файла
                input_students = students_from_json(input_path)
                print(f"   Загружено студентов: {len(input_students)}")
                
                if input_students:
                    print(f"\n   Студенты из входного файла:")
                    for i, s in enumerate(input_students[:3], 1):
                        print(f"   {i}. {s}")
                    if len(input_students) > 3:
                        print(f"   ... и еще {len(input_students) - 3} студентов")
            else:
                print(f"    Файл пустой")
    except json.JSONDecodeError as e:
        print(f"    Ошибка JSON: {e}")
        print(f"   Содержимое файла: {content[:100]}...")
    except Exception as e:
        print(f"    Ошибка: {e}")
else:
    print(f"    Файл не найден")

print("\n" + "="*60)
print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
print("="*60)
