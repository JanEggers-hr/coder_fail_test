import csv

def lese_csv_datei(datei):
    with open(datei, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        return list(reader)

def schreibe_csv_datei(datei, daten):
    with open(datei, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerows(daten)

def vergleiche_csv(datei1, datei2, ergebnis_datei):
    daten1 = lese_csv_datei(datei1)
    daten2 = lese_csv_datei(datei2)
    
    header = daten1[0]
    daten1_dict = {tuple(row[:5]): row for row in daten1[1:]}
    daten2_dict = {tuple(row[:5]): row for row in daten2[1:]}
    
    unterschiede = [header]
    
    for key, row in daten2_dict.items():
        if key not in daten1_dict or daten1_dict[key] != daten2_dict[key]:
            unterschiede.append(row)
    
    schreibe_csv_datei(ergebnis_datei, unterschiede)

vergleiche_csv('DATEI1.csv', 'DATEI2.csv', 'DATEI3.csv')