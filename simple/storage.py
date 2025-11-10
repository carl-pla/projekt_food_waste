
import os
import json
from models import Entry
from utils import ensure_parent

class Store:
    """
    JSONL-only Store. Always persists to JSON Lines (one JSON object per line).
    CSV is supported only for IMPORT, never for persistence.
    """
    def __init__(self, path):
        self.path = os.path.expanduser(path)
        ensure_parent(self.path)
        if not os.path.exists(self.path):
            # create empty JSONL file
            open(self.path, "a", encoding="utf-8").close()

    def append(self, entry: Entry):
        with open(self.path, "a", encoding="utf-8") as f:   # Schreibt appended, also am Ende der Datei
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")     # dumps wandelt dict in json-String um
            # Schreibt in die Datei ein dump für den übergebenen Entry-Eintrag mit utf-8 und fügt einen Zeilenumbruch ein

    def read_all(self):
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

    def save_all(self, entries):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e.to_dict(), ensure_ascii=False) + "\n")
        os.replace(tmp, self.path)      # (src, dst)
