# app.py
import os
from datetime import date
from models import new_entry
from storage import Store, DEFAULT_DB_PATH
from analytics import Analytics
from importer import CsvImporter
from utils import parse_date_or_today


class App:
    def __init__(self):
        # Nutze den Default-Pfad aus storage.py (data.jsonl im Code-Ordner)
        self.store = Store(DEFAULT_DB_PATH)
        self.db_path = self.store.path

        self.analytics = Analytics()
        self.importer = CsvImporter()

    # ---------------- input helpers -----------------
    # Verbessern die Codequalität, man muss nicht jeden Input separat prüfen, sondern deckt das hiermit alles ab.
    # Durch den "_" am Anfang ist die Funktion nur intern aufrufbar.
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
                print(f"Bitte eine gültige ganze Zahl eingeben '>=0'")

    def _input_date(self, prompt, allow_empty=True):
        while True:
            v = input(prompt).strip()
            if not v and allow_empty:
                return None
            try:
                return parse_date_or_today(v)
            except Exception as e:
                print(f"Ungültiges Datum: {e}")

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
            print(f"{e.id}\t{e.date_iso}\t{e.item}\t{e.grams}\t{e.reason}")
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
            print(f"{i}. {item}: {grams}g")

    def show_period(self):
        start = self._input_date("Startdatum: ", allow_empty=False)
        end = self._input_date("Enddatum: ", allow_empty=False)
        entries = self.store.read_all()
        print(f"SUMME {start} bis {end}: {self.analytics.waste_in_period(entries, start, end)}g")

    def show_common_reason(self):
        entries = self.store.read_all()
        r = self.analytics.most_common_reason(entries)
        print("Kein Eintrag vorhanden." if r is None else f"HÄUFIGSTER GRUND: {r}")

    def import_csv(self):
        csvp = self._input_nonempty("CSV-Pfad: ")
        print("Optional: Spalten-Mapping angeben (ENTER = überspringen).")
        print("Zielspalten: DATE, ITEM, GRAMS, REASON, optional ID.")
        mapping = {}
        for tgt in ["DATE","ITEM","GRAMS","REASON","ID"]:
            src = self._input_optional(f"CSV-Spaltenname für {tgt} (leer=ignorieren): ")
            if src:
                mapping[tgt] = src
        enc = self._input_optional("Encoding (leer = utf-8): ") or "utf-8"
        delim = self._input_optional("Delimiter (z.B. ;, , , \\t) (leer = auto): ")

        self.importer.encoding = enc
        self.importer.delimiter = (delim or None)

        stats = self.importer.import_file(csvp, self.store, mapping=mapping or None, dry_run=False)
        print(f"Importiert: {stats["added"]}, Übersprungen: {stats["skipped"]}")
        if stats["errors"]:
            print("Fehler (erste 10):")
            for e in stats["errors"][:10]:
                print(" -", e)

    def change_settings(self):
        new_name = self._input_optional(
            f"Neuer Dateiname (leer = unverändert, aktuell: {os.path.basename(self.db_path)}): "
        )
        if new_name:
            from storage import BASE_DIR
            new_path = os.path.join(BASE_DIR, new_name)
            self.store = Store(new_path)
            self.db_path = self.store.path

        print("Einstellungen aktualisiert:")
        print(" - Speicherort:", self.db_path)
        print(" - Verzeichnis bleibt:", os.path.dirname(self.db_path))

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
