
import os
import csv
from models import Entry
from utils import parse_date_or_today, parse_int_nonnegative, detect_delimiter

class CsvImporter:
    def __init__(self, encoding="utf-8", delimiter=None):
        self.encoding = encoding
        self.delimiter = delimiter  # None => auto-detect

    def import_file(self, csv_path, store, mapping=None, dry_run=False):
        """
        Importiert CSV-Einträge in den JSONL-Store.
        mapping: dict wie {"DATE":"Datum","ITEM":"Artikel","GRAMS":"Menge","REASON":"Grund","ID":"ID"}
        """
        csv_path = os.path.expanduser(csv_path)
        if not os.path.exists(csv_path):
            raise FileNotFoundError("CSV not found: %s" % csv_path)

        added = 0
        skipped = 0
        errors = []

        with open(csv_path, "r", encoding=self.encoding, newline="") as f:
            if self.delimiter is None:
                sample = f.read(4096); f.seek(0)
                delim = detect_delimiter(sample)
            else:
                delim = self.delimiter

            reader = csv.DictReader(f, delimiter=delim)
            headers = reader.fieldnames or []
            upper = {h.strip().upper(): h for h in headers}

            if mapping:
                col = {k.upper(): v for k, v in mapping.items()}
            else:
                required = ["DATE","ITEM","GRAMS","REASON"]
                missing = [r for r in required if r not in upper]
                if missing:
                    raise ValueError("Missing required columns: %s. Found: %s" % (missing, headers))
                col = {k: upper[k] for k in required}
                if "ID" in upper:
                    col["ID"] = upper["ID"]

            for i, row in enumerate(reader, start=2):
                try:
                    d = parse_date_or_today(row[col["DATE"]])
                    item = str(row[col["ITEM"]]).strip()
                    grams = parse_int_nonnegative(row[col["GRAMS"]])
                    reason = str(row[col["REASON"]]).strip()

                    entry = Entry("TEMP_ID", d.isoformat(), item, grams, reason)
                    entry.id = __import__("uuid").uuid4().hex
                    if "ID" in col and row.get(col["ID"]):
                        entry.id = str(row[col["ID"]]).strip() or entry.id

                    if not dry_run:
                        store.append(entry)
                    added += 1
                except Exception as ex:
                    errors.append("line %d: %s" % (i, ex))
                    skipped += 1

        return {"added": added, "skipped": skipped, "errors": errors, "db": store.path}
