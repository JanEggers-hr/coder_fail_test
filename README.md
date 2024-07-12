# Teste das Coding der KI

Ein kleines Experiment: Wie oft patzt GPT-4o (bzw.: Claude 3.5 Sonnet) beim Coden?

Verzeichnis klonen (bzw. herunterladen und entpacken), in das Verzeichnis wechseln, dann mit ```python main.py``` den Test starten. 

## Programm

Das Programm ```main.py``` ausführen - das tut dann folgendes: 

- Frage nach der Anzahl der Durchläufe. 
- Fordere bei GPT-4o ein Python-Programm an, das zwei Dateien vergleichen soll. 
- Lade den Code der KI dann herunter und schreibe ihn in eine Datei namens ```llm_code.py```.
- Führe ```llm_code.py``` aus (wenn das geht). Vermerke eventuelle Fehler. 
- Wenn das Programm durchlief: Lade die Ergebnisdatei. Schau, ob das Ergebnis identisch mit einer Muster-Vergleichsdatei ist
- Schreibe das Ergebnis in eine Liste, in der alle Code-Schnipsel und Ergebnisse vermerkt sind.
- Exportiere die Ergebnisse als Excel-Tabelle.

Außerdem gibt's noch ein Programm namens ```llm_sample_code.py```, Das muss einmal durchlaufen, damit es die beiden Demo-Dateien ```DATEI1.csv``` und ```DATEI2.csv``` vergleicht und den Vergleich in eine Datei namens ```vorlage.csv``` schreibt. Mit dieser Datei wird bei den Durchläufen von main.py das Ergebnis des KI-Codes verglichen, die eine Datei ```DATEI3.csv``` erzeugen soll. 

Ich habe noch eine Version von ```main.py``` namens ```main_claude.py``` erstellt, die statt mit GPT-4o mit dem Claude-Sonnet-3.5-Modell von Anthropic arbeitet. Die Ergebnisse werden als ```llm_code_claude.py``` und ```results_claude.xlsx``` abgelegt. 

## Die Daten

stammen aus der Bürgermeisterwahl in Darmstadt - eine Leerdatei (```DATEI1.csv```), und eine, die ich von Hand an vier Stellen verändert habe (```DATEI2.csv```). Könnte man auch mit Live-Daten vom Wahlabend machen - müsste ich raussuchen.

Diese Daten-Dateien liegen auch im Verzeichnis (aus einem Lauf mit 100 Durchläufen):
- ```DATEI1.csv``` ist die Wahl-Leerdatei
- ```DATEI2.csv``` ist die veränderte Wahl-Leerdatei zum Vergleich
- ```DATEI3.csv``` ist die Datei, die das von der KI geschriebene Programm erzeugt
- ```vorlage.csv``` ist die von meinem Programm ```llm_code_sample.py``` einmal erzeugte Vergleichsdatei. 

## Das Prompt

steht in ```main.py```:

```
'Schreibe Python-Code, der zwei CSV-Dateien 
'DATEI1.csv und DATEI2.csv vergleicht.
'Die ersten fünf Spalten enthalten die Identifikation.

'Beispiel für die erste Zeile: 
'```
datum;wahl;ags;gebiet-nr;gebiet-name;max-schnellmeldungen;anz-schnellmeldungen;A1;A2;A3;A;B;B1;C;D;D1;D2;D3;D4;D5;D6;D7;D8;D9;D10
19.03.2023;Oberbürgermeisterwahl;06411000;10;00010 - Stadtverwaltung;1;0;;;;;;;;;;;;;;;;;;
'```

'Führe den Vergleich der übrigen Spalten durch, und 
'zwar so, dass alle Daten-Zeilen aufgelistet werden, die sich in DATEI2.csv
'gegenüber DATEI1.csv verändert haben oder hinzugekommen sind.

'Das Ergebnis soll in eine Datei DATEI3.csv geschrieben werden.
```

## Das Kleingedruckte

Der Test gibt nicht zwingend wieder, wie häufig der ChatGPT-Analysemodus Fehler produziert; er ist möglicherweise nicht fair:

- Dass das Programm Ergebnis- und Vergleichs-Datei als "Nicht identisch" markiert, **kann ganz harmlose Ursachen haben** - dass Zahlen als Komma- statt als Ganzzahl-Werte gespeichert werden (tatsächlich hatte mein Vorlagen-Erzeuger-Programm genau mit diesem Problem zu kämpfen). Ich habe aber einen Fall näher angeschaut - und da waren tatsächlich Quell- und Zieldaten vertauscht. 
- Selbst ein wirklich falsches Programm führt im Analysemodus nicht wirklich zu einem falschen Ergebnis, weil das Sprachmodell die Programme dort in einer Testumgebung ausführt und dann 
- Die verwendeten Daten sind ein klein wenig unrealistisch - aber dann doch nicht so sehr: schließlich handelt es sich um reale Daten und eine reale Aufgabenstellung. 
- **Das Prompt ist nicht optimal** - man kann der KI die Aufgabe noch wesentlich detaillierter und unmissverständlicher beschreiben. 
- Auffällig: GPT-4o löst die Aufgabe meist **ohne das ```pandas```-Paket**, das für Tabellendaten eigentlich der Standard ist. Im Analysemodus - also wenn man innerhalb von ChatGPT Daten verarbeiten lässt - kommt ```pandas``` immer zum Einsatz. Die Trefferquote ist dort also vermutlich höher.

Insgesamt zeigt der Versuch aber: 
- Sich mit KI Werkzeuge bauen, ist völlig in Ordnung - wenn man sie testet. 
- Problematisch wird es, wenn die KI diese Werkzeuge erst zur Laufzeit generiert - weil man nicht garantieren kann, dass das Ergebnis stimmt. 

Mehr über die Hintergründe in meinem Blog: https://janeggers.tech
