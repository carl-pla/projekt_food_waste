# Food Waste Tracker

Ein performantes CLI-Tool, um Lebensmittelverschwendung zu protokollieren und auszuwerten – mit **JSONL**/**CSV**-Persistenz, robusten Datumsparsern und integrierten Analytics.

## Features
- `add`, `list`, `total`, `top3`, `period`, `common-reason`
- JSONL (default) oder CSV Speicherung
- Sichere, atomare Schreibvorgänge
- Tests via `unittest`

## Installation (Editable)
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## Nutzung
```bash
# Eintrag hinzufügen (heute)
food-waste-tracker add --item "Brot" --grams 120 --reason "verdorben"

# Mit Datum
food-waste-tracker add --date 03.11.2025 --item "Milch" --grams 500 --reason "MHD abgelaufen"

# Gesamtsumme
food-waste-tracker total

# Top 3 Artikel
food-waste-tracker top3

# Zeitraum (inklusive)
food-waste-tracker period --start 2025-10-01 --end 2025-10-31

# Häufigster Grund
food-waste-tracker common-reason
```

> Standardpfad der Datenbank: `~/.food_waste/data.jsonl`.  
> Alternativ: Umgebungsvariable `FOOD_WASTE_TRACKER_PATH` setzen oder `--db` verwenden.

## Tests
```bash
python -m unittest
```

## Lizenz
MIT
