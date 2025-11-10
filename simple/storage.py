
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
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")

    def read_all(self):
        res = []
        if not os.path.exists(self.path):
            return res
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                d = json.loads(s)
                res.append(Entry.from_dict(d))
        return res

    def save_all(self, entries):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e.to_dict(), ensure_ascii=False) + "\n")
        os.replace(tmp, self.path)
