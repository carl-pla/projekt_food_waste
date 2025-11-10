
from uuid import uuid4
from datetime import datetime

class Entry:
    """
    Domain-Objekt für einen Lebensmittelabfall-Eintrag.
    - date_iso: "YYYY-MM-DD" (String), damit Speicherung einfach bleibt
    """
    def __init__(self, id_, date_iso, item, grams, reason):
        self.id = str(id_)
        self.date_iso = str(date_iso)
        self.item = str(item).strip()
        self.grams = int(grams)
        self.reason = str(reason).strip()

    def to_dict(self):
        return {"ID": self.id, "DATE": self.date_iso, "ITEM": self.item, "GRAMS": self.grams, "REASON": self.reason}

    @staticmethod
    def from_dict(d: dict):
        return Entry(d["ID"], d["DATE"], d["ITEM"], int(d["GRAMS"]), d["REASON"])

    def date_obj(self):
        return datetime.strptime(self.date_iso, "%Y-%m-%d").date()

def new_entry(item, grams, reason, date_obj):
    """Convenience Factory: erzeugt Entry mit neuer UUID und Datum als ISO."""
    return Entry(str(uuid4()), date_obj.isoformat(), item, grams, reason)
