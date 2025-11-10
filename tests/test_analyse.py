# Wir importieren hier die Funktionen aus deinem Hauptprogramm


# Da wir alles in einem File simulieren, definieren wir Dummy-Funktionen:
def gesamte_verschwendung():
    # ineffektiv jeden eintrag zusammenzuzuählen 
    pass

def lebensmittel_meiste_verschwendung():
    return "Paprika"

def zeitraum(start, ende):
    # simuliert Daten im Zeitraum
    return [100, 200]

def grund():
    return "Schimmel"

# --- Testprogramm ---
def run_tests():
    print("Starte Tests...")

    # Test 1: gesamte Verschwendung
    ergebnis = gesamte_verschwendung()
    if ergebnis == 500:
        print("Test gesamte_verschwendung: OK")
    else:
        print(f"Test gesamte_verschwendung: FEHLER, Ergebnis = {ergebnis}")

    # Test 2: Lebensmittel mit meiste Verschwendung
    ergebnis = lebensmittel_meiste_verschwendung()
    if ergebnis == "Paprika":
        print("Test lebensmittel_meiste_verschwendung: OK")
    else:
        print(f"Test lebensmittel_meiste_verschwendung: FEHLER, Ergebnis = {ergebnis}")

    # Test 3: Zeitraum
    ergebnis = zeitraum("2025-11-01", "2025-11-03")
    if ergebnis == [100, 200]:
        print("Test zeitraum: OK")
    else:
        print(f"Test zeitraum: FEHLER, Ergebnis = {ergebnis}")

    # Test 4: Häufigster Grund
    ergebnis = grund()
    if ergebnis == "Schimmel":
        print("Test grund: OK")
    else:
        print(f"Test grund: FEHLER, Ergebnis = {ergebnis}")

    print("Tests abgeschlossen.")

# Nur ausführen, wenn das Script direkt gestartet wird
if __name__ == "__main__":
    run_tests()