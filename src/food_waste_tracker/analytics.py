from __future__ import annotations
from collections import Counter, defaultdict
from datetime import date
from typing import Dict, Iterable, List, Tuple
from .models import ENTRY

# ANALYTICS MODULE PROVIDES COMPUTATIONS REQUIRED BY THE SPEC.

def TOTAL_WASTE(ENTRIES: Iterable[ENTRY]) -> int:
    """
    RETURN TOTAL GRAMS WASTED ACROSS ALL ENTRIES.
    """
    TOTAL = 0
    for E in ENTRIES:
        TOTAL += E.GRAMS
    return TOTAL

def TOP_THREE_ITEMS(ENTRIES: Iterable[ENTRY]) -> List[Tuple[str, int]]:
    """
    RETURN TOP THREE ITEMS BY TOTAL WASTE (ITEM NAME, TOTAL GRAMS), DESCENDING.
    """
    AGG: Dict[str, int] = defaultdict(int)
    for E in ENTRIES:
        AGG[E.ITEM] += E.GRAMS
    SORTED = sorted(AGG.items(), key=lambda X: X[1], reverse=True)
    return SORTED[:3]

def WASTE_IN_PERIOD(ENTRIES: Iterable[ENTRY], START: date, END: date) -> int:
    """
    RETURN TOTAL WASTE BETWEEN START AND END (INCLUSIVE).
    """
    TOTAL = 0
    for E in ENTRIES:
        if START <= E.DATE <= END:
            TOTAL += E.GRAMS
    return TOTAL

def MOST_COMMON_REASON(ENTRIES: Iterable[ENTRY]) -> str | None:
    """
    RETURN MOST FREQUENT REASON OR NONE IF NO DATA.
    """
    C = Counter(E.REASON for E in ENTRIES)
    if not C:
        return None
    return C.most_common(1)[0][0]
