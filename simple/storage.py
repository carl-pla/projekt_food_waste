# storage.py
import os
import json
from models import Entry, entry_from_dict

# Ordner, in dem storage.py liegt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# data.jsonl im selben Ordner
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "data.jsonl")


class Store:
    """
    JSONL-Store.
    Speichert alle Einträge in data.jsonl im selben Verzeichnis wie der Code.
    """
    def __init__(self, path: str = DEFAULT_DB_PATH):
        self.path = path

        # Datei anlegen, falls sie noch nicht existiert
        if not os.path.exists(self.path):
            # Leere Datei anlegen
            with open(self.path, "w", encoding="utf-8"):
                pass  # leere Datei reicht für JSONL

    def append(self, entry: Entry):
        """Einen Eintrag ans Ende der JSONL-Datei anhängen."""
        with open(self.path, "a", encoding="utf-8") as f:   # Schreibt appended, also am Ende der Datei
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")     # dumps wandelt dict in json-String um
            # Schreibt in die Datei ein dump für den übergebenen Entry-Eintrag mit utf-8 und fügt einen Zeilenumbruch ein

    def read_all(self):
        """Alle Einträge aus der JSONL-Datei als Entry-Objekte laden."""
        res = []
        if not os.path.exists(self.path):
            return res

        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                d = json.loads(s)   # Lädt die Zeile als json aus einem string (loads = load string)
                res.append(Entry.from_dict(d))
        return res

    def save_all(self, entries) -> None:
        """Komplettliste speichern (überschreibt Datei)."""
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e.to_dict(), ensure_ascii=False) + "\n")
        os.replace(tmp, self.path)      # (src, dst)
