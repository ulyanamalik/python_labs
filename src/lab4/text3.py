import re
from collections import Counter

def normalize(text):
    normalized = text.lower()
    normalized = re.sub(r'[^\w\s]', '', normalized)  # удаляем знаки пунктуации
    return normalized.strip()

def tokenize(text):
    tokens = text.split()
    return tokens

def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:n]

def count_freq(tokens):
    frequencies = Counter(tokens)
    return frequencies