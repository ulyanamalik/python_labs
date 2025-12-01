import json
from typing import List

# Используем абсолютный импорт с обработкой ошибок
try:
    # Пытаемся импортировать как модуль из пакета
    from .models import Student
except ImportError:
    # Если не работает (например, при прямом запуске из папки lab8)
    # пробуем прямой импорт
    try:
        from models import Student
    except ImportError as e:
        print(f"Ошибка импорта Student: {e}")
        raise


def students_to_json(students: List[Student], path: str) -> None:
    """Сохраняет список студентов в JSON файл"""
    data = [student.to_dict() for student in students]
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Данные сохранены в {path}")


def students_from_json(path: str) -> List[Student]:
    """Загружает список студентов из JSON файла"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        students = []
        for item in data:
            try:
                # Используем уже импортированный класс Student
                student = Student.from_dict(item)
                students.append(student)
            except (KeyError, ValueError) as e:
                print(f"Пропущен элемент: {e}")
                continue
        
        print(f"Загружено студентов: {len(students)}")
        return students
        
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка JSON в файле {path}: {e}")
        return []


# Тестирование при запуске файла
if __name__ == "__main__":
    print("="*60)
    print("Тестирование модуля serialize.py")
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
    import os
    os.makedirs("../../data/lab8", exist_ok=True)
    
    # Тестируем students_to_json
    output_path = "../../data/lab8/students_output.json"
    print(f"\n2. Сохраняем в {output_path}")
    students_to_json(students, output_path)
    
    # Тестируем students_from_json
    print(f"\n3. Загружаем из {output_path}")
    loaded_students = students_from_json(output_path)
    
    if loaded_students:
        print(f"\n4. Загруженные студенты:")
        for i, student in enumerate(loaded_students, 1):
            print(f"   {i}. {student}")
    
    print("\n" + "="*60)
    print("serialize.py выполнен успешно!")
    print("="*60)
