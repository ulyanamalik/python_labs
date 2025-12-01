from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict


@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

    def __post_init__(self):
        # Исправленная валидация формата даты и диапазона gpa
        try:
            datetime.strptime(self.birthdate, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Неверный формат даты: {self.birthdate}. Ожидается YYYY-MM-DD")
        
        if not (0 <= self.gpa <= 5):
            raise ValueError(f"GPA должен быть в диапазоне от 0 до 5. Получено: {self.gpa}")

    def age(self) -> int:
        # Исправленный расчет возраста
        birth_date = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        today = date.today()
        
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        return age

    def to_dict(self) -> Dict[str, any]:
        # Исправленный to_dict - правильные поля
        return {
            "fio": self.fio,
            "birthdate": self.birthdate,
            "group": self.group,
            "gpa": self.gpa
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'Student':
        # Исправленный from_dict - создает объект Student
        return cls(
            fio=data["fio"],
            birthdate=data["birthdate"],
            group=data["group"],
            gpa=float(data["gpa"])
        )

    def __str__(self) -> str:
        # Исправленный __str__ - возвращает строку
        return f"Студент: {self.fio}, группа: {self.group}, GPA: {self.gpa:.2f}"


# Тестирование при запуске файла
if __name__ == "__main__":
    print("="*60)
    print("Тестирование класса Student из models.py")
    print("="*60)
    
    # Создание студента
    student = Student(
        fio="Иванов Иван Иванович",
        birthdate="2000-05-15",
        group="SE-01",
        gpa=4.5
    )
    
    print(f"\n1. Создан студент: {student}")
    print(f"   Возраст: {student.age()} лет")
    
    # Тест to_dict
    print(f"\n2. Метод to_dict(): {student.to_dict()}")
    
    # Тест from_dict
    print("\n3. Метод from_dict():")
    data = {"fio": "Петрова Анна Сергеевна", "birthdate": "2001-11-23", "group": "SE-02", "gpa": 3.8}
    student2 = Student.from_dict(data)
    print(f"   Создан: {student2}")
    
    # Тест валидации
    print("\n4. Тест валидации:")
    try:
        Student(fio="Тест", birthdate="2023-13-45", group="SE-01", gpa=3.0)
    except ValueError as e:
        print(f"    Ошибка даты: {e}")
    
    try:
        Student(fio="Тест", birthdate="2000-01-01", group="SE-01", gpa=6.0)
    except ValueError as e:
        print(f"    Ошибка GPA: {e}")
    
    print("\n" + "="*60)
    print("models.py выполнен успешно!")
    print("="*60)
