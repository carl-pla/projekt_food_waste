# THIS OPTIONAL SCRIPT SHOWS HOW TO INVOKE THE CLI PROGRAMMATICALLY.
# IT IS PURELY FOR DEMONSTRATION AND KEPT IN PYTHON (CODE-ONLY OUTPUT).
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

def MAIN() -> None:
    DB = str((Path.home() / ".food_waste" / "data.jsonl").expanduser())
    # ADD A SAMPLE ENTRY
    subprocess.run([sys.executable, "-m", "food_waste_tracker", "--db", DB, "add", "--item", "APFEL", "--grams", "90", "--reason", "RESTE"], check=False)
    # SHOW TOTAL
    subprocess.run([sys.executable, "-m", "food_waste_tracker", "--db", DB, "total"], check=False)

if __name__ == "__main__":
    MAIN()
