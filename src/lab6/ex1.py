import os

def check_file(file_path):
    """Проверяет существование файла"""
    return os.path.isfile(file_path)
