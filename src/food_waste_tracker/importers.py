from __future__ import annotations
from typing import Dict, Any, Optional
from pathlib import Path
import csv

from .models import ENTRY
from .storage import STORAGE
from .utils import PARSE_INT_NONNEGATIVE

def IMPORT_CSV_TO_STORAGE(
    CSV_PATH: str,
    STORE: STORAGE,
    MAPPING: Optional[Dict[str, str]] = None,
    ENCODING: str = "utf-8",
    DELIMITER: Optional[str] = None,
    DRY_RUN: bool = False,
) -> Dict[str, Any]:
    """
    Lies Einträge aus einer CSV-Datei ein und füge sie der aktuellen STORAGE hinzu.

    Erwartete Standard-Header (case-insensitive): DATE, ITEM, GRAMS, REASON, optional ID.
    Alternativ MAPPING übergeben, z.B. {"DATE": "Datum", "ITEM": "Artikel", "GRAMS": "Menge", "REASON": "Grund", "ID": "ID"}.

    Rückgabe: {"added": int, "skipped": int, "errors": [str], "db": str}
    """
    path = Path(CSV_PATH)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    added = 0
    skipped = 0
    errors: list[str] = []

    with path.open("r", encoding=ENCODING, newline="") as f:
        sample = f.read(4096)
        f.seek(0)

        if DELIMITER is None:
            try:
                dialect = csv.Sniffer().sniff(sample)
            except csv.Error:
                dialect = csv.excel
        else:
            dialect = csv.excel
            dialect.delimiter = DELIMITER  # type: ignore[attr-defined]

        reader = csv.DictReader(f, dialect=dialect)

        # Header-Mapping vorbereiten
        def up(s: str) -> str: return s.strip().upper()
        header = [h for h in (reader.fieldnames or [])]
        header_up = {up(h): h for h in header}

        if MAPPING:
            col = {k.upper(): v for k, v in MAPPING.items()}
        else:
            required = ["DATE", "ITEM", "GRAMS", "REASON"]
            missing = [r for r in required if r not in header_up]
            if missing:
                raise ValueError(f"Missing required columns: {', '.join(missing)}. Found: {header}")
            col = {k: header_up[k] for k in required}
            if "ID" in header_up:
                col["ID"] = header_up["ID"]

        # Zeilen importieren
        for i, row in enumerate(reader, start=2):  # 2 = erste Datenzeile nach Header
            try:
                date_str = str(row[col["DATE"]])
                item = str(row[col["ITEM"]]).strip()
                grams_str = str(row[col["GRAMS"]])
                reason = str(row[col["REASON"]]).strip()
                id_value = None
                if "ID" in col and row.get(col["ID"]):
                    id_value = str(row[col["ID"]]).strip() or None

                grams = PARSE_INT_NONNEGATIVE(grams_str)
                # ENTRY erzeugen (parst Datum intern; normalisiert Strings)
                entry = ENTRY.CREATE(ITEM=item, GRAMS=grams, REASON=reason, DATE_STR=date_str)

                # Falls CSV eine ID mitbringt, diese verwenden (ENTRY ist frozen, daher neu konstruieren)
                if id_value:
                    entry = ENTRY(
                        ID=id_value,
                        DATE=entry.DATE,
                        ITEM=entry.ITEM,
                        GRAMS=entry.GRAMS,
                        REASON=entry.REASON,
                    )

                if not DRY_RUN:
                    STORE.APPEND(entry)
                added += 1
            except Exception as e:
                errors.append(f"line {i}: {e}")
                skipped += 1

    return {"added": added, "skipped": skipped, "errors": errors, "db": str(STORE.PATH)}
