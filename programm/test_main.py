# =========================================================
# Grundidee des Testprogramms: 
# --> Code baut eine Testumgebung auf 
# --> führt Testfunktionen basierend auf dessen Inhalten aus (sonst müssen Daten aus einer unberrechenbaren Umgebung genommen werden)
# --> prüft Ergebnisse 
# --> stellt echte Umgebung wieder her

# Gliederung: 
# 1.Benötigte Module importieren
# 2.Test-Datei erstellen 
# 3.Test-Runner erstellen

# 4.Test nr.1: Funktioniert das korrekte auslesen aus der CSV-datei?
# 5.Test nr.2: Wird ein korrektes Dictionary zurückgegeben? 
# 6.Test nr.3: Wird ein neuer Eintrag korrekt an die CSV gehängt?
# 7.Test nr.4: Stimmt die Validierung mit der Logik des datetime-modules überein? 
# =========================================================

#importieren der benötigten Module
import os
import csv
from datetime import datetime

# Die Funktionen aus main.py, die wir testen wollen
from main import read_data, write_dict, write_data, check_date_format


# =========================================================
# Test-Datei für CSV-Operationen (orignale CSV-Datei wird nicht benutzt)
# =========================================================

# Name der Test-CSV-Datei
TEST_CSV = "test_data.csv"


# =========================================================
# Mini-Testframework (eigener kleiner Test-Runner) 
# --> führt Testfunktion aus, druckt "FEHLER" oder "OK", unterscheidet Fehler (erwartet vs. unerwartet)
# =========================================================

def test(name, func):
    """
    Führt einen Test aus.
    Zeigt übersichtlich an, ob er OK war oder Fehler hatte.
    """
    try:
        func()
        print(f"[OK]     {name}")
    except AssertionError as e:
        # AssertionError = Test schlägt sauber fehl
        print(f"[FEHLER] {name}: {e}")
    except Exception as e:
        # Alle anderen Fehler = Unerwartet → Hinweis
        print(f"[FEHLER] {name}: Unerwarteter Fehler -> {e}")



# =========================================================
# Test-Dummy-CSV
# =========================================================

def erstelle_test_csv():
    """
    Erstellt eine komplette Beispiel-CSV,
    damit die Tests auf einer kontrollierten Datei laufen.
    """
    inhalt = """lebensmittel,datum,waste,grund
Apfel,2024-01-01,1000,Schimmel
Brot,2024-02-01,200,Abgelaufen
Milch,2024-03-01,300,Schimmel
"""
    # Datei überschreiben → Testdaten 100% reproduzierbar
    with open(TEST_CSV, "w", encoding="utf-8") as f:
        f.write(inhalt)


# =========================================================
# Einzeltests für jede main.py-Funktion

# --> test_read_data und test_write_data arbeiten mit einer künstlichen-CSV-Datei, das schützt die echten Daten, Testumgebung und Reproduziertbarkeit des Tests!
# --> Folgen, wenn nicht: Wiederholbarkeit des Tests nicht gegeben, durch Veränderungen an der Original Datei
# =========================================================

def test_read_data():
    """
    Testet, ob read_data() korrekt aus der CSV liest
    und das richtige Dictionary zurückgibt.
    """
    erstelle_test_csv()

    # Pfade der realen Datei und der Testdatei bestimmen
    original_path = os.path.join(os.path.dirname(__file__), "data.csv")
    test_path = os.path.join(os.path.dirname(__file__), TEST_CSV)

    # Falls echte data.csv existiert → sichern
    if os.path.exists(original_path):
        os.rename(original_path, original_path + ".backup")

    # test_data.csv → data.csv umbenennen
    os.rename(test_path, original_path)

    # Test durchführen
    data = read_data()

    # Prüfen, ob die Lebensmittel korrekt eingelesen wurden
    assert "Apfel" in data
    assert "Brot" in data
    assert "Milch" in data

    # Prüfen, ob ein Feld korrekt übernommen wurde
    assert data["Apfel"]["waste"] == "1000"

    # Dateien zurücksetzen
    os.rename(original_path, test_path)
    if os.path.exists(original_path + ".backup"):
        os.rename(original_path + ".backup", original_path)


def test_write_dict():
    """
    Testet, ob write_dict() ein korrekt formatiertes Dictionary erzeugt
    """
    data = {}
    appended_data = write_dict("TestLM", "2024-10-10", "999", "TestGrund", data)

    # Prüfen, ob der Eintrag im zurückgegebenen Dictionary vorhanden ist
    assert "TestLM" in appended_data
    assert appended_data["TestLM"]["waste"] == "999"
    assert appended_data["TestLM"]["grund"] == "TestGrund"

    # Prüfen, ob der Eintrag auch ins data-Dictionary übernommen wurde
    assert "TestLM" in data
    assert data["TestLM"]["waste"] == "999"
    assert data["TestLM"]["grund"] == "TestGrund"


def test_write_data():
    """
    Testet, ob write_data() eine neue Zeile KORREKT an die CSV anhängt.
    """
    erstelle_test_csv()

    # Dummy-Datensatz, der angehängt werden soll
    data = {
        "TestLM": { 
            "lebensmittel": "TestLM",
            "datum": "2024-10-10",
            "waste": "999",
            "grund": "TestGrund"
        }
    }
    

    # Pfade ermitteln
    path = os.path.join(os.path.dirname(__file__), TEST_CSV)
    original_path = os.path.join(os.path.dirname(__file__), "data.csv")

    # Originaldatei sichern als "backup"
    if os.path.exists(original_path):
        os.rename(original_path, original_path + ".backup")

    # test_data.csv → data.csv, damit write_data korrekt arbeitet
    os.rename(path, original_path)

    # Test: neue Zeile anhängen
    write_data(data)
    

    # Datei einlesen
    with open(original_path, "r") as f:
        lines = f.read().splitlines()

    # Letzte Zeile überprüfen
    assert "TestLM,2024-10-10,999,TestGrund" in lines[-1]

    # Dateien wiederherstellen
    os.rename(original_path, path)
    if os.path.exists(original_path + ".backup"):
        os.rename(original_path + ".backup", original_path)


def test_check_date_format():
    """
    Testet die Datumsformat-Prüfung (YYYY-MM-DD).
    """
    assert check_date_format("2024-01-01") is True
    assert check_date_format("2024-13-40") is False
    assert check_date_format("01-01-2024") is False
    assert check_date_format("abc") is False


# =========================================================
# Test Runner
# =========================================================

if __name__ == "__main__":
    print("Starte Tests für main.py ...\n")

    test("read_data", test_read_data)
    test("write_dict", test_write_dict)
    test("write_data", test_write_data)
    test("check_date_format", test_check_date_format)

    print("\nTests abgeschlossen.")
