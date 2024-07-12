# Variante mit Claude 3.5 Sonnet statt GPT-4o

D1 = "./DATEI1.csv"
D2 = "./DATEI2.csv"
D_TEST = "./DATEI3.csv"
D_SAMPLE = "./vorlage.csv"

import re
import os
import pandas as pd
import subprocess
import anthropic


def execute(code):
    # Save the code to a temporary file
    with open("llm_code_claude.py", "w") as f:
        f.write(code)
    try:
    # Run the file as a separate process
        result = subprocess.run(["python", "llm_code_claude.py"], capture_output=True, text=True, timeout=5)
        # Check if there were any errors
        if "Error" in str(result.stderr):
            print("Errors:", result.stderr)
            return False
        else:
            return True
    except subprocess.TimeoutExpired:
        print("Error: Code execution timed out")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    
   
# Compares the two 
import filecmp

def compare(file1, file2):
    # Check if the files exist
    if not os.path.exists(D_TEST) or not os.path.exists(D_SAMPLE):
        return "Datei fehlt"
    try:
        df1 = pd.read_csv(D_SAMPLE,sep=";")
        df2 = pd.read_csv(D_TEST,sep=";")
    except:
        # Formatfehler; nicht lesbar
        return "Falsches CSV"
    
    if not df1.columns.equals(df2.columns):
        return "Versch. Spalten"
    
    # Spalten sind identisch sortiert - hopefully. Manchmal knallt's trotzdem.
    try:
        diff_df = df2.compare(df1).ne('self')
        changed=diff_df.index.unique()
    except:
        return "Versch. Daten"
    if len(changed)== 0:
        # Fein, sind identisch
        return "OK"
    else:
        return "Nicht identisch"
    
    # Compare files using filecmp
    is_same = filecmp.cmp(D_TEST, D_SAMPLE, shallow=False)

    return is_same

def code_extract(llm_output: str) -> str:
    # Pattern to match Python code blocks
    pattern = r"```python\s*(.*?)```"
    # Find all matches, ignoring case and allowing for multiline
    matches = re.findall(pattern, llm_output, re.IGNORECASE | re.DOTALL)
    # Concatenate all found code blocks
    extracted_code = "\n\n".join(match.strip() for match in matches)
    return extracted_code
  
sys_prompt = "Du bist ein wortkarger Python-Programmierer. Du antwortest nur mit lauffähigem Code."
prompt ="""
Schreibe Python-Code, der zwei CSV-Dateien 
DATEI1.csv und DATEI2.csv vergleicht.
Die ersten fünf Spalten enthalten die Identifikation.

Beispiel für die erste Zeile: 
```
datum;wahl;ags;gebiet-nr;gebiet-name;max-schnellmeldungen;anz-schnellmeldungen;A1;A2;A3;A;B;B1;C;D;D1;D2;D3;D4;D5;D6;D7;D8;D9;D10
19.03.2023;Oberbürgermeisterwahl;06411000;10;00010 - Stadtverwaltung;1;0;;;;;;;;;;;;;;;;;;
```

Führe den Vergleich der übrigen Spalten durch, und 
zwar so, dass alle Daten-Zeilen aufgelistet werden, die sich in DATEI2.csv
gegenüber DATEI1.csv verändert haben oder hinzugekommen sind.

Das Ergebnis soll in eine Datei DATEI3.csv geschrieben werden.
"""


if __name__=="__main__":
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    results=[]
    code_samples=[]
    print("V1.0 - Claude3.5")
    n=int(input("Wie viele Durchläufe soll ich machen? "))
    for i in range(n):
        # Delete D_TEST if exists
        if os.path.exists(D_TEST):
           os.remove(D_TEST)
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            temperature=0.7,
            max_tokens=1000,
            system = sys_prompt,
            messages=[
                {
                   'role': 'user',
                   'content': [
                       {
                           'type': 'text',
                           'text': prompt,
                       }
                   ]
                }
            ],
            stream=False,
        )
        # Extract code
        code = code_extract(message.content[0].text)
        code_samples.append(code)
        if not execute(code):
           print("Code failed")
           results.append("Codefehler")
        else:
           c = compare(D_TEST,D_SAMPLE)
           print(f"Ergebnis Durchlauf {i+1}: {c}")
           results.append(c)
    print(f"{n} Durchläufe abgeschlossen.")
    df = pd.DataFrame({'Ergebnis': results,'Code':code_samples})
    df.to_excel("results_claude.xlsx",index=True)
