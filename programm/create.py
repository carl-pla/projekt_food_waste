from datetime import datetime

    
"""
User willl Einträge in die csv-Datei hinzufügen
""" 

def daten_hinzufuegen():
    try:
        datum = input("Datum (yyyy-mm-dd): ").strip()
        lebensmittel = input("Lebensmittel: ").strip()
        menge = input("Menge (in Gramm): ").strip()
        grund = input("Grund: ").strip()

        # Eingaben prüfen
        if not datum or not lebensmittel or not menge or not grund:
            print("Bitte alle Felder ausfüllen.")
            return

        try:
            menge = int(menge)  # prüfen, ob Zahl
        except ValueError:
            print("Ungültige und ungerade Zahl bei der Menge!")
            return

        # In Datei schreiben
        with open("data.csv", "a") as file:
            file.write(f"{datum},{lebensmittel},{menge},{grund}\n")

        print("Eintrag erfolgreich hinzugefügt!")

    except FileNotFoundError:
        print("Datei wurde nicht gefunden.")
    except Exception:
        raise Exception

