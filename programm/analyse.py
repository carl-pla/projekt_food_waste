from datetime import datetime


def _iter_rows(data):
    """Erlaubt sowohl Listen als auch Dicts als Eingabe."""
    if isinstance(data, dict): # wenn data ein dict ist, sonst wird Liste returnt
        return data.values()
    return data


def gesamte_verschwendung(data):
    """Berechnet die gesamte Menge an weggeworfenen Lebensmitteln in Gramm."""
    summe = 0.0

    for row in _iter_rows(data):
        try:
            summe += float(row["waste"])
        except (KeyError, TypeError, ValueError):
            # Kaputte/unkomplette Zeilen ignorieren
            continue

    return summe


def lebensmittel_meiste_verschwendung(data):
    """Gibt die drei Lebensmittel mit der größten weggeworfenen Menge zurück.

    Rückgabe: Liste von Tupeln [(lebensmittel, gesamt_waste), ...]
    """
    summen_pro_lebensmittel = {}

    for row in _iter_rows(data):
        try:
            name = row["lebensmittel"]
            waste = float(row["waste"])
        except (KeyError, TypeError, ValueError):
            continue

        if not name: # falls kein Lebensmittelname im Zeilendict vorhanden ist, wird Eintrag (Zeile der csv) geskippt (invalider Eintrag)
            continue

        summen_pro_lebensmittel[name] = (
            summen_pro_lebensmittel.get(name, 0.0) + waste # built-in: holt value des Keys name über dict.get(key, Nummer (falls dem key noch kein value zugeordnet wurde, wird geholter value zu Nummer)
        )

    return sorted(
        summen_pro_lebensmittel.items(), # Liste der Tupelobjekte der Form (key, value) werden sortiert
        key=lambda x: x[1], # Sortierung nach dem value der Tupel
        reverse=True, # größte values zuerst
    )[:3]


def zeitraum(eingabe_start, eingabe_ende, data):
    """Filtert alle Datensätze, die zwischen zwei Datumsangaben liegen.

    Rückgabe: Liste von Zeilen-Dicts.
    """
    start_datum = datetime.strptime(eingabe_start, "%Y-%m-%d").date()
    ende_datum = datetime.strptime(eingabe_ende, "%Y-%m-%d").date()

    ergebnis = []

    for row in _iter_rows(data):
        try:
            datum = datetime.strptime(row["datum"], "%Y-%m-%d").date()
        except (KeyError, TypeError, ValueError):
            continue

        if start_datum <= datum <= ende_datum:
            ergebnis.append(row)

    return ergebnis


def grund(data):
    """Ermittelt den häufigsten Grund (bei gleicher Häufigkeit mehrere Gründe) für das Wegwerfen.

    Rückgabe: Liste von Tupeln [(grund, anzahl), ...]
    """
    gruende = {}
    hoechste_frequenz = 0.0

    for row in _iter_rows(data):
        try:
            g = row["grund"]
        except (KeyError, TypeError):
            continue

        if not g:
            continue

        gruende[g] = gruende.get(g, 0) + 1

    sorted_list = sorted(
        gruende.items(),
        key=lambda x: x[1],
        reverse=True)

    haeufigster_grund_frequenz = sorted_list[0][1]

    haeufigste_gruende = []

    for g in sorted_list:
        if g[1] == haeufigster_grund_frequenz:
            haeufigste_gruende.append(g)

    return haeufigste_gruende
