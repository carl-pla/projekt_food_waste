
import os
import tempfile
import csv
from datetime import date

from models import Entry, new_entry, entry_from_dict
from utils import parse_date_or_today, parse_int_nonnegative, detect_delimiter
from storage import Store
from analytics import Analytics
from importer import CsvImporter


def run_test(name, func):
    """Hilfsfunktion: führt einen Test aus und gibt ein kurzes Ergebnis aus."""
    try:
        func()
        print(f"[OK]   {name}")
    except AssertionError as e:
        print(f"[FAIL] {name} -> {e}")
    except Exception as e:
        print(f"[ERROR]{name} -> unerwartete Exception: {e}")


# ---------------------- Tests für models.py ----------------------


def test_models_entry_and_factory():
    # Direktes Erzeugen eines Entry
    e = Entry("id123", "2025-01-02", "  Brot  ", "42", "  Verdorben  ")
    assert e.id == "id123"
    assert e.date_iso == "2025-01-02"
    assert e.item == "Brot"          # getrimmt
    assert e.grams == 42             # in int umgewandelt
    assert e.reason == "Verdorben"   # getrimmt

    d = e.to_dict()
    assert d == {
        "ID": "id123",
        "DATE": "2025-01-02",
        "ITEM": "Brot",
        "GRAMS": 42,
        "REASON": "Verdorben",
    }

    # Wieder zurück aus Dict
    e2 = entry_from_dict(d)
    assert isinstance(e2, Entry)
    assert e2.id == "id123"
    assert e2.item == "Brot"
    assert e2.grams == 42

    # new_entry erzeugt eine neue UUID und ISO-Datum
    some_date = date(2025, 1, 3)
    e3 = new_entry("Milch", 100, "Rest", some_date)
    assert isinstance(e3, Entry)
    assert e3.item == "Milch"
    assert e3.grams == 100
    assert e3.date_iso == "2025-01-03"
    assert e3.id and isinstance(e3.id, str) and len(e3.id) > 8

    # date_obj wandelt ISO-String zurück in date
    assert e3.date_obj() == some_date


# ---------------------- Tests für utils.py ----------------------


def test_utils_parse_date_or_today():
    today = date.today()
    # Leere und None -> heute
    assert parse_date_or_today("") == today
    assert parse_date_or_today(None) == today

    # Verschiedene Formate
    d1 = parse_date_or_today("2025-01-02")
    d2 = parse_date_or_today("02.01.2025")
    d3 = parse_date_or_today("2025/01/02")
    assert d1 == d2 == d3 == date(2025, 1, 2)

    # Falsches Format -> ValueError
    try:
        parse_date_or_today("blabla")
    except ValueError:
        pass
    else:
        raise AssertionError("parse_date_or_today sollte bei ungültigem Datum ValueError werfen")


def test_utils_parse_int_nonnegative_and_delimiter():
    # parse_int_nonnegative
    assert parse_int_nonnegative("42") == 42
    assert parse_int_nonnegative("  7  ") == 7

    try:
        parse_int_nonnegative("-1")
    except ValueError:
        pass
    else:
        raise AssertionError("parse_int_nonnegative sollte bei negativer Zahl ValueError werfen")

    try:
        parse_int_nonnegative("keine Zahl")
    except ValueError:
        pass
    else:
        raise AssertionError("parse_int_nonnegative sollte bei Nicht-Zahl ValueError werfen")

    # detect_delimiter
    sample_comma = "DATE,ITEM,GRAMS\n2025-01-01,BROT,50"
    sample_semicolon = "DATE;ITEM;GRAMS\n2025-01-01;BROT;50"
    sample_none = "nur Text ohne Trennzeichen"

    assert detect_delimiter(sample_comma) == ","
    assert detect_delimiter(sample_semicolon) == ";"
    # Wenn keiner gefunden wird, soll der Standard ',' zurückkommen
    assert detect_delimiter(sample_none) == ","


# ---------------------- Tests für storage.py ----------------------


def test_storage_append_read():
    a = Analytics()  # wird weiter unten gebraucht, hier nur Import-Check
    del a

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_db.jsonl")
        store = Store(db_path)

        # Anfangs: Datei existiert, aber noch keine Einträge
        entries0 = store.read_all()
        assert isinstance(entries0, list)
        assert len(entries0) == 0

        # Zwei Einträge hinzufügen
        e1 = new_entry("Brot", 50, "Test1", date(2025, 1, 1))
        e2 = new_entry("Milch", 100, "Test2", date(2025, 1, 2))
        store.append(e1)
        store.append(e2)

        entries = store.read_all()
        assert len(entries) == 2
        assert entries[0].item == "Brot"
        assert entries[1].item == "Milch"


# ---------------------- Tests für analytics.py ----------------------


