import csv
from datetime import datetime

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

            
            
def zeitraum(eingabe_start, eingabe_ende): #nochmal vertiefen, besonders das Modul
    start_datum = datetime.strptime(eingabe_start, "%Y-%m-%d").date()
    ende_datum = datetime.strptime(eingabe_ende, "%Y-%m-%d").date()
    daten_im_zeitraum = []

    with open("data.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                datum = datetime.strptime(row["datum"], "%Y-%m-%d").date()
                if start_datum <= datum <= ende_datum:
                    daten_im_zeitraum.append(row)
            except (KeyError, ValueError):
                continue

    return daten_im_zeitraum


     

def grund():
    gruende = {}
    try:
        with open("data.csv", "r") as file:
            next(file)  # Überspringe die Kopfzeile
            for line in file:
                teile = line.strip().split(",") #?
                grund = teile[-1].strip().lower()  # Letzte Spalte = Grund
                if grund == "":
                    continue

                # Grund zählen
                if grund in gruende:
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
