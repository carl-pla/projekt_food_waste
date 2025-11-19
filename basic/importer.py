# importer.py
import os
import csv
from models import new_entry
from utils import parse_date_or_today, parse_int_nonnegative, detect_delimiter

class CsvImporter:
    def __init__(self, encoding="utf-8", delimiter=None):
        self.encoding = encoding
        self.delimiter = delimiter  # None => auto-detect

    def import_file(self, csv_path, store, mapping=None, dry_run=False):
        """
        Liest eine CSV ein und hängt gültige Einträge an den Store (JSONL).

        Erwartetes Format (Header in der CSV):
            DATE,ITEM,GRAMS,REASON

        - DATE   : Datum (z.B. 2025-11-19 oder 19.11.2025)
        - ITEM   : Name des Lebensmittels
        - GRAMS  : Gramm (Integer, >= 0)
        - REASON : Grund (Text)

        Eine ID-Spalte wird nicht erwartet – IDs werden intern vergeben.
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV nicht gefunden: {csv_path}")

        added = 0
        skipped = 0
        errors = []

        # CSV öffnen, ggf. Delimiter auto-detecten
        with open(csv_path, "r", encoding=self.encoding, newline="") as f:
            sample = f.read(1024)
            if not sample:
                raise ValueError("CSV-Datei ist leer.")
            delim = self.delimiter or detect_delimiter(sample)
            f.seek(0)

            reader = csv.DictReader(f, delimiter=delim)

            # Header prüfen
            expected = ["DATE", "ITEM", "GRAMS", "REASON"]
            if not reader.fieldnames:
                raise ValueError("CSV-Datei enthält keinen Header.")

            missing = [c for c in expected if c not in reader.fieldnames]
            if missing:
                raise ValueError(
                    "CSV-Header muss exakt diese Spalten enthalten "
                    f"(ohne ID): {', '.join(expected)}. "
                    f"Es fehlen: {', '.join(missing)}"
                )

            # Zeilen abarbeiten (Zeile 1 = Header => start=2)
            for i, row in enumerate(reader, start=2):
                try:
                    raw_date = row["DATE"]
                    raw_item = row["ITEM"]
                    raw_grams = row["GRAMS"]
                    raw_reason = row["REASON"]

                    if not raw_item or not str(raw_item).strip():
                        raise ValueError("ITEM ist leer.")

                    d = parse_date_or_today(raw_date)
                    grams = parse_int_nonnegative(raw_grams)
                    reason = (raw_reason or "").strip()

                    # ID wird NICHT aus der CSV gelesen, sondern neu vergeben
                    entry = new_entry(raw_item, grams, reason, d)

                    if not dry_run:
                        store.append(entry)

                    added += 1
                except Exception as ex:
                    errors.append(f"line {i}: {ex}")
                    skipped += 1

        return {
            "added": added,
            "skipped": skipped,
            "errors": errors,
            "db": store.path,
        }
