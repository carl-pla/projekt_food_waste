# Testdatei ohne unittest/pytest (no unittest/pytest)
from __future__ import annotations
import os, tempfile, io, sys
from datetime import date
from typing import List

# Testet, ob das Paket installiert ist; wenn nicht, fügt es ./src zu sys.path hinzu
try:
    from food_waste_tracker.models import ENTRY
    from food_waste_tracker.storage import STORAGE
    from food_waste_tracker.analytics import TOTAL_WASTE, TOP_THREE_ITEMS, WASTE_IN_PERIOD, MOST_COMMON_REASON
    from food_waste_tracker.cli import BUILD_PARSER, RUN_FROM_ARGS
except ImportError:
    import pathlib
    sys.path.insert(0, str((pathlib.Path(__file__).resolve().parent / "src").resolve()))
    from food_waste_tracker.models import ENTRY
    from food_waste_tracker.storage import STORAGE
    from food_waste_tracker.analytics import TOTAL_WASTE, TOP_THREE_ITEMS, WASTE_IN_PERIOD, MOST_COMMON_REASON
    from food_waste_tracker.cli import BUILD_PARSER, RUN_FROM_ARGS

class TempDB:   # Hilfsklasse für temporäre Datenbanken in Tests
    def __init__(self, fmt: str = "JSONL"):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)    # Erstelle eine temporäre Datei, die nicht automatisch gelöscht wird
        self.tmp.close()    # Schließe die Datei, damit STORAGE sie öffnen kann
        self.db_path = self.tmp.name
        self.store = STORAGE(self.db_path, fmt)

    def cleanup(self) -> None:
        try:
            os.remove(self.db_path)
        except FileNotFoundError:
            pass

def seed(store: STORAGE):   # Füllt den Speicher mit Beispiel-Einträgen
    e1 = ENTRY.CREATE(ITEM="BROT", GRAMS=120, REASON="VERDORBEN", DATE_STR="2025-10-01")
    e2 = ENTRY.CREATE(ITEM="TRAUBEN", GRAMS=200, REASON="ZU VIEL GEKOCHT", DATE_STR="2025-10-02")
    e3 = ENTRY.CREATE(ITEM="BROT", GRAMS=80, REASON="MHD ABGELAUFEN", DATE_STR="2025-10-03")
    e4 = ENTRY.CREATE(ITEM="MILCH", GRAMS=500, REASON="VERDORBEN", DATE_STR="2025-10-04")
    for e in (e1, e2, e3, e4):
        store.APPEND(e)
    return [e1, e2, e3, e4]

def run_test(name: str, fn):
    try:
        fn()
        print(f"[PASS] {name}")
        return True
    except AssertionError as e:
        print(f"[FAIL] {name}: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {name}: {type(e).__name__}: {e}")
        return False

def test_storage_roundtrip():
    t = TempDB("JSONL")
    try:
        entries = seed(t.store)
        loaded = t.store.READ_ALL()
        assert len(loaded) == len(entries), "Loaded entries count mismatch"
        assert sorted([e.ITEM for e in loaded]) == sorted([e.ITEM for e in entries]), "Items mismatch"
    finally:
        t.cleanup()

def test_analytics_total():
    t = TempDB("JSONL")
    try:
        entries = seed(t.store)
        assert TOTAL_WASTE(entries) == 120 + 200 + 80 + 500, "Total waste incorrect"
    finally:
        t.cleanup()

def test_analytics_top3():
    t = TempDB("JSONL")
    try:
        entries = seed(t.store)
        top = TOP_THREE_ITEMS(entries)
        assert top[0][0] == "MILCH", "Top #1 item should be MILCH"
        sum_brot = [T for T in top if T[0] == "BROT"][0][1]
        assert sum_brot == 200, "Aggregated BROT grams should be 200"
    finally:
        t.cleanup()

def test_analytics_period():
    t = TempDB("JSONL")
    try:
        entries = seed(t.store)
        total = WASTE_IN_PERIOD(entries, date(2025,10,2), date(2025,10,3))
        assert total == 200 + 80, "Period total incorrect"
    finally:
        t.cleanup()

def test_analytics_common_reason():
    t = TempDB("JSONL")
    try:
        entries = seed(t.store)
        r = MOST_COMMON_REASON(entries)
        assert r == "VERDORBEN", "Most common reason should be VERDORBEN"
    finally:
        t.cleanup()

def test_cli_add_and_total():
    t = TempDB("JSONL")
    try:
        parser = BUILD_PARSER()
        args = parser.parse_args(["--db", t.db_path, "--format", "JSONL",
                                  "add", "--date", "2025-10-05", "--item", "JOGHURT",
                                  "--grams", "150", "--reason", "MHD ABGELAUFEN"])
        code = RUN_FROM_ARGS(args)
        assert code == 0, "CLI add returned non-zero"

        parser2 = BUILD_PARSER()
        args2 = parser2.parse_args(["--db", t.db_path, "--format", "JSONL", "total"])
        buf = io.StringIO()
        old = sys.stdout
        try:
            sys.stdout = buf
            code2 = RUN_FROM_ARGS(args2)
        finally:
            sys.stdout = old
        assert code2 == 0, "CLI total returned non-zero"
        out = buf.getvalue()
        assert "TOTAL WASTE:" in out, "CLI total did not print expected text"
    finally:
        t.cleanup()

def test_cli_period_validation():
    t = TempDB("JSONL")
    try:
        parser = BUILD_PARSER()
        args = parser.parse_args(["--db", t.db_path, "--format", "JSONL",
                                  "period", "--start", "2025-10-05", "--end", "2025-10-01"])
        # Expect ValueError because end < start
        try:
            RUN_FROM_ARGS(args)
        except ValueError:
            pass
        else:
            assert False, "Expected ValueError for invalid period"
    finally:
        t.cleanup()

def test_csv_storage():
    t = TempDB("CSV")
    try:
        e = ENTRY.CREATE(ITEM="KÄSE", GRAMS=50, REASON="RESTE", DATE_STR="2025-10-06")
        t.store.APPEND(e)
        loaded = t.store.READ_ALL()
        assert len(loaded) == 1, "CSV load count incorrect"
        assert loaded[0].ITEM == "KÄSE", "CSV item mismatch"
    finally:
        t.cleanup()

def main():
    tests = [
        ("storage_roundtrip", test_storage_roundtrip),
        ("analytics_total", test_analytics_total),
        ("analytics_top3", test_analytics_top3),
        ("analytics_period", test_analytics_period),
        ("analytics_common_reason", test_analytics_common_reason),
        ("cli_add_and_total", test_cli_add_and_total),
        ("cli_period_validation", test_cli_period_validation),
        ("csv_storage", test_csv_storage),
    ]
    passed = 0
    for name, fn in tests:
        ok = run_test(name, fn)
        if ok:
            passed += 1
    total = len(tests)
    print(f"\n{passed}/{total} tests passed")
    if passed != total:
        sys.exit(1)

if __name__ == "__main__":
    main()
