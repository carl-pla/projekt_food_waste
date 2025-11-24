from datetime import datetime
import os
import csv

from analyse import (
    gesamte_verschwendung,
    lebensmittel_meiste_verschwendung,
    zeitraum,
    grund,
)


# =========================
# Datei-Funktionen
# =========================

def _data_path():
    """Pfad zur data.csv im aktuellen Ordner."""
    return os.path.join(os.path.dirname(__file__), "data.csv")


def read_data():
    """Liest die CSV-Datei ein und gibt eine Liste von Zeilen-Dicts zurück."""
    path = _data_path()
    rows = []

    if not os.path.exists(path):
        return rows
    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row.get("lebensmittel", "")

            # Headerzeile(n) oder leere Namen ignorieren
            if not name or name == "lebensmittel":
                continue

            rows.append(
                {
                    "lebensmittel": name,
                    "datum": row.get("datum", ""),
                    "waste": row.get("waste", ""),
                    "grund": row.get("grund", ""),
                }
            )

    return rows


def write_data(new_rows):
    """Hängt neue Zeilen an die CSV-Datei an.

    `new_rows` ist eine Liste von Dicts mit den Keys:
    lebensmittel, datum, waste, grund
    """
    path = _data_path()
    file_exists = os.path.exists(path)
    write_header = (not file_exists) or os.path.getsize(path) == 0

    with open(path, "a", newline="", encoding="utf-8") as file:
        fieldnames = ["lebensmittel", "datum", "waste", "grund"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        for row in new_rows:
            writer.writerow(
                {
                    "lebensmittel": row.get("lebensmittel", ""),
                    "datum": row.get("datum", ""),
                    "waste": row.get("waste", ""),
                    "grund": row.get("grund", ""),
                }
            )


def write_dict(lebensmittel, datum, waste, grund, data):
    """Erstellt einen neuen Datensatz, hängt ihn an `data` an und gibt ihn zurück."""
    row = {
        "lebensmittel": lebensmittel,
        "datum": str(datum),
        "waste": str(waste),
        "grund": grund,
    }

    data.append(row)
    return row


def check_date_format(date_text):
    """Prüft, ob ein Datum im Format YYYY-MM-DD gültig ist."""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# =========================
# Eingabe-Helfer
# =========================

def _input_date(prompt_text):
    while True:
        date_text = input(prompt_text).strip()
        if check_date_format(date_text):
            return date_text
        print("Ungültiges Datum! Bitte im Format yyyy-mm-dd eingeben.\n")


def _input_date_today(prompt_text):
    while True:
        # Hinweis im Prompt ergänzen
        date_text = input(f"{prompt_text} (leer = heutiges Datum): ").strip()

        # Wenn nichts eingegeben wird → heutiges Datum verwenden
        if not date_text:
            today = datetime.today().date()
            return today.strftime("%Y-%m-%d")

        # Sonst wie bisher prüfen
        if check_date_format(date_text):
            return date_text

        print("Ungültiges Datum! Bitte im Format yyyy-mm-dd eingeben.\n")


def _input_non_empty(prompt_text):
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Eingabe darf nicht leer sein.\n")


def _input_positive_float(prompt_text):
    while True:
        try:
            value = float(input(prompt_text).strip())
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Bitte eine gültige Zahl größer als 0 eingeben.\n")


# =========================
# Menü-Logik
# =========================

def _menu_auslesen(data):
    print(
        "\nWillkommen beim Daten auslesen\n"
        "Was möchten Sie wissen?\n"
        "a) Gesamte Menge an weggeworfenen Lebensmitteln anzeigen\n"
        "b) Die drei Lebensmittel mit der größten weggeworfenen Menge\n"
        "c) Menge an weggeworfenen Lebensmitteln in einem bestimmten Zeitraum\n"
        "d) Häufigste Gründe für das Wegwerfen\n"
    )

    auswahl = input("\nIhre Auswahl (a | b | c | d): ").lower().strip()

    if auswahl not in {"a", "b", "c", "d"}:
        print("Ungültige Auswahl. Bitte a, b, c oder d eingeben.\n")
        return

    if auswahl == "a":
        gesamt = gesamte_verschwendung(data)
        print(
            f"Deine Auswahl: {auswahl}\n"
            f"Gesamte Menge an weggeworfenen Lebensmitteln: {gesamt} g"
        )

    elif auswahl == "b":
        top3 = lebensmittel_meiste_verschwendung(data)
        print("Deine Auswahl: b")
        print("Die drei Lebensmittel mit der größten weggeworfenen Menge:")
        for name, menge in top3:
            print(f"- {name}: {menge} g")

    elif auswahl == "c":
        start_datum = _input_date("Geben Sie das Startdatum ein (yyyy-mm-dd): ")
        end_datum = _input_date("Geben Sie das Enddatum ein (yyyy-mm-dd): ")

        daten_im_zeitraum = zeitraum(start_datum, end_datum, data)
        gesamt = gesamte_verschwendung(daten_im_zeitraum)

        print("Deine Auswahl: c")
        print(
            f"Im Zeitraum von {start_datum} bis {end_datum} wurden insgesamt "
            f"{gesamt} g Lebensmittel weggeworfen."
        )

    elif auswahl == "d":
        haeufigste_gruende = grund(data)
        print("Deine Auswahl: d")
        print("Häufigster Grund/Gründe für das Wegwerfen:")
        for reason, count in haeufigste_gruende:
            print(f"- {reason}: {count} mal")


def _menu_hinzufuegen(data):
    print("\nWillkommen, welche Daten möchten Sie hinzufügen?\n")

    datum = _input_date_today("Datum (yyyy-mm-dd): ")
    lebensmittel = _input_non_empty("Lebensmittel: ")
    menge = _input_positive_float("Menge (in Gramm): ")
    grund_text = _input_non_empty("Grund (Stichwort): ")

    row = write_dict(lebensmittel, datum, menge, grund_text, data)
    write_data([row])

    print("\nEintrag erfolgreich hinzugefügt!")
    print(f"- Datum: {datum}")
    print(f"- Lebensmittel: {lebensmittel}")
    print(f"- Menge: {menge} g")
    print(f"- Grund: {grund_text}\n")


def main():
    data = read_data()

    while True:
        welche_aufgabe = input(
            "\nWillkommen beim Food Waste Tracker\n"
            "Möchten Sie Daten auslesen (1), hinzufügen (2) oder das Programm beenden (3)? "
        ).strip()

        if welche_aufgabe == "1":
            _menu_auslesen(data)
        elif welche_aufgabe == "2":
            _menu_hinzufuegen(data)
        elif welche_aufgabe == "3":
            print("Programm wird beendet. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe! Bitte geben Sie '1', '2' oder '3' ein.\n")


if __name__ == "__main__":
    main()
