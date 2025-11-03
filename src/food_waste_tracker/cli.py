from __future__ import annotations
import argparse
import os
from datetime import date
from typing import List
from .models import ENTRY
from .storage import STORAGE
from .analytics import TOTAL_WASTE, TOP_THREE_ITEMS, WASTE_IN_PERIOD, MOST_COMMON_REASON
from .utils import PARSE_DATE, PARSE_INT_NONNEGATIVE, OPTIONAL_STRIP

# CLI PROVIDES A CLEAN COMMAND-LINE INTERFACE AS REQUIRED.

def _DEFAULT_PATH() -> str:
    """
    RESOLVE DEFAULT PATH FROM ENV OR HOME DIRECTORY.
    """
    ENV_PATH = os.getenv("FOOD_WASTE_TRACKER_PATH")
    if ENV_PATH:
        return os.path.expanduser(ENV_PATH)
    # DEFAULT IS ~/.food_waste/data.jsonl
    from pathlib import Path
    HOME = Path.home()
    return str((HOME / ".food_waste" / "data.jsonl").expanduser())

def BUILD_PARSER() -> argparse.ArgumentParser:
    PARSER = argparse.ArgumentParser(
        prog="FOOD-WASTE-TRACKER",
        description="TRACK HOUSEHOLD FOOD WASTE WITH PERSISTENT STORAGE AND ANALYTICS.",
    )
    PARSER.add_argument(
        "--db",
        default=_DEFAULT_PATH(),
        help="PATH TO DATA FILE (DEFAULT: ~/.food_waste/data.jsonl OR ENV FOOD_WASTE_TRACKER_PATH)",
    )
    PARSER.add_argument(
        "--format",
        choices=["JSONL", "CSV", "jsonl", "csv"],
        default="JSONL",
        help="STORAGE FORMAT (DEFAULT: JSONL)",
    )
    SUBPARSE = PARSER.add_subparsers(dest="COMMAND", required=True)

    # ADD COMMAND
    P_ADD = SUBPARSE.add_parser("add", help="ADD A NEW WASTE ENTRY")
    P_ADD.add_argument("--date", required=False, help="DATE (YYYY-MM-DD OR DD.MM.YYYY); DEFAULT: TODAY")
    P_ADD.add_argument("--item", required=True, help="FOOD ITEM NAME")
    P_ADD.add_argument("--grams", required=True, type=PARSE_INT_NONNEGATIVE, help="WASTED GRAMS (INT >= 0)")
    P_ADD.add_argument("--reason", required=True, help="REASON (FREE TEXT)")

    # LIST COMMAND
    P_LIST = SUBPARSE.add_parser("list", help="LIST ALL ENTRIES")
    P_LIST.add_argument("--limit", type=int, default=0, help="LIMIT NUMBER OF ROWS SHOWN (0=ALL)")

    # TOTAL COMMAND
    SUBPARSE.add_parser("total", help="SHOW TOTAL WASTED GRAMS")

    # TOP3 COMMAND
    SUBPARSE.add_parser("top3", help="SHOW TOP 3 ITEMS BY WASTE")

    # PERIOD COMMAND
    P_PERIOD = SUBPARSE.add_parser("period", help="SHOW TOTAL WASTE IN A DATE RANGE (INCLUSIVE)")
    P_PERIOD.add_argument("--start", required=True, help="START DATE (YYYY-MM-DD OR DD.MM.YYYY)")
    P_PERIOD.add_argument("--end", required=True, help="END DATE (YYYY-MM-DD OR DD.MM.YYYY)")

    # COMMON-REASON COMMAND
    SUBPARSE.add_parser("common-reason", help="SHOW MOST FREQUENT REASON")

    return PARSER

def RUN_FROM_ARGS(ARGS: argparse.Namespace) -> int:
    DB_PATH = ARGS.db
    FORMAT = ARGS.format.upper()
    STORE = STORAGE(DB_PATH, FORMAT)
    ENTRIES = STORE.READ_ALL()

    if ARGS.COMMAND == "add":
        DATE_STR = OPTIONAL_STRIP(ARGS.date)
        ITEM = ARGS.item
        GRAMS = int(ARGS.grams)
        REASON = ARGS.reason
        ENTRY_OBJ = ENTRY.CREATE(ITEM=ITEM, GRAMS=GRAMS, REASON=REASON, DATE_STR=DATE_STR)
        STORE.APPEND(ENTRY_OBJ)
        print(f"ADDED: {ENTRY_OBJ.ID} {ENTRY_OBJ.DATE.isoformat()} {ENTRY_OBJ.ITEM} {ENTRY_OBJ.GRAMS}G {ENTRY_OBJ.REASON}")
        return 0

    if ARGS.COMMAND == "list":
        LIMIT = int(ARGS.limit or 0)
        COUNT = 0
        for E in ENTRIES:
            print(f"{E.ID}\t{E.DATE.isoformat()}\t{E.ITEM}\t{E.GRAMS}\t{E.REASON}")
            COUNT += 1
            if LIMIT > 0 and COUNT >= LIMIT:
                break
        if COUNT == 0:
            print("NO ENTRIES")
        return 0

    if ARGS.COMMAND == "total":
        T = TOTAL_WASTE(ENTRIES)
        print(f"TOTAL WASTE: {T} G")
        return 0

    if ARGS.COMMAND == "top3":
        TOP = TOP_THREE_ITEMS(ENTRIES)
        if not TOP:
            print("NO ENTRIES")
        else:
            for RANK, (ITEM, GRAMS) in enumerate(TOP, start=1):
                print(f"{RANK}. {ITEM}: {GRAMS} G")
        return 0

    if ARGS.COMMAND == "period":
        START = PARSE_DATE(ARGS.start)
        END = PARSE_DATE(ARGS.end)
        if END < START:
            raise ValueError("END DATE MUST BE >= START DATE")
        T = WASTE_IN_PERIOD(ENTRIES, START, END)
        print(f"WASTE FROM {START.isoformat()} TO {END.isoformat()}: {T} G")
        return 0

    if ARGS.COMMAND == "common-reason":
        R = MOST_COMMON_REASON(ENTRIES)
        print("NO ENTRIES" if R is None else f"MOST COMMON REASON: {R}")
        return 0

    raise RuntimeError("UNKNOWN COMMAND")

def MAIN() -> None:
    PARSER = BUILD_PARSER()
    ARGS = PARSER.parse_args()
    EXIT_CODE = RUN_FROM_ARGS(ARGS)
    raise SystemExit(EXIT_CODE)

if __name__ == "__main__":
    MAIN()
