from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, Any
from uuid import uuid4

# ALL CLASS NAMES, FUNCTION NAMES AND VARIABLES ARE UPPERCASE AS REQUESTED.

@dataclass(frozen=True)
class ENTRY:
    """
    ENTRY REPRESENTS A SINGLE FOOD WASTE RECORD.

    FIELDS:
    - ID: UNIQUE IDENTIFIER (UUID4 STRING) FOR TRACEABILITY.
    - DATE: PYTHON DATE OBJECT, WHEN THE WASTE OCCURRED.
    - ITEM: NAME OF THE FOOD ITEM.
    - GRAMS: WASTED AMOUNT IN GRAMS (NON-NEGATIVE INTEGER).
    - REASON: FREE-TEXT REASON (E.G., "VERDORBEN", "MHD ABGELAUFEN", "ZU VIEL GEKOCHT").
    """
    ID: str
    DATE: date
    ITEM: str
    GRAMS: int
    REASON: str

    @staticmethod
    def CREATE(ITEM: str, GRAMS: int, REASON: str, DATE_STR: str | None = None) -> "ENTRY":
        """
        CONVENIENCE CONSTRUCTOR:
        - PARSES DATE FROM STRING OR USES TODAY IF NONE IS PROVIDED.
        - NORMALIZES STRING FIELDS (STRIP).
        - VALIDATES GRAMS.
        """
        if GRAMS < 0:
            raise ValueError("GRAMS MUST BE >= 0")
        DATE_OBJ: date = datetime.today().date() if DATE_STR is None else ENTRY._PARSE_DATE(DATE_STR)
        return ENTRY(
            ID=str(uuid4()),
            DATE=DATE_OBJ,
            ITEM=ITEM.strip(),
            GRAMS=int(GRAMS),
            REASON=REASON.strip(),
        )

    @staticmethod
    def _PARSE_DATE(DATE_STR: str) -> date:
        """
        ACCEPTS COMMON FORMATS:
        - YYYY-MM-DD
        - DD.MM.YYYY
        - YYYY/MM/DD
        """
        FORMATS = ["%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d"]
        LAST_ERROR: Exception | None = None
        for F in FORMATS:
            try:
                return datetime.strptime(DATE_STR.strip(), F).date()
            except Exception as E:  # noqa: BLE001
                LAST_ERROR = E
        raise ValueError(f"UNSUPPORTED DATE FORMAT: {DATE_STR}") from LAST_ERROR

    def TO_DICT(self) -> Dict[str, Any]:
        """
        SERIALIZE ENTRY TO A DICT FOR STORAGE.
        """
        return {
            "ID": self.ID,
            "DATE": self.DATE.isoformat(),
            "ITEM": self.ITEM,
            "GRAMS": self.GRAMS,
            "REASON": self.REASON,
        }

    @staticmethod
    def FROM_DICT(DATA: Dict[str, Any]) -> "ENTRY":
        """
        DESERIALIZE ENTRY FROM A DICT.
        """
        return ENTRY(
            ID=str(DATA["ID"]),
            DATE=datetime.fromisoformat(DATA["DATE"]).date(),
            ITEM=str(DATA["ITEM"]),
            GRAMS=int(DATA["GRAMS"]),
            REASON=str(DATA["REASON"]),
        )
