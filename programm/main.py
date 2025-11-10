from datetime import datetime
from Projekt_FoodWaste.programm.create import daten_hinzufuegen
from Projekt_FoodWaste.programm.analyse import gesamte_verschwendung, lebensmittel_meiste_verschwendung, zeitraum, grund

"""
csv.datei wird nicht in spezieller Methode aufgerufen, da sonst zwei Methoden kollidieren, was es schlecht zum testen  

Programm kann in verschiedene Dateien sortiert werden, dass es übersichtlicher bleibt

"""
                
                       
"""
-CLI-Handling (Inputs,prints)
-nicht objektorientiert

"""

def main():
    while True:
        welche_aufgabe = input(
            "Willkommen beim Food Waste Tracker\n"
            "Möchten Sie Daten auslesen oder hinzufügen? (1/2): "
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
                print(f"Deine Auswahl: {auswahl}\n{gesamte_verschwendung()}")
            elif auswahl == "b":
                print(f"Deine Auswahl: {auswahl}\n{lebensmittel_meiste_verschwendung()}")
            elif auswahl == "c":
                print(f"Deine Auswahl: {auswahl}\n{zeitraum()}")
            elif auswahl == "d":
                print(f"Deine Auswahl: {auswahl}\n{grund()}")
            
            
            

        elif welche_aufgabe == "2":
            print("\nWillkommen, welche Daten möchten Sie hinzufügen?\n")

            # Datum prüfen
            while True:
                datum_abfrage = input("Datum (yyyy-mm-dd): ")
                try:
                    datum_abfrage = datetime.strptime(datum_abfrage, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print("Ungültiges Datum! Bitte im Format yyyy-mm-dd eingeben.\n")

            # Lebensmittel prüfen
            while True:
                try:
                    lebensmittel_abfrage = input("Lebensmittel: ").strip() #Unnötige Leerzeichen werden zusätzlich entfernt
                    if not lebensmittel_abfrage:
                        raise ValueError("Bitte ein Lebensmittel angeben.")
                    break
                except ValueError:
                    raise(ValueError)

            # Menge prüfen
            while True:
                try:
                    menge_abfrage = input("Menge (in Gramm): ").strip()
                    if menge_abfrage == float():
                        raise ValueError("Die Menge muss eine gerade Zahl sein")
                    if menge_abfrage <= 0:
                        raise ValueError("Die Menge muss größer als 0 sein.")
                    break
                except ValueError:
                    print("Bitte eine gültige, gerade Zahl größer als 0 eingeben.\n")

            # Grund prüfen
            while True:
                try:
                    grund_abfrage = input("Grund (Stichwort): ").strip()
                    if not grund_abfrage:
                        raise ValueError("Bitte einen Grund angeben.")
                    break
                except ValueError:
                    raise ValueError

            
            # Zu data.csv hinzufügen 
            daten_hinzufuegen()
            
            # Ausgabe
            print("\nDaten erfolgreich aufgenommen!")
            print(f"- Datum: {datum_abfrage}")
            print(f"- Lebensmittel: {lebensmittel_abfrage}")
            print(f"- Menge: {menge_abfrage} g")
            print(f"- Grund: {grund_abfrage}\n")

        else:
            print("Ungültige Eingabe! Bitte geben Sie '1' oder '2' ein.\n")


if __name__ == "__main__":
    main()
