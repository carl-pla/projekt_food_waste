
import sys
import os
import csv
from datetime import date
from app import App
from models import Entry
from storage import Store
from analytics import Analytics
from importer import CsvImporter

def run_simple_tests():
    print("Running simple tests (JSONL-only)...")
    home = os.path.expanduser("~")
    tmp = os.path.join(home, ".food_waste", "test_data.jsonl")
    if os.path.exists(tmp):
        os.remove(tmp)

    store = Store(tmp)           # JSONL only
    a = Analytics()

    e1 = Entry("id1", "2025-10-01", "BROT", 120, "VERDORBEN")
    e2 = Entry("id2", "2025-10-02", "MILCH", 200, "MHD")
    store.append(e1); store.append(e2)

    data = store.read_all()
    assert len(data) == 2, "2 entries expected"
    assert a.total_waste(data) == 320
    top = a.top_three_items(data)
    assert top and top[0][0] in ("BROT","MILCH")
    s = date(2025,10,1); e = date(2025,10,2)
    assert a.waste_in_period(data, s, e) == 320
    assert a.most_common_reason(data) in ("VERDORBEN","MHD")

    # CSV import test (create CSV ad hoc and import into JSONL store)
    csv_path = tmp.replace(".jsonl", ".csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["DATE","ITEM","GRAMS","REASON"])
        writer.writeheader()
        writer.writerow({"DATE":"2025-10-03","ITEM":"OBST","GRAMS":"50","REASON":"RESTE"})
        writer.writerow({"DATE":"2025-10-04","ITEM":"BROT","GRAMS":"30","REASON":"VERDORBEN"})
    stats = CsvImporter().import_file(csv_path, store, mapping=None, dry_run=False)
    assert stats["added"] == 2

    data2 = store.read_all()
    assert len(data2) == 4, "after CSV import there should be 4 entries total"

    print("All simple tests passed.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        run_simple_tests()
        raise SystemExit(0)
    App().run()
