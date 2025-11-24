import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.lib.text import normalize, tokenize, count_freq, top_n


def test_normalize():
    assert normalize("ПРИВЕТ МИР") == "привет мир"
    assert normalize("") == ""


def test_tokenize():
    assert tokenize("привет мир") == ["привет", "мир"]
    assert tokenize("") == []


def test_count_freq():
    tokens = ["я", "ты", "я", "мы"]
    result = count_freq(tokens)
    assert result == {"я": 2, "ты": 1, "мы": 1}


def test_top_n():
    freq = {"я": 3, "ты": 2, "мы": 1}
    result = top_n(freq, 2)
    assert result == [("я", 3), ("ты", 2)]
