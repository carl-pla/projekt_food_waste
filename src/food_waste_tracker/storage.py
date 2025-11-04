from __future__ import annotations
import csv
import json
import os
from pathlib import Path
from typing import Iterable, List
from .models import ENTRY

# Die Datei speichert und liest Einträge in verschiedenen Formaten (JSONL und CSV).

class STORAGE:
    def __init__(SELF, PATH_STR: str | None = None, FORMAT: str = "JSONL") -> None:
        """
        PATH_STR:
            - FILE PATH WHERE DATA IS STORED.
            - IF NONE, USES DEFAULT UNDER USER HOME: ~/.food_waste/data.jsonl
        FORMAT:
            - "JSONL" OR "CSV" (CASE-INSENSITIVE).
        PATH_STR:
            - Dateipfad, an dem die Daten gespeichert sind
            - Wenn keiner angegeben ist, wird der Standardpfad unter dem Benutzerverzeichnis verwendet: ~/.food_waste/data.jsonl
        FORMAT:
            - "JSONL" oder "CSV" (gross-/kleinschreibung unabhängig).
        """
        HOME = Path.home()
        DEFAULT_DIR = HOME / ".food_waste"
        DEFAULT_DIR.mkdir(parents=True, exist_ok=True)  # Die Zeile stellt sicher, dass das Verzeichnis existiert, falls nicht, wird es erstellt.
        DEFAULT_FILE = DEFAULT_DIR / "data.jsonl"
        SELF.PATH = Path(PATH_STR).expanduser() if PATH_STR else DEFAULT_FILE   # expanduser() ersetzt ~ durch das Benutzerverzeichnis
        SELF.FORMAT = FORMAT.upper()
        if SELF.FORMAT not in {"JSONL", "CSV"}:
            raise ValueError("FORMAT MUST BE 'JSONL' OR 'CSV'")
        # Prüftt, ob das Verzeichnis existiert, und erstellt es bei Bedarf
        SELF.PATH.parent.mkdir(parents=True, exist_ok=True)
        # Prüft, ob die Datei existiert, und erstellt sie bei Bedarf mit dem richtigen Header
        if not SELF.PATH.exists():
            if SELF.FORMAT == "JSONL":
                SELF.PATH.touch()   # Erstellt eine leere Datei
            else:
                with SELF.PATH.open("w", newline="", encoding="utf-8") as F:    # newline="" verhindert zusätzliche Leerzeilen in Windows
                    WRITER = csv.DictWriter(F, fieldnames=["ID", "DATE", "ITEM", "GRAMS", "REASON"])
                    WRITER.writeheader()

    def APPEND(SELF, ENTRY_OBJ: ENTRY) -> None:
        """
        Fügt einen einzelnen Eintrag zum Speicher hinzu.
        """
        if SELF.FORMAT == "JSONL":
            with SELF.PATH.open("a", encoding="utf-8") as F:    # mode "a" steht für append (anhängen)
                F.write(json.dumps(ENTRY_OBJ.TO_DICT(), ensure_ascii=False) + "\n")
        else:
            FILE_EXISTS = SELF.PATH.exists() and SELF.PATH.stat().st_size > 0   # Prüft, ob die Datei existiert und nicht leer ist
            with SELF.PATH.open("a", newline="", encoding="utf-8") as F:
                WRITER = csv.DictWriter(F, fieldnames=["ID", "DATE", "ITEM", "GRAMS", "REASON"])
                if not FILE_EXISTS:
                    WRITER.writeheader()    # Schreibt den Header (WRITER), wenn die Datei neu ist
                WRITER.writerow(ENTRY_OBJ.TO_DICT())    # writerow schreibt eine einzelne Zeile in die CSV-Datei

    def SAVE_ALL(SELF, ENTRIES: Iterable[ENTRY]) -> None:
        """
        Schreibt den gesamten Datensatz atomar neu, um Datenverlust zu vermeiden, weil APPEND nicht für alle Einträge geeignet ist.
        """
        TMP_PATH = SELF.PATH.with_suffix(SELF.PATH.suffix + ".tmp")
        if SELF.FORMAT == "JSONL":
            with TMP_PATH.open("w", encoding="utf-8") as F:
                for E in ENTRIES:
                    F.write(json.dumps(E.TO_DICT(), ensure_ascii=False) + "\n")
        else:
            with TMP_PATH.open("w", newline="", encoding="utf-8") as F:
                WRITER = csv.DictWriter(F, fieldnames=["ID", "DATE", "ITEM", "GRAMS", "REASON"])
                WRITER.writeheader()
                for E in ENTRIES:
                    WRITER.writerow(E.TO_DICT())
        os.replace(TMP_PATH, SELF.PATH)

    def READ_ALL(SELF) -> List[ENTRY]:
        """
        Liest alle Einträge aus dem Speicher.
        """
        RESULT: List[ENTRY] = []
        if not SELF.PATH.exists():
            return RESULT
        if SELF.FORMAT == "JSONL":
            with SELF.PATH.open("r", encoding="utf-8") as F:
                for LINE in F:
                    LINE = LINE.strip()
                    if not LINE:
                        continue
                    DATA = json.loads(LINE)
                    RESULT.append(ENTRY.FROM_DICT(DATA))
        else:
            with SELF.PATH.open("r", newline="", encoding="utf-8") as F:
                READER = csv.DictReader(F)
                for ROW in READER:
                    RESULT.append(ENTRY.FROM_DICT(ROW))
        return RESULT
