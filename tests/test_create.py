# test_create.py

# Importiere die Funktion aus create.py

def daten_hinzufuegen():
    try:
        datum = input("Datum (yyyy-mm-dd): ").strip()
        lebensmittel = input("Lebensmittel: ").strip()
        menge = int(input("Menge (in Gramm): ")).strip()
        grund = input("Grund: ").strip()

        if not datum or not lebensmittel or not menge or not grund:
            print("Bitte alle Felder ausfüllen.")
            return

        try:
            menge = int(menge)
        except ValueError:
            print("Ungültige und ungerade Zahl bei der Menge!")
            return

        with open("data.csv", "a") as file:
            file.write(f"{datum},{lebensmittel},{menge},{grund}\n")

        print("Eintrag erfolgreich hinzugefügt!")

    except FileNotFoundError:
        print("Datei wurde nicht gefunden.")
    except Exception:
        raise Exception

# --- Testprogramm ---
def run_tests():
    print("Starte Tests für daten_hinzufuegen...")

    # Test 1: Gültige Eingaben simulieren
    inputs = iter(["2025-11-07", "Paprika", 100, "Schimmel"])
    original_input = __builtins__.input
    __builtins__.input = lambda _: next(inputs)

    try:
        daten_hinzufuegen()
        print("Test 1: Gültige Eingaben erfolgreich")
    except Exception as e:
        print(f"Test 1: FEHLER: {e}")

    # Test 2: Ungültige Menge
    inputs = iter(["2025-11-07", "Joghurt", "abc", "Ablaufdatum"])
    __builtins__.input = lambda _: next(inputs)

    try:
        daten_hinzufuegen()
        print("Test 2: Ungültige Menge korrekt behandelt")
    except Exception as e:
        print(f"Test 2: FEHLER: {e}")

    # Test 3: Leere Eingabe
    inputs = iter(["", "Milch", 50, "Schimmel"])
    __builtins__.input = lambda _: next(inputs)

    try:
        daten_hinzufuegen()
        print("Test 3: Leere Eingabe korrekt behandelt")
    except Exception as e:
        print(f"Test 3: FEHLER: {e}")

    # Restore original input
    __builtins__.input = original_input

    print("Tests abgeschlossen.")

# Nur ausführen, wenn das Script direkt gestartet wird
if __name__ == "__main__":
    run_tests()
