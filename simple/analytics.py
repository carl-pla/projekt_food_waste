
from collections import Counter

class Analytics:
    def total_waste(self, entries):
        return sum(e.grams for e in entries)

    def top_three_items(self, entries):
        grams_by_item = {}
        for e in entries:
            grams_by_item[e.item] = grams_by_item.get(e.item, 0) + e.grams
        return sorted(grams_by_item.items(), key=lambda kv: kv[1], reverse=True)[:3]

    def waste_in_period(self, entries, start_date, end_date):
        if end_date < start_date:
            raise ValueError("END < START")
        s_iso = start_date.isoformat(); e_iso = end_date.isoformat()
        total = 0
        for e in entries:
            if s_iso <= e.date_iso <= e_iso:
                total += e.grams
        return total

    def most_common_reason(self, entries):
        c = Counter(e.reason for e in entries)
        return c.most_common(1)[0][0] if c else None
