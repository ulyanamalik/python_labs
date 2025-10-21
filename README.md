# Лабораторная №4
## Задание А-text.py
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





