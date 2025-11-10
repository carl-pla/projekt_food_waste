
# Food Waste Tracker – JSONL-only (modular, ohne Packaging)

**Anforderung:** CSV einlesen können, aber **immer** in **JSONL** speichern.  
Diese Variante speichert ausschließlich als JSON Lines und importiert CSV nur als Eingangsformat.

## Struktur
```
food_waste_cli_modular_jsonl/
├─ main.py           # Einstiegspunkt (startet App oder Mini-Tests)
├─ app.py            # Interaktive CLI (Menü & User-Flows)
├─ models.py         # Entry-Domainobjekt (+ Factory)
├─ storage.py        # JSONL-Store (append/read_all/save_all)
├─ analytics.py      # Auswertungen
├─ importer.py       # CSV→JSONL-Importer (Mapping/Delimiter/Encoding)
└─ utils.py          # Hilfsfunktionen
```

## Start
```bash
python main.py
```
Menü führt durch alle Funktionen.

## Wichtige Änderung
- **Kein CSV-Speichern mehr.** Storage ist immer JSONL.
- CSV kann über Menüpunkt `7)` importiert werden → die Einträge werden als JSONL abgelegt.

## CSV-Import (interaktiv)
- Pfad angeben
- Optional: Spalten-Mapping (z. B. DATE=Datum)
- Encoding/Delimiter abfragen (leer = auto/utf-8)

## Datenformat
- JSONL unter `~/.food_waste/data.jsonl` (Standard)
- Im Menü „Einstellungen“ lässt sich **nur** der Pfad ändern – **Format ist fest JSONL**.

## Mini-Tests (ohne unittest)
```bash
python main.py test
```
Erstellt temporäre Daten, prüft Summe, Zeitraum, häufigsten Grund und importiert eine ad-hoc CSV in den JSONL-Store.
