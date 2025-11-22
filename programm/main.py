from datetime import datetime
import os
import csv
from analyse import gesamte_verschwendung, lebensmittel_meiste_verschwendung, zeitraum, grund

""" 
Programm kann in verschiedene Dateien sortiert werden, sodass es übersichtlicher bleibt

"""          
                       
"""
-CLI-Handling (Inputs,prints)
-nicht objektorientiert

"""
def read_data():
    data = {}
    path = os.path.join(os.path.dirname(__file__), "data.csv")
    with open(path, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row["lebensmittel"]
            data[key] = row
    return data

def write_data(appended_data):
    path = os.path.join(os.path.dirname(__file__), "data.csv")
    with open (path, "a", newline="") as file:
        fieldnames = ["lebensmittel","datum","waste","grund"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for row in appended_data.values():
            writer.writerow(row)

def write_dict(lebensmittel, datum, waste, grund, data):
    appended_data = {}
    appended_data[lebensmittel] = {
        "lebensmittel": lebensmittel,
        "datum": datum,
        "waste": waste,
        "grund": grund
    }
    data[lebensmittel] = appended_data[lebensmittel]  # füge es ins existierende data ein
    return appended_data


def check_date_format(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def main():
    while True:
        
        welche_aufgabe = input(
            "\nWillkommen beim Food Waste Tracker\n"
            "Möchten Sie Daten auslesen (1) oder hinzufügen (2) oder das Programm beenden(3)?: "
        )

        if welche_aufgabe == "1":
            print(
                "\nWillkommen beim Daten auslesen\n"
                "Was möchten Sie wissen?\n"
                "a) Gesamte Menge an weggeworfenen Lebensmitteln anzeigen\n"
                "b) Die drei Lebensmittel mit der größten weggeworfenen Menge\n"
                "c) Menge an weggeworfenen Lebensmitteln in einem bestimmten Zeitraum\n"
                "d) Häufigster Grund für das Wegwerfen\n"
            )

            auswahl = input("\nIhre Auswahl (a | b | c | d): ").lower()

            if auswahl not in ["a", "b", "c", "d"]:
                print("Ungültige Auswahl. Bitte a, b, c oder d eingeben.\n")
            
            elif auswahl == "a":
                print(f"Deine Auswahl: {auswahl}\n{gesamte_verschwendung(data)} gramm")
            
            elif auswahl == "b":
                print(f"Deine Auswahl: {auswahl}\n{lebensmittel_meiste_verschwendung(data)}")
            
            elif auswahl == "c":
                while True:
                    start_datum = input("Geben Sie das Startdatum ein (yyyy-mm-dd): ")
                    if check_date_format(start_datum):
                        break
                    else:
                        print("Ungültiges Datum! Bitte im Format yyyy-mm-dd eingeben.\n")
                while True:
                    end_datum = input("Geben Sie das Enddatum ein (yyyy-mm-dd): ")
                    if check_date_format(end_datum):
                        break
                    else:
                        print("Ungültiges Datum! Bitte im Format yyyy-mm-dd eingeben.\n")
                print(f"Deine Auswahl: {auswahl}\n{zeitraum(start_datum, end_datum,data)} gramm")
            
            elif auswahl == "d":
                print(f"Deine Auswahl: {auswahl}\n{grund(data)}")

        elif welche_aufgabe == "2":
            print("\nWillkommen, welche Daten möchten Sie hinzufügen?\n")

            while True:
                datum_abfrage = input("Datum (yyyy-mm-dd): ")
                try:
                    datum_abfrage = datetime.strptime(datum_abfrage, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print("Ungültiges Datum! Bitte im Format yyyy-mm-dd eingeben.\n")

            while True:
                try:
                    lebensmittel_abfrage = input("Lebensmittel: ").strip()
                    if not lebensmittel_abfrage:
                        raise ValueError("Bitte ein Lebensmittel angeben.")
                    break
                except ValueError:
                    raise(ValueError)

            while True:
                try:
                    menge_abfrage = float(input("Menge (in Gramm): "))
                    if menge_abfrage <= 0:
                        raise ValueError("Die Menge muss größer als 0 sein.")
                    break
                except ValueError:
                    print("Bitte eine gültige Zahl größer als 0 eingeben.\n")

            while True:
                try:
                    grund_abfrage = input("Grund (Stichwort): ").strip()
                    if not grund_abfrage:
                        raise ValueError("Bitte einen Grund angeben.")
                    break
                except ValueError:
                    raise ValueError

            write_data(write_dict(lebensmittel_abfrage,datum_abfrage,menge_abfrage,grund_abfrage))
            print("Eintrag erfolgreich hinzugefügt!")

            print("\nDaten erfolgreich aufgenommen!")
            print(f"- Datum: {datum_abfrage}")
            print(f"- Lebensmittel: {lebensmittel_abfrage}")
            print(f"- Menge: {menge_abfrage} g")
            print(f"- Grund: {grund_abfrage}\n")

        elif welche_aufgabe == "3":
            print("Programm wird beendet. Auf Wiedersehen!")
            break

        else:
            print("Ungültige Eingabe! Bitte geben Sie '1', '2' oder '3' ein.\n")

if __name__ == "__main__":
    data = read_data()
    main()