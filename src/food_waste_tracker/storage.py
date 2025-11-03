from __future__ import annotations
import csv
import json
import os
from pathlib import Path
from typing import Iterable, List
from .models import ENTRY

# STORAGE HANDLES DURABLE PERSISTENCE OF ENTRIES.
# SUPPORTED FORMATS: JSONL (DEFAULT) AND CSV.

class STORAGE:
    def __init__(SELF, PATH_STR: str | None = None, FORMAT: str = "JSONL") -> None:
        """
        PATH_STR:
            - FILE PATH WHERE DATA IS STORED.
            - IF NONE, USES DEFAULT UNDER USER HOME: ~/.food_waste/data.jsonl
        FORMAT:
            - "JSONL" OR "CSV" (CASE-INSENSITIVE).
        """
        HOME = Path.home()
        DEFAULT_DIR = HOME / ".food_waste"
        DEFAULT_DIR.mkdir(parents=True, exist_ok=True)
        DEFAULT_FILE = DEFAULT_DIR / "data.jsonl"
        SELF.PATH = Path(PATH_STR).expanduser() if PATH_STR else DEFAULT_FILE
        SELF.FORMAT = FORMAT.upper()
        if SELF.FORMAT not in {"JSONL", "CSV"}:
            raise ValueError("FORMAT MUST BE 'JSONL' OR 'CSV'")
        # ENSURE DIRECTORY EXISTS
        SELF.PATH.parent.mkdir(parents=True, exist_ok=True)
        # ENSURE FILE EXISTS
        if not SELF.PATH.exists():
            if SELF.FORMAT == "JSONL":
                SELF.PATH.touch()
            else:
                with SELF.PATH.open("w", newline="", encoding="utf-8") as F:
                    WRITER = csv.DictWriter(F, fieldnames=["ID", "DATE", "ITEM", "GRAMS", "REASON"])
                    WRITER.writeheader()

    def APPEND(SELF, ENTRY_OBJ: ENTRY) -> None:
        """
        APPEND A SINGLE ENTRY TO STORAGE.
        """
        if SELF.FORMAT == "JSONL":
            with SELF.PATH.open("a", encoding="utf-8") as F:
                F.write(json.dumps(ENTRY_OBJ.TO_DICT(), ensure_ascii=False) + "\n")
        else:
            FILE_EXISTS = SELF.PATH.exists() and SELF.PATH.stat().st_size > 0
            with SELF.PATH.open("a", newline="", encoding="utf-8") as F:
                WRITER = csv.DictWriter(F, fieldnames=["ID", "DATE", "ITEM", "GRAMS", "REASON"])
                if not FILE_EXISTS:
                    WRITER.writeheader()
                WRITER.writerow(ENTRY_OBJ.TO_DICT())

    def SAVE_ALL(SELF, ENTRIES: Iterable[ENTRY]) -> None:
        """
        ATOMICALLY REWRITE THE ENTIRE DATASET.
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
        READ ALL ENTRIES FROM STORAGE.
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
