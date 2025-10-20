import re
from collections import Counter

def normalize(text):
    """
    Простая нормализация текста:
    - Преобразование символов в нижний регистр
    - Удаление знаков препинания и ненужных символов
    """
    normalized = text.lower()
    normalized = re.sub(r'[^\w\s]', '', normalized)  # удаляем знаки пунктуации
    return normalized.strip()

def tokenize(text):
    """
    Токенизация текста: разделение на отдельные слова.
    """
    tokens = text.split()
    return tokens

def calculate_frequencies(tokens):
    """
    Подсчет частот слов.
    Возвращает словарь вида {слово: частота}
    """
    frequencies = Counter(tokens)
    return frequencies