
import os
from datetime import datetime, date

DATE_FORMATS = ["%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d"]

def parse_date_or_today(s):
    """Return date from string (several formats). Empty/None => today()."""
    if not s or not str(s).strip():
        return datetime.today().date()
    s = str(s).strip()
    last_err = None
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(s, f).date()
        except Exception as e:
            last_err = e
    raise ValueError(f"Unsupported date format: {last_err} (allowed: YYYY-MM-DD, DD.MM.YYYY, YYYY/MM/DD)")

def parse_int_nonnegative(s):
    try:
        v = int(str(s).strip())
        if v < 0:
            raise ValueError("Value must be >= 0")
        return v
    except ValueError as e:
        raise ValueError(f"Bitte eine ganze Zahl eingeben (aktuell: {s!r})")

def detect_delimiter(sample: str) -> str:
    counts = {",": sample.count(","), ";": sample.count(";"), "\t": sample.count("\t")}     # Zählt, wie oft die typischen csv delimiter im sample vorkommen
    delim = max(counts, key=counts.get)     # Prüft, welcher Count-Wert am höchsten ist
    return delim if counts[delim] > 0 else ","      # Gibt den höchsten zurück, wenn > 0, ansonsten den Standard ","
