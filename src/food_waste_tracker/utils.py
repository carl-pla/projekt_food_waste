from __future__ import annotations
from datetime import datetime, date
from typing import Optional

# UTILS FOR DATE PARSING AND VALIDATION.

def PARSE_DATE(VAL: str) -> date:
    """
    PARSE A DATE STRING IN COMMON FORMATS:
    - YYYY-MM-DD
    - DD.MM.YYYY
    - YYYY/MM/DD
    """
    FORMATS = ["%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d"]
    LAST_ERROR: Exception | None = None
    for F in FORMATS:
        try:
            return datetime.strptime(VAL.strip(), F).date()
        except Exception as E:  # noqa: BLE001
            LAST_ERROR = E
    raise ValueError(f"UNSUPPORTED DATE FORMAT: {VAL}") from LAST_ERROR

def PARSE_INT_NONNEGATIVE(VAL: str) -> int:
    """
    PARSE NON-NEGATIVE INTEGER FROM STRING.
    """
    X = int(VAL)
    if X < 0:
        raise ValueError("VALUE MUST BE NON-NEGATIVE")
    return X

def OPTIONAL_STRIP(VAL: Optional[str]) -> Optional[str]:
    """
    STRIP STRING OR PASS THROUGH NONE.
    """
    return VAL.strip() if isinstance(VAL, str) else VAL
