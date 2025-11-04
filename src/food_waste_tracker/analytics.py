from __future__ import annotations
from collections import Counter, defaultdict
from datetime import date
from typing import Dict, Iterable, List, Tuple
from .models import ENTRY

# ANALYTICS MODULE PROVIDES COMPUTATIONS REQUIRED BY THE SPEC.

def TOTAL_WASTE(ENTRIES: Iterable[ENTRY]) -> int:
    """
    Gibt die gesamte Verschwendung in Gramm zurück.
    """
    TOTAL = 0
    for E in ENTRIES:
        TOTAL += E.GRAMS
    return TOTAL

def TOP_THREE_ITEMS(ENTRIES: Iterable[ENTRY]) -> List[Tuple[str, int]]:
    """
    Gibt die 3 Einträge mit der höchsten Gesamtverschwendung zurück. (Artikelname, Gesamtgramm, absteigend sortiert.)
    """
    AGG: Dict[str, int] = defaultdict(int)  # Legt die Variable AGG als ein Dict (Standarddict) mit dem Muster str->int an
    for E in ENTRIES:
        AGG[E.ITEM] += E.GRAMS  # Legt einen neuen Eintrag im Dict an oder addiert die Grammzahl zum bestehenden Eintrag
    SORTED = sorted(AGG.items(), key=lambda X: X[1], reverse=True)  # Sortiert das dict nach den Grammzahlen absteigend
    return SORTED[:3]   # Gibt die Top 3 Einträge als Liste zurück

def WASTE_IN_PERIOD(ENTRIES: Iterable[ENTRY], START: date, END: date) -> int:
    """
    Gibt die gesamte Verschwendung in Gramm zwischen START und END (einschließlich) zurück.
    """
    TOTAL = 0
    for E in ENTRIES:
        if START <= E.DATE <= END:
            TOTAL += E.GRAMS
    return TOTAL

def MOST_COMMON_REASON(ENTRIES: Iterable[ENTRY]) -> str | None:
    """
    Gibt die am häufigsten vorkommende REASON zurück. Wenn keine Einträge vorhanden sind, wird None zurückgegeben.
    """
    # Zählt die Vorkommen jeder REASON
    C = Counter(E.REASON for E in ENTRIES)
    if not C:
        return None
    # Gibt die am häufigsten vorkommende REASON zurück
    #   (1) gibt das erste zurück, [0] nimmt das erste Tupel (gibt nur eins, aber ist im Format für mehrere und [0] nimmt den Namenswert
    return C.most_common(1)[0][0]
