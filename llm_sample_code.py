import pandas as pd

def compare_csv(file1, file2, output_file):
    df1 = pd.read_csv(file1,sep=";")
    df2 = pd.read_csv(file2,sep=";")
    # Die ersten fünf Spalten identifizieren die Datenreihe: 
    # datum, wahl, ags, gebiet-nr, gebiet-name
    # (Okay, Datum und Wahl sind gleich)
    #
    # Wichtig auch: Anzahl der Spalten ist immer gleich. 

    # Setze die ersten fünf Spalten als Index
    df1.set_index(['datum', 'wahl', 'ags', 'gebiet-nr', 'gebiet-name'], inplace=True)
    df2.set_index(['datum', 'wahl', 'ags', 'gebiet-nr', 'gebiet-name'], inplace=True)

    # Spalten sind identisch sortiert
    diff_df = df2.compare(df1).ne('self')
    changed=diff_df.index.unique()
    changed_df = df2.loc[changed]
    # Leider
    changed_df.to_csv (output_file,sep=";",float_format='%.0f') 
    print("Fertig!")

compare_csv('DATEI1.csv', 'DATEI2.csv', 'vorlage.csv')