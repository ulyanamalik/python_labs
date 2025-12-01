#!/usr/bin/env python3
"""Запуск serialize.py из корня проекта"""

import sys
import os

# Добавляем src в путь Python
sys.path.insert(0, 'src')

# Импортируем и запускаем тестирование
from lab8.serialize import students_to_json, students_from_json
from lab8.models import Student

print("="*60)
print("ЗАПУСК МОДУЛЯ SERIALIZE.PY ИЗ КОРНЯ ПРОЕКТА")
print("="*60)

# Создаем студентов
students = [
    Student(fio="Иванов Иван Иванович", birthdate="2000-05-15", group="SE-01", gpa=4.5),
    Student(fio="Петрова Анна Сергеевна", birthdate="2001-11-23", group="SE-02", gpa=3.8),
    Student(fio="Сидоров Алексей Петрович", birthdate="1999-02-10", group="AI-01", gpa=4.9)
]

print(f"\n1. Создано студентов: {len(students)}")
for i, student in enumerate(students, 1):
    print(f"   {i}. {student}")

# Создаем папку если нет
os.makedirs("data/lab8", exist_ok=True)

# Тестируем students_to_json
output_path = "data/lab8/students_output.json"
print(f"\n2. Сохраняем в {output_path}")
students_to_json(students, output_path)

# Тестируем students_from_json
print(f"\n3. Загружаем из {output_path}")
loaded_students = students_from_json(output_path)

if loaded_students:
    print(f"\n4. Загруженные студенты:")
    for i, student in enumerate(loaded_students, 1):
        print(f"   {i}. {student}")

# Проверяем входной файл
input_path = "data/lab8/students_input.json"
if os.path.exists(input_path):
    print(f"\n5. Загрузка из входного файла {input_path}:")
    input_students = students_from_json(input_path)
    if input_students:
        print(f"   Загружено студентов: {len(input_students)}")
    else:
        print("   Не удалось загрузить студентов из входного файла")
else:
    print(f"\n5. Входной файл не найден: {input_path}")

print("\n" + "="*60)
print("serialize.py выполнен успешно из корня проекта!")
print("="*60)
