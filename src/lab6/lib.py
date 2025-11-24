import csv
import json
import pandas as pd

def json_to_csv(json_file, csv_file):
    """Конвертирует JSON в CSV"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list) and len(data) > 0:
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    else:
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for key, value in data.items():
                writer.writerow([key, value])

def csv_to_json(csv_file, json_file):
    """Конвертирует CSV в JSON"""
    data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def csv_to_xlsx(csv_file, xlsx_file):
    """Конвертирует CSV в XLSX"""
    df = pd.read_csv(csv_file)
    df.to_excel(xlsx_file, index=False)
