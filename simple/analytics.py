
from collections import Counter     # Importiert Counter, um automatisch counts für listen zu erstellen

class Analytics:
    def total_waste(self, entries):
        return sum(e.grams for e in entries)    # Gibt die Summe der Spalte grams aller entries zurück

    def top_three_items(self, entries):
        grams_by_item = {}
        for e in entries:
            grams_by_item[e.item] = grams_by_item.get(e.item, 0) + e.grams      # Erstellt einen Eintrag oder ruft den aktuellen auf, nimmt den Eintrag oder 0 und fügt die grams für den aktuellen Eintrag hinzu
        return sorted(grams_by_item.items(), key=lambda kv: kv[1], reverse=True)[:3]
        # Sortiert das Dict nach den Values vom Schlüssel [1] (Grams) absteigend und vom 0. bis 2. Eintrag

    def waste_in_period(self, entries, start_date, end_date):   # Erklärt sich von selbst
        if end_date < start_date:
            raise ValueError("END < START")
        s_iso = start_date.isoformat(); e_iso = end_date.isoformat()
        total = 0
        for e in entries:
            if s_iso <= e.date_iso <= e_iso:
                total += e.grams
        return total

    def most_common_reason(self, entries):
        c = Counter(e.reason for e in entries)  # Erstellt einen Counter für alle Einträge in der Spalte REASON
        # print(c.most_common(2))
        # [('verdorben', 18), ('Reste vom Kochen', 16)]
        return c.most_common(1)[0][0] if c else None    # Gibt die ersten 1 größten Counter als Tupel als Liste aus, nimmt den ersten Eintrag dort den ersten Eintrag
