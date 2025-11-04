from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, Any
from uuid import uuid4


# Kurzschreibweise für
# class ENTRY: ...
# ENTRY = dataclass(frozen=True)(ENTRY)
# Spart manuelle Implementierung von __init__, __repr__, __eq__, etc.
# FROZEN macht die Instanz unveränderlich (immutable).
@dataclass(frozen=True)
class ENTRY:
    """
    ENTRY repräsentiert einen einzelnen Lebensmittelabfall-Eintrag.

    Felder:
    - ID: Eindeutige Kennung (UUID4 STRING) zur Nachverfolgbarkeit.
    - DATE: Python-Datumsobjekt, wann der Abfall aufgetreten ist.
    - ITEM: Name des Lebensmittelartikels.
    - GRAMS: Verschwendete Menge in Gramm (nicht-negativer Integer).
    - REASON: Freitextgrund (z.B. "VERDORBEN", "MHD ABGELAUFEN", "ZU VIEL GEKOCHT").
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

    # @staticmethod macht die Methode unabhängig von einer Instanz der Klasse aufrufbar
    # z.B. ENTRY._PARSE_DATE("2024-01-01")
    # Die Funktion funktioniert nur mit den übergebenen Parametern und hat keinen Zugriff auf self oder cls, also keine Instanz- oder Klassenvariablen.
    @staticmethod
    # _ macht die Methode "privat", also nicht für den externen Gebrauch gedacht
    # Parst ein Datums-String in gängigen Formaten und gibt ein Datumsobjekt zurück, um einheitliche Datumserstellung zu gewährleisten
    def _PARSE_DATE(DATE_STR: str) -> date:
        """
        Akzeptiert ein Datums-String in gängigen Formaten und gibt ein Datumsobjekt zurück.
        Unterstützte Formate:
        - YYYY-MM-DD
        - DD.MM.YYYY
        - YYYY/MM/DD
        """
        FORMATS = ["%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d"]
        LAST_ERROR: Exception | None = None # Initialisierung der Variable für den letzten Fehler
        for F in FORMATS:
            try:
                return datetime.strptime(DATE_STR.strip(), F).date()    # Versucht, das Datum zu parsen
            except Exception as E:  # noqa: BLE001
                LAST_ERROR = E  # Speichert den letzten Fehler, falls das Parsen fehlschlägt
        # Wenn kein Format passt, wird ein ValueError mit dem letzten Fehler ausgelöst
        raise ValueError(f"UNSUPPORTED DATE FORMAT: {DATE_STR}") from LAST_ERROR

    def TO_DICT(self) -> Dict[str, Any]:
        """
        Serialisiert das ENTRY-Objekt in ein Dictionary-Format für die Speicherung.
        Serialisiert = Umwandlung eines Objekts in ein Format, das gespeichert oder übertragen werden kann.
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
        Deserialisiert ein Dictionary-Format zurück in ein ENTRY-Objekt.
        """
        return ENTRY(
            ID=str(DATA["ID"]),
            DATE=datetime.fromisoformat(DATA["DATE"]).date(),
            ITEM=str(DATA["ITEM"]),
            GRAMS=int(DATA["GRAMS"]),
            REASON=str(DATA["REASON"]),
        )
