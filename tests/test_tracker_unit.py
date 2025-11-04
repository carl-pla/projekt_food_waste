from __future__ import annotations
import os
import tempfile
import unittest
from datetime import date
from typing import List
from food_waste_tracker.models import ENTRY
from food_waste_tracker.storage import STORAGE
from food_waste_tracker.analytics import TOTAL_WASTE, TOP_THREE_ITEMS, WASTE_IN_PERIOD, MOST_COMMON_REASON
from food_waste_tracker.cli import BUILD_PARSER, RUN_FROM_ARGS

class TEST_FOOD_WASTE_TRACKER(unittest.TestCase):
    """
    COMPREHENSIVE UNIT TESTS COVERING STORAGE, ANALYTICS, AND CLI BEHAVIOR.
    """

    def setUp(SELF) -> None:  # noqa: N802
        SELF.TMP = tempfile.NamedTemporaryFile(delete=False)
        SELF.TMP.close()
        SELF.DB_PATH = SELF.TMP.name
        # DEFAULT FORMAT JSONL
        SELF.STORE = STORAGE(SELF.DB_PATH, "JSONL")

    def tearDown(SELF) -> None:  # noqa: N802
        try:
            os.remove(SELF.DB_PATH)
        except FileNotFoundError:
            pass

    def _SEED(SELF) -> List[ENTRY]:
        E1 = ENTRY.CREATE(ITEM="BROT", GRAMS=120, REASON="VERDORBEN", DATE_STR="2025-10-01")
        E2 = ENTRY.CREATE(ITEM="TRAUBEN", GRAMS=200, REASON="ZU VIEL GEKOCHT", DATE_STR="2025-10-02")
        E3 = ENTRY.CREATE(ITEM="BROT", GRAMS=80, REASON="MHD ABGELAUFEN", DATE_STR="2025-10-03")
        E4 = ENTRY.CREATE(ITEM="MILCH", GRAMS=500, REASON="VERDORBEN", DATE_STR="2025-10-04")
        for E in [E1, E2, E3, E4]:
            SELF.STORE.APPEND(E)
        return [E1, E2, E3, E4]

    def test_storage_roundtrip(SELF) -> None:
        ENTRIES = SELF._SEED()
        LOADED = SELF.STORE.READ_ALL()
        SELF.assertEqual(len(LOADED), len(ENTRIES))
        # ENSURE STABLE FIELDS
        SELF.assertEqual(sorted([E.ITEM for E in LOADED]), sorted([E.ITEM for E in ENTRIES]))

    def test_analytics_total(SELF) -> None:
        ENTRIES = SELF._SEED()
        SELF.assertEqual(TOTAL_WASTE(ENTRIES), 120 + 200 + 80 + 500)

    def test_analytics_top3(SELF) -> None:
        ENTRIES = SELF._SEED()
        TOP = TOP_THREE_ITEMS(ENTRIES)
        # EXPECT MILCH FIRST (500), THEN BROT (200), THEN TRAUBEN (200)
        SELF.assertEqual(TOP[0][0], "MILCH")
        # BROT TOTAL = 200
        SUM_BROT = [T for T in TOP if T[0] == "BROT"][0][1]
        SELF.assertEqual(SUM_BROT, 200)

    def test_analytics_period(SELF) -> None:
        ENTRIES = SELF._SEED()
        T = WASTE_IN_PERIOD(ENTRIES, date(2025, 10, 2), date(2025, 10, 3))
        SELF.assertEqual(T, 200 + 80)

    def test_analytics_common_reason(SELF) -> None:
        ENTRIES = SELF._SEED()
        R = MOST_COMMON_REASON(ENTRIES)
        SELF.assertEqual(R, "VERDORBEN")

    def test_cli_add_and_total(SELF) -> None:
        # ADD ENTRY VIA CLI
        PARSER = BUILD_PARSER()
        ARGS = PARSER.parse_args(
            ["--db", SELF.DB_PATH, "--format", "JSONL", "add", "--date", "2025-10-05", "--item", "JOGHURT", "--grams", "150", "--reason", "MHD ABGELAUFEN"]
        )
        CODE = RUN_FROM_ARGS(ARGS)
        SELF.assertEqual(CODE, 0)
        # CHECK TOTAL > 0
        PARSER2 = BUILD_PARSER()
        ARGS2 = PARSER2.parse_args(["--db", SELF.DB_PATH, "--format", "JSONL", "total"])
        # CAPTURE PRINTED OUTPUT BY TEMPORARY REDIRECTION
        import io
        import sys

        BUF = io.StringIO()
        OLD = sys.stdout
        try:
            sys.stdout = BUF
            CODE2 = RUN_FROM_ARGS(ARGS2)
        finally:
            sys.stdout = OLD
        SELF.assertEqual(CODE2, 0)
        OUT = BUF.getvalue()
        SELF.assertIn("TOTAL WASTE:", OUT)

    def test_cli_period_validation(SELF) -> None:
        # INVALID PERIOD (END < START) SHOULD RAISE
        PARSER = BUILD_PARSER()
        ARGS = PARSER.parse_args(["--db", SELF.DB_PATH, "--format", "JSONL", "period", "--start", "2025-10-05", "--end", "2025-10-01"])
        with SELF.assertRaises(ValueError):
            RUN_FROM_ARGS(ARGS)

    def test_csv_storage(SELF) -> None:
        # RE-INIT STORE AS CSV ON SAME PATH (OVERWRITE)
        SELF.STORE = STORAGE(SELF.DB_PATH, "CSV")
        E = ENTRY.CREATE(ITEM="KÄSE", GRAMS=50, REASON="RESTE", DATE_STR="2025-10-06")
        SELF.STORE.APPEND(E)
        LOADED = SELF.STORE.READ_ALL()
        SELF.assertEqual(len(LOADED), 1)
        SELF.assertEqual(LOADED[0].ITEM, "KÄSE")

if __name__ == "__main__":
    unittest.main()
