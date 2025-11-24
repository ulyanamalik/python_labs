import re
from collections import Counter
from typing import Dict, List, Tuple


def normalize(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = text.replace("ё", "е")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> List[str]:
    if not text:
        return []
    tokens = re.findall(r"[а-яa-z]+", text, flags=re.IGNORECASE)
    return tokens


def count_freq(tokens: List[str]) -> Dict[str, int]:
    return dict(Counter(tokens))


def top_n(freq: Dict[str, int], n: int) -> List[Tuple[str, int]]:
    if not freq:
        return []
    sorted_items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return sorted_items[:n]
