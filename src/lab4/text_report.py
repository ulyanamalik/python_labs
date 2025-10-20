import argparse
import sys
import csv
from pathlib import Path
from collections import Counter
from lib.text import normalize, tokenize, calculate_frequencies

def main():
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description="Анализ текста и создание отчета по частоте слов.")
    parser.add_argument('--in', dest='input_file', type=str, default='data/input.txt',
                        help='Путь к входному файлу.')
    parser.add_argument('--out', dest='output_file', type=str, default='data/report.csv',
                        help='Путь к выходному файлу отчета.')
    parser.add_argument('--encoding', type=str, default='utf-8',
                        help='Кодировка файла (например, utf-8, cp1251)')
    args = parser.parse_args()

    # Читаем входной файл
    try:
        with open(args.input_file, 'r', encoding=args.encoding) as f:
            content = f.read().strip()
    except FileNotFoundError:
        print(f"Ошибка: файл '{args.input_file}' не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Возникла проблема при обработке файла: {e}.")
        sys.exit(1)

    # Обрабатываем текст
    normalized_text = normalize(content)
    tokens = tokenize(normalized_text)
    frequency_dict = calculate_frequencies(tokens)

    # Сортируем список слов по убыванию частоты и лексикографически
    sorted_freq = sorted(frequency_dict.items(),
                       key=lambda item: (-item[1], item[0]))  # сортировка сначала по количеству, потом по слову

    # Формируем отчет
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as outf:
        writer = csv.writer(outf)
        writer.writerow(['word', 'count'])  # Заголовок таблицы
        writer.writerows(sorted_freq)  # Данные по каждому слову

    # Выводим краткую информацию в консоль
    total_words = sum(frequency_dict.values())  # общее количество слов
    unique_words = len(frequency_dict)          # уникальных слов
    top_5 = sorted_freq[:5]                   # Топ-5 слов

    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print("Топ-5 слов:")
    for word, count in top_5:
        print(f"{word}: {count}")

if __name__ == '__main__':
    main()