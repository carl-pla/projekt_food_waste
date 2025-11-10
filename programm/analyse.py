import csv
from datetime import datetime

# Gesamte Verschwendung der Lebensmittel 
def gesamte_verschwendung():
    summe = 0
    with open("programm/data.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                summe += float(row["waste"])
            except (KeyError, ValueError):
                continue
    return summe


# Welche 3 Lebensmittel wurden am meisten entsorgt  
def lebensmittel_meiste_verschwendung():
    max_wert = 0
    lebensmittel = None
    with open("data.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                menge = float(row["waste"])
                if menge > max_wert:
                    max_wert = menge
                    lebensmittel = row["lebensmittel"]
            except (KeyError, ValueError):
                continue
    return lebensmittel, max_wert

            
# Abfrage der Lebensmittelverschwendung in einem individuellen Zeitraum    
def zeitraum(eingabe_start, eingabe_ende): 
    start_datum = datetime.strptime(eingabe_start, "%Y-%m-%d").date()
    ende_datum = datetime.strptime(eingabe_ende, "%Y-%m-%d").date()
    daten_im_zeitraum = []
    
    # öffnen der csv-datei 
    with open("data.csv", "r", newline="") as file:
        reader = csv.DictReader(file) # implementierung des csv-moduls, um jede Zeile als Dictionary auszulesen 
        for row in reader:
            try:
                datum = datetime.strptime(row["datum"], "%Y-%m-%d").date() # implementierung des datetime-moduls: striptime heißt interpretation eines textes als datum
                if start_datum <= datum <= ende_datum:
                    daten_im_zeitraum.append(row)
            except (KeyError, ValueError): #KeyError: wenn es keine zeile gibt; Valueerror: kein gültiges datum
                continue

    return daten_im_zeitraum


     

def grund():
    gruende = {} # leeres dic angelegt, um Schlüssel (grund) und werte (anzahl) zuzuordnen 
    try:
        with open("data.csv", "r") as file:
            next(file)  # Überspringe die Kopfzeile
            for line in file:
                teile = line.strip().split(",") # strip: entfernt überflüssige Leerzeichen; split: hängt am ende des eintrags ein komma an
                grund = teile[-1].strip().lower()  # Letzte Spalte = Grund
                if grund == "": # leere Einträge werden ignoriert 
                    continue

                # Grund zählen
                if grund in gruende: # wenn der grund im dict. steht soll dieses gezählt werden
                    gruende[grund] += 1
                else:
                    gruende[grund] = 1

        # Häufigsten Grund bestimmen
        häufigster_grund = None
        max_anzahl = 0

        for g, anzahl in gruende.items():
            if anzahl > max_anzahl:
                häufigster_grund = g
                max_anzahl = anzahl

        if häufigster_grund:
            return häufigster_grund, max_anzahl
        else:
            return None

    except FileNotFoundError:
        print("Datei 'data.csv' wurde nicht gefunden.")
        return None
