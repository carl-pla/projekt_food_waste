
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
    raise ValueError("Unsupported date format: %r (allowed: YYYY-MM-DD, DD.MM.YYYY, YYYY/MM/DD)" % s) from last_err

def parse_int_nonnegative(s):
    v = int(str(s).strip())
    if v < 0:
        raise ValueError("Value must be >= 0")
    return v

def detect_delimiter(sample: str) -> str:
    counts = {",": sample.count(","), ";": sample.count(";"), "\t": sample.count("\t")}
    delim = max(counts, key=counts.get)
    return delim if counts[delim] > 0 else ","

def ensure_parent(path: str) -> None:
    parent = os.path.dirname(path)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
