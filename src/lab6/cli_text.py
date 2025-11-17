import sys
import os
import argparse
from lib import stats_text

def check_file(file_path):
    """Проверяет, существует ли файл"""
    if not os.path.isfile(file_path):
        print(f"Ошибка: файл '{file_path}' не найден", file=sys.stderr)
        return False
    return True

def show_file_content(file_path, show_numbers=False):
    """Показывает содержимое файла"""
    if not check_file(file_path):
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file, 1):
                if show_numbers:
                    print(f"{i:4}  {line}", end='')
                else:
                    print(line, end='')
    except Exception as e:
        print(f"Ошибка чтения: {e}", file=sys.stderr)
        sys.exit(1)

def analyze_file(file_path, top_words=5):
    """Анализирует частоту слов в файле"""
    if not check_file(file_path):
        return
    
    if top_words <= 0:
        print("Ошибка: --top должен быть больше 0", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            stats_text(text, top_words)
    except Exception as e:
        print(f"Ошибка анализа: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description="Утилита для работы с текстом")
    
    # Создаем подкоманды
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")
    
    # Команда cat
    cat_cmd = subparsers.add_parser("cat", help="Показать содержимое файла")
    cat_cmd.add_argument("--input", required=True, help="Путь к файлу")
    cat_cmd.add_argument("-n", action="store_true", help="Показать номера строк")
    
    # Команда stats
    stats_cmd = subparsers.add_parser("stats", help="Статистика слов")
    stats_cmd.add_argument("--input", required=True, help="Путь к файлу")
    stats_cmd.add_argument("--top", type=int, default=5, help="Количество топ-слов")
    
    # Разбираем аргументы
    args = parser.parse_args()
    
    # Выполняем команды
    if args.command == "cat":
        show_file_content(args.input, args.n)
    elif args.command == "stats":
        analyze_file(args.input, args.top)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()