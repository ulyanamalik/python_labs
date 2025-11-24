import sys, csv, os

sys.path.append(r"C:\Users\1\Documents\GitHub\ulyana\src")
from text3 import normalize, tokenize, top_n, count_freq
from io_txt_csv import read_text, write_csv, ensure_parent_dir

in1 = True
if in1:
    print("Режим один файл:")

    path = r"C:\Users\1\Documents\GitHub\ulyana\src\data\input.txt"
    text = read_text(path)
    words = tokenize(normalize(text))
    total_words = len(words)
    freqs = count_freq(words)
    unique_words = len(freqs)
    sorted_words = sorted(freqs.items(), key=lambda x: (-x[1], x[0]))

    output_dir = r"C:\Users\1\Documents\GitHub\ulyana\src\data"
    ensure_parent_dir(r"C:\Users\1\Documents\GitHub\ulyana\src\data")

    output_path = os.path.join(output_dir, "report.csv")
    with open(output_path, "w", encoding="cp65001", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        writer.writerows(sorted_words)

    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print("Топ-5:")
    for i in sorted_words:
        print(i[0], i[1])


# src/lab4/text_report.py


# import argparse
# import sys
# import csv
# from pathlib import Path
# from collections import Counter
# from project.lib.text import normalize, tokenize, calculate_frequencies  # Абсолютный импорт

# def main():
#     # Настройка парсера аргументов командной строки
#     parser = argparse.ArgumentParser(description="Анализ текста и создание отчета по частоте слов.")
#     parser.add_argument('--in', dest='input_file', type=str, default='data/input.txt',
#                         help='Путь к входному файлу.')
#     parser.add_argument('--out', dest='output_file', type=str, default='data/report.csv',
#                         help='Путь к выходному файлу отчета.')
#     parser.add_argument('--encoding', type=str, default='utf-8',
#                         help='Кодировка файла (например, utf-8, cp1251)')
#     args = parser.parse_args()

#     # Читаем входной файл
#     try:
#         with open(args.input_file, 'r', encoding=args.encoding) as f:
#             content = f.read().strip()
#     except FileNotFoundError:
#         print(f"Ошибка: файл '{args.input_file}' не найден.")
#         sys.exit(1)
#     except Exception as e:
#         print(f"Возникла проблема при обработке файла: {e}.")
#         sys.exit(1)

#     # Обрабатываем текст
#     normalized_text = normalize(content)
#     tokens = tokenize(normalized_text)
#     frequency_dict = calculate_frequencies(tokens)

#     # Сортируем список слов по убыванию частоты и лексикографически
#     sorted_freq = sorted(frequency_dict.items(),
#                        key=lambda item: (-item[1], item[0]))  # сортировка сначала по количеству, потом по слову

#     # Формируем отчет
#     output_path = Path(args.output_file)
#     output_path.parent.mkdir(parents=True, exist_ok=True)

#     with open(output_path, 'w', newline='', encoding='utf-8') as outf:
#         writer = csv.writer(outf)
#         writer.writerow(['word', 'count'])  # Заголовок таблицы
#         writer.writerows(sorted_freq)  # Данные по каждому слову

#     # Выводим краткую информацию в консоль
#     total_words = sum(frequency_dict.values())  # общее количество слов
#     unique_words = len(frequency_dict)          # уникальных слов
#     top_5 = sorted_freq[:5]                   # Топ-5 слов
