from pathlib import Path
import csv
import os
from typing import List, Tuple, Optional, Union, AnyStr


def read_text(path: Union[str, Path], encoding: str = "utf-8") -> str:
    try:
        return Path(path).read_text(encoding=encoding)
    except FileNotFoundError:
        return "Файл не найден."
    except UnicodeDecodeError:
        return "Ошибка изменения кодировки."


def write_csv(
    rows: List[Union[Tuple[AnyStr, ...], List[AnyStr]]],
    path: Union[str, Path],
    header: Optional[Tuple[str, ...]] = None,
) -> None:
    p = Path(path)
    with p.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if header is None and rows == []:
            writer.writerow(["a", "b"])

        elif header is not None:
            writer.writerow(header)

        if rows:
            first_row_len = len(rows[0])
            for row in rows:
                if len(row) != first_row_len:
                    raise ValueError(
                        f"Все строки должны иметь одинаковую длину ({first_row_len}). Получено {len(row)} элементов."
                    )

        writer.writerows(rows)


def ensure_parent_dir(path: Union[str, Path]) -> None:
    parent_path = os.path.dirname(str(path))
    Path(parent_path).mkdir(parents=True, exist_ok=True)


print(read_text(r"C:\Users\1\Documents\GitHub\ulyana\data\input.txt"))

# Запись CSV-файла
write_csv(
    [("word", "count"), ("test", 3)],
    r"C:\Users\1\Documents\GitHub\ulyana\data\check.csv",
)
