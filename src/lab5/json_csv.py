import json
import csv
from pathlib import Path

def json_to_csv(json_path: str, csv_path: str) -> None:

    json_file = Path(json_path)
    if not json_file.exists():
        raise FileNotFoundError(f"Файл {json_path} не найден.")
    
    with json_file.open('r', encoding='utf-8') as f:
        data = json.load(f)

   
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("JSON должен содержать список словарей.")

    headers = set()
    for item in data:
        headers.update(item.keys())
    headers = sorted(headers)  

    with Path(csv_path).open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

def csv_to_json(csv_path: str, json_path: str) -> None:
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"Файл {csv_path} не найден.")

    with csv_file.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    if not data:
        raise ValueError("CSV-файл пуст.")

    with Path(json_path).open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    json_to_csv("data/samples/people.json", "data/out/people_from_json.csv")
    csv_to_json("data/samples/people.csv", "data/out/people_from_csv.json")