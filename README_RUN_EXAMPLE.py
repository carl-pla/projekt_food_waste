# Hier ist ein einfaches Beispiel, um das Projekt zu verwenden
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

def MAIN() -> None:
    # Datenbank unter C:\Users\<DeinName>\.food_waste\data.jsonl
    DB = str((Path.home() / ".food_waste" / "data.jsonl").expanduser())
    # Standard Eintrag zum hinzufügen
    subprocess.run([sys.executable, "-m", "food_waste_tracker", "--db", DB, "add", "--item", "APFEL", "--grams", "90", "--reason", "RESTE"], check=False)
    # Anzeigen von Auswertungen
    subprocess.run([sys.executable, "-m", "food_waste_tracker", "--db", DB, "total"], check=False)

if __name__ == "__main__":
    MAIN()
