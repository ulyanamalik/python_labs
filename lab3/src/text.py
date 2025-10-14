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

