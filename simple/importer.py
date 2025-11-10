# importer.py
import os
import csv
from models import new_entry
from utils import parse_date_or_today, parse_int_nonnegative, detect_delimiter

class CsvImporter:      # Erstellt ein Objekt
    def __init__(self, encoding="utf-8", delimiter=None):   # Initiiert mit Verschlüsselung und Delimiter, wenn Übergeben, ansonsten Standardwerte
        self.encoding = encoding
        self.delimiter = delimiter  # None => auto-detect

    def import_file(self, csv_path, store, mapping=None, dry_run=False):
        """
        Liest eine CSV ein und hängt gültige Einträge an den Store (JSONL).
        mapping: z.B. {"DATE":"Datum","ITEM":"Artikel","GRAMS":"Menge","REASON":"Grund","ID":"ID"}
        """

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV not found: {csv_path}")

        added = 0
        skipped = 0
        errors = []

        with open(csv_path, "r", encoding=self.encoding, newline="") as f:
            if self.delimiter is None:  # Wenn kein Delimiter angegeben wird
                sample = f.read(4096); f.seek(0)    # Liest einen Teil ein, um daran festzumachen, welche Trennzeichen benutzt werden
                # f.seek(0) springt wieder an den Anfang
                delim = detect_delimiter(sample)
            else:
                delim = self.delimiter  # Setzt das Trennzeichen/Delimiter

            reader = csv.DictReader(f, delimiter=delim)     # Erstellt ein CSV-Reader Objekt, das dicts einliest
            # Dabei wird die erste Zeile als Header interpretiert und in reader.fieldnames gespeichert
            headers = reader.fieldnames or []   # liest die Header ein oder setzt sie leer, wenn nicht vorhanden
            upper = {h.strip().upper(): h for h in headers}     # Mappt die vorgesehenen Namen mit den Spaltennamen der Datei

            if mapping:
                col = {k.upper(): v for k, v in mapping.items()}    # Benutzerdefinierte Zuordnung
            else:
                required = ["DATE","ITEM","GRAMS","REASON"]     # Notwendige Spalten
                missing = [r for r in required if r not in upper]   # Speichert fehlende Spalten
                if missing:     # Wenn Spalten fehlen
                    raise ValueError(f"Missing required columns: {missing}. Found: {headers}")    # Gibt einen Fehler
                col = {k: upper[k] for k in required}   # Um eventuelle Extraspalten auszuschließen, wird col nur mit den geforderten Spalten erstellt
                if "ID" in upper:   # Setzt die ID, wenn sie vorhanden ist, ansonsten wird sie später erstellt
                    col["ID"] = upper["ID"]

            for i, row in enumerate(reader, start=2):   # Startet bei der 2ten Zeile, um die Header nicht als Werte einzulesen
            # i als index und row als dict
                try:
                    d = parse_date_or_today(row[col["DATE"]])   # Mit row[col["DATE"]] wird aus der row die Spalte geholt, die für "DATE" gemappt ist
                    item = str(row[col["ITEM"]]).strip()    # Strip entfernt Leerzeichen am Anfang oder Ende
                    grams = parse_int_nonnegative(row[col["GRAMS"]])
                    reason = str(row[col["REASON"]]).strip()

                    entry = new_entry(item, grams, reason, d)

                    # Falls CSV eine ID-Spalte hat, übernehme sie
                    if "ID" in col and row.get(col["ID"]):
                        entry.id = str(row[col["ID"]]).strip() or entry.id

                    if not dry_run:     # Wenn kein Test, also dry im Sinne von, keine Endgültige Veränderung
                        store.append(entry)     # Fügt den Datensatz als neue Zeile hinzu
                    added += 1      # Setzt den count für hinzugefügte Datensätze hoch
                except Exception as ex:
                    errors.append(f"line {i}: {ex}")      # Fügt den Error der Liste an, damit der run nicht unterbrochen wird
                    skipped += 1    # Erhöht den übersprungen/fehler count

        return {"added": added, "skipped": skipped, "errors": errors, "db": store.path}
