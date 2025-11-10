
import os
from datetime import date
from models import new_entry
from storage import Store
from analytics import Analytics
from importer import CsvImporter
from utils import parse_date_or_today

class App:
    def __init__(self):
        home = os.path.expanduser("~")
        default_path = os.path.join(home, ".food_waste", "data.jsonl")
        self.db_path = default_path
        self.store = Store(self.db_path)           # JSONL only
        self.analytics = Analytics()
        self.importer = CsvImporter()

    # ---------------- input helpers -----------------
    def _input_nonempty(self, prompt):
        while True:
            v = input(prompt).strip()
            if v:
                return v
            print("Bitte einen Wert eingeben.")

    def _input_optional(self, prompt):
        v = input(prompt).strip()
        return v if v else None

    def _input_int(self, prompt, nonneg=True):
        while True:
            v = input(prompt).strip()
            try:
                n = int(v)
                if nonneg and n < 0:
                    raise ValueError
                return n
            except Exception:
                print("Bitte eine gültige ganze Zahl eingeben%s." % (" (>= 0)" if nonneg else ""))

    def _input_date(self, prompt, allow_empty=True):
        while True:
            v = input(prompt).strip()
            if not v and allow_empty:
                return None
            try:
                return parse_date_or_today(v)
            except Exception as e:
                print("Ungültiges Datum: %s" % e)

    # ---------------- actions -----------------------
    def add_entry(self):
        item = self._input_nonempty("Item: ")
        grams = self._input_int("Gramm (>=0): ", nonneg=True)
        reason = self._input_nonempty("Grund: ")
        d = self._input_date("Datum (leer = heute, Formate: YYYY-MM-DD / DD.MM.YYYY / YYYY/MM/DD): ", allow_empty=True)
        d = d or date.today()
        e = new_entry(item, grams, reason, d)
        self.store.append(e)
        print("Hinzugefügt:", e.to_dict())

    def list_entries(self):
        entries = self.store.read_all()
        if not entries:
            print("Keine Einträge.")
            return
        limit = self._input_int("Wieviele Zeilen anzeigen? (0 = alle): ", nonneg=True)
        shown = 0
        for e in entries:
            print("%s\t%s\t%s\t%dg\t%s" % (e.id, e.date_iso, e.item, e.grams, e.reason))
            shown += 1
            if limit and shown >= limit:
                break

    def show_total(self):
        entries = self.store.read_all()
        print("TOTAL WASTE:", self.analytics.total_waste(entries), "g")

    def show_top3(self):
        entries = self.store.read_all()
        top = self.analytics.top_three_items(entries)
        if not top:
            print("Keine Einträge.")
            return
        for i, (item, grams) in enumerate(top, start=1):
            print("%d. %s: %d g" % (i, item, grams))

    def show_period(self):
        start = self._input_date("Startdatum: ", allow_empty=False)
        end = self._input_date("Enddatum: ", allow_empty=False)
        entries = self.store.read_all()
        print("SUMME %s bis %s: %d g" % (start, end, self.analytics.waste_in_period(entries, start, end)))

    def show_common_reason(self):
        entries = self.store.read_all()
        r = self.analytics.most_common_reason(entries)
        print("Kein Eintrag vorhanden." if r is None else "HÄUFIGSTER GRUND: %s" % r)

    def import_csv(self):
        csvp = self._input_nonempty("CSV-Pfad: ")
        print("Optional: Spalten-Mapping angeben (ENTER = überspringen).")
        print("Zielspalten: DATE, ITEM, GRAMS, REASON, optional ID.")
        mapping = {}
        for tgt in ["DATE","ITEM","GRAMS","REASON","ID"]:
            src = self._input_optional("CSV-Spaltenname für %s (leer=ignorieren): " % tgt)
            if src:
                mapping[tgt] = src
        enc = self._input_optional("Encoding (leer = utf-8): ") or "utf-8"
        delim = self._input_optional("Delimiter (z.B. ;, , , \\t) (leer = auto): ")

        self.importer.encoding = enc
        self.importer.delimiter = (delim or None)

        stats = self.importer.import_file(csvp, self.store, mapping=mapping or None, dry_run=False)
        print("Importiert: %d, Übersprungen: %d" % (stats["added"], stats["skipped"]))
        if stats["errors"]:
            print("Fehler (erste 10):")
            for e in stats["errors"][:10]:
                print(" -", e)

    def change_settings(self):
        new_path = self._input_optional("Neuer DB-Pfad (leer = unverändert, aktuell: %s): " % self.db_path)
        if new_path:
            self.db_path = os.path.expanduser(new_path)
            self.store = Store(self.db_path)   # JSONL only
        print("Einstellungen aktualisiert:", self.db_path, "(Format: JSONL)")

    def run(self):
        print("=== Food Waste Tracker (JSONL-only, modular) ===")
        while True:
            print("\nAktuelle DB:", self.db_path, "| Format: JSONL (fest)")
            print("1) Eintrag hinzufügen")
            print("2) Einträge anzeigen")
            print("3) Gesamt (TOTAL)")
            print("4) Top 3 Items")
            print("5) Summe in Zeitraum")
            print("6) Häufigster Grund")
            print("7) CSV importieren → JSONL")
            print("8) Einstellungen ändern (nur Pfad)")
            print("9) Beenden")
            choice = input("Auswahl (1-9): ").strip()
            try:
                if choice == "1":   self.add_entry()
                elif choice == "2": self.list_entries()
                elif choice == "3": self.show_total()
                elif choice == "4": self.show_top3()
                elif choice == "5": self.show_period()
                elif choice == "6": self.show_common_reason()
                elif choice == "7": self.import_csv()
                elif choice == "8": self.change_settings()
                elif choice == "9":
                    print("Tschüss!")
                    return
                else:
                    print("Bitte 1-9 wählen.")
            except Exception as ex:
                print("FEHLER:", ex)
