import csv
from collections import defaultdict

def read_csv(filename):
    data = defaultdict(dict)
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        headers = next(reader)
        for row in reader:
            key = tuple(row[:5])
            data[key] = {headers[i]: row[i] for i in range(5, len(row))}
    return data

def compare_csvs(file1, file2, output_file):
    data1 = read_csv(file1)
    data2 = read_csv(file2)
    
    changes = []
    for key in data2:
        if key not in data1 or data1[key] != data2[key]:
            changes.append(list(key) + [f"{k}:{data2[key][k]}" for k in data2[key]])
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['datum', 'wahl', 'ags', 'gebiet-nr', 'gebiet-name', 'changes'])
        writer.writerows(changes)

compare_csvs('DATEI1.csv', 'DATEI2.csv', 'DATEI3.csv')