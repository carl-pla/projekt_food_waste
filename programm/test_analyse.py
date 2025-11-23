# Die Funktionen aus analyse.py, die wir testen wollen
from analyse import (
    gesamte_verschwendung,
    lebensmittel_meiste_verschwendung,
    zeitraum,
    grund,
)


# =========================================================
# Mini-Testframework (eigener kleiner Test-Runner) 
# --> führt Testfunktion aus, druckt "FEHLER" oder "OK", unterscheidet Fehler (erwartet vs. unerwartet)
# =========================================================

def test(name, func):
    try:
        func()
        print(f"[OK]     {name}")
    except AssertionError as e:
        print(f"[FEHLER] {name}: {e}")
    except Exception as e:
        print(f"[FEHLER] {name}: Unerwarteter Fehler -> {e}")


# =========================================================
# Test-Dummy-Daten (Liste von Zeilen wie aus read_data)
# =========================================================

DATA = [
    {
        "lebensmittel": "Apfel",
        "datum": "2024-01-10",
        "waste": "1000",
        "grund": "Schimmel",
    },
    {
        "lebensmittel": "Brot",
        "datum": "2024-02-10",
        "waste": "200",
        "grund": "Abgelaufen",
    },
    {
        "lebensmittel": "Milch",
        "datum": "2024-03-10",
        "waste": "300",
        "grund": "Schimmel",
    },
]


# =========================================================
# Einzeltests für jede analyse.py-Funktion
# =========================================================

def test_gesamte_verschwendung():
    resultat = gesamte_verschwendung(DATA)
    # 1000 + 200 + 300 = 1500
    assert resultat == 1500.0, f"Erwartet 1500.0, bekommen {resultat}"


def test_lebensmittel_meiste_verschwendung():
    resultat = lebensmittel_meiste_verschwendung(DATA)
    # Sortierung: Apfel (1000), Milch (300), Brot (200)
    erwartung = [("Apfel", 1000.0), ("Milch", 300.0), ("Brot", 200.0)]
    assert resultat == erwartung, f"Erwartet {erwartung}, bekommen {resultat}"


def test_zeitraum():
    resultat = zeitraum("2024-01-01", "2024-02-28", DATA)
    # Apfel (10.01.2024) und Brot (10.02.2024) liegen im Zeitraum
    lebensmittel = {row["lebensmittel"] for row in resultat}
    erwartung = {"Apfel", "Brot"}
    assert lebensmittel == erwartung, f"Erwartet {erwartung}, bekommen {lebensmittel}"


def test_grund():
    resultat = grund(DATA)
    # Schimmel kommt 2x vor, Abgelaufen einmal
    erwartung = [("Schimmel", 2), ("Abgelaufen", 1)]
    assert resultat == erwartung, f"Erwartet {erwartung}, bekommen {resultat}"


# =========================================================
# Test Runner
# =========================================================

if __name__ == "__main__":
    print("\nStarte Tests für analyse.py ...\n")

    test("gesamte_verschwendung", test_gesamte_verschwendung)
    test("lebensmittel_meiste_verschwendung", test_lebensmittel_meiste_verschwendung)
    test("zeitraum", test_zeitraum)
    test("grund", test_grund)

    print("\nTests abgeschlossen.\n")