def test_analytics_functions():
    a = Analytics()

    entries = [
        Entry("1", "2025-01-01", "Brot", 100, "Verdorben"),
        Entry("2", "2025-01-02", "Milch", 200, "Reste"),
        Entry("3", "2025-01-03", "Brot", 50, "Reste"),
        Entry("4", "2025-02-01", "Apfel", 30, "Verdorben"),
    ]

    # total_waste
    assert a.total_waste(entries) == 380

    # top_three_items – wir schauen auf die aggregierten Gramm pro Item
    top = a.top_three_items(entries)
    assert 1 <= len(top) <= 3
    top_dict = dict(top)
    assert top_dict["Brot"] == 150
    assert top_dict["Milch"] == 200
    assert top_dict["Apfel"] == 30

    # Prüfen, dass nach Gramm absteigend sortiert ist
    grams_sorted = [g for _, g in top]
    assert grams_sorted == sorted(grams_sorted, reverse=True)

    # waste_in_period
    s = date(2025, 1, 1)
    e = date(2025, 1, 31)
    assert a.waste_in_period(entries, s, e) == 350  # Einträge 1,2,3

    # Ungültiger Zeitraum (Ende < Start) -> ValueError
    try:
        a.waste_in_period(entries, date(2025, 2, 1), date(2025, 1, 1))
    except ValueError:
        pass
    else:
        raise AssertionError("waste_in_period sollte bei END<START ValueError werfen")

    # most_common_reason
    r = a.most_common_reason(entries)
    # Es gibt zwei Gründe mit gleicher Häufigkeit, akzeptiere beide
    assert r in ("Verdorben", "Reste")

    # Keine Einträge -> None
    assert a.most_common_reason([]) is None


# ---------------------- Tests für importer.py ----------------------


def test_importer_basic_and_errors():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "import_db.jsonl")
        store = Store(db_path)
        importer = CsvImporter()

        # 1) Gültige CSV mit Komma als Trennzeichen
        csv_path = os.path.join(tmpdir, "ok.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["DATE", "ITEM", "GRAMS", "REASON"])
            writer.writeheader()
            writer.writerow({"DATE": "2025-01-01", "ITEM": "Brot", "GRAMS": "50", "REASON": "Test"})
            writer.writerow({"DATE": "2025-01-02", "ITEM": "Milch", "GRAMS": "100", "REASON": "Test2"})

        stats = importer.import_file(csv_path, store, mapping=None, dry_run=False)
        assert stats["added"] == 2
        assert stats["skipped"] == 0
        assert not stats["errors"]
        entries = store.read_all()
        assert len(entries) == 2
        assert {e.item for e in entries} == {"Brot", "Milch"}

        # 2) dry_run: es werden Einträge gezählt, aber nicht gespeichert
        csv_path2 = os.path.join(tmpdir, "dryrun.csv")
        with open(csv_path2, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["DATE", "ITEM", "GRAMS", "REASON"])
            writer.writeheader()
            writer.writerow({"DATE": "2025-01-03", "ITEM": "Obst", "GRAMS": "30", "REASON": "Rest"})
        stats2 = importer.import_file(csv_path2, store, mapping=None, dry_run=True)
        assert stats2["added"] == 1
        assert stats2["skipped"] == 0
        # DB sollte unverändert bleiben (immer noch 2 Einträge)
        assert len(store.read_all()) == 2

        # 3) Fehlender Header -> ValueError
        bad_header_path = os.path.join(tmpdir, "bad_header.csv")
        with open(bad_header_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["DATE", "ITEM", "GRAMS"])  # REASON fehlt
            writer.writeheader()
            writer.writerow({"DATE": "2025-01-04", "ITEM": "Test", "GRAMS": "10"})
        try:
            importer.import_file(bad_header_path, store, mapping=None, dry_run=False)
        except ValueError:
            pass
        else:
            raise AssertionError("Importer sollte bei fehlender REASON-Spalte ValueError werfen")

        # 4) Ungültige Gramm-Angabe -> wird übersprungen und als Fehler gezählt
        csv_path3 = os.path.join(tmpdir, "invalid_row.csv")
        with open(csv_path3, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["DATE", "ITEM", "GRAMS", "REASON"])
            writer.writeheader()
            writer.writerow({"DATE": "2025-01-05", "ITEM": "Brot", "GRAMS": "20", "REASON": "ok"})
            writer.writerow({"DATE": "2025-01-06", "ITEM": "Milch", "GRAMS": "-5", "REASON": "negativ"})  # ungültig
        stats3 = importer.import_file(csv_path3, store, mapping=None, dry_run=False)
        assert stats3["added"] == 1
        assert stats3["skipped"] == 1
        assert len(stats3["errors"]) == 1


def main():
    print("=== Manuelle Tests für Food Waste Tracker ===")
    tests = [
        ("models: Entry/new_entry", test_models_entry_and_factory),
        ("utils: parse_date_or_today", test_utils_parse_date_or_today),
        ("utils: parse_int_nonnegative & detect_delimiter", test_utils_parse_int_nonnegative_and_delimiter),
        ("storage: append/read", test_storage_append_read),
        ("analytics: Funktionen", test_analytics_functions),
        ("importer: CSV-Import & Fehlerfälle", test_importer_basic_and_errors),
    ]
    for name, func in tests:
        run_test(name, func)
    print("=== Tests fertig ===")


if __name__ == "__main__":
    main()
