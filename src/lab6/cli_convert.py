import sys
import argparse
from lib import csv_to_xlsx, json_to_csv, csv_to_json
from ex1 import check_file


def main():
    # Настройка парсера аргументов
    parser = argparse.ArgumentParser(description="Конвертер данных")
    commands = parser.add_subparsers(dest="cmd", required=True)

    # Создаем команды
    cmd_list = ["json2csv", "csv2json", "csv2xlsx"]

    for cmd in cmd_list:
        # Создаем парсер для каждой команды
        cmd_parser = commands.add_parser(cmd)
        cmd_parser.add_argument(
            "--in", dest="input", required=True, help="Входной файл"
        )
        cmd_parser.add_argument(
            "--out", dest="output", required=True, help="Выходной файл"
        )

    # Получаем аргументы
    args = parser.parse_args()

    # Проверяем входной файл
    if not check_file(args.input):
        print(f"Ошибка: Файл {args.input} не существует")
        sys.exit(1)

    # Выбираем действие
    actions = {
        "json2csv": lambda: json_to_csv(args.input, args.output),
        "csv2json": lambda: csv_to_json(args.input, args.output),
        "csv2xlsx": lambda: csv_to_xlsx(args.input, args.output),
    }

    # Выполняем команду
    try:
        actions[args.cmd]()
        print(f"Успешно: {args.cmd}")
    except Exception as e:
        print(f"Ошибка конвертации: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
