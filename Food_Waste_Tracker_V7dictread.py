import datetime as dt
import csv

file_not_found_message = "Datei nicht gefunden. Sie müssen zuerst eine Liste anlegen oder die Datei in den Ordner des Programmes verschieben."

def get_input_options_and_functions():
    """
    Beinhaltet das Dictionary mit allen Eingabeoptionen und deren Funktion.

    Returns:
        Dictionary mit allen Eingabeoptionen und der jeweiligen Funktion
    """
    return {
    "Eintrag": "Eintrag hinzufügen / neue Liste anlegen; Abfrage zu Datum, Lebensmittel, Menge und Grund für Entsorgung",
    "Liste": "Liste lesen; Ausgabe der Liste zum manuellen Nachlesen",
    "Menge": "Ausgabe der gesamten Menge weggeworfener Lebensmittel",
    "Top3": "Ausgabe der drei Lebensmittel mit größter weggeworfenen Menge",
    "Zeitraum": "Abfrage zu Zeitraum, Ausgabe der Menge weggeworfener Lebensmittel in bestimmtem Zeitraum",
    "Grund": "Ausgabe des häufigsten Grund für das Wegwerfen",
    "Beenden": "Beendet das Programm, speichert Einträge final in der CSV-Datei / einer neuen CSV-Datei"
    }

def add_indent_to_dict(input_options_and_functions_dict):
    """
    Erstellt eine Liste von strings, wobei jeder string aus der Eingabeoption, einem Abstand zum Pfeil,
    dem Pfeil selbst und der jeweiligen Funktion besteht.

    Args:
        input_options_and_functions_dict (dict): Enthält alle Eingabeoptionen als keys und deren Funktionen als values

    Returns:
        formatted_input_options_and_functions (list): Enthält strings, die je Eingabeoption, Abstand zum Pfeil,
        Pfeil selbst und Funktion der Eingabeoption enthalten
    """
    longest_key = ""
    for option in input_options_and_functions_dict.keys():
        if len(option) > len(longest_key):
            longest_key = option

    formatted_input_options_and_functions = []

    for inp, func in input_options_and_functions_dict.items():
        individual_space_before_arrow = (len(longest_key) + 2 - len(inp)) * " "
        formatted_input_options_and_functions.append(f"{inp}{individual_space_before_arrow}-> {func}")

    return formatted_input_options_and_functions

def read_csv():
    """
    Versucht, die bestehende CSV-Datei "food_waste_list.csv" per DictReader zu lesen.

    Returns:
        fwl_dict (dict): Rückgabe bei bereits vorhandener CSV-Datei. Enthält alle Zeilen als Dictionaries.
        Key der Zeile ist eine laufende Nummer (Start bei 1), die values sind weitere Dictionaries, dessen keys
        "Datum", "Lebensmittel", (Wegwerf)"Menge" und (Wegwerf)"Grund" heißen
        None (None): Rückgabe bei keiner bisher vorhandenen CSV-Datei.
    """
    fwl_dict = {}
    try:
        with open("food_waste_list.csv", "r", newline="",encoding='utf-8') as fwl:
            fwl_dictreader = csv.DictReader(fwl, delimiter=",")
            key = 1
            for row in fwl_dictreader:
                fwl_dict[key] = row
                key += 1
        return fwl_dict
    except FileNotFoundError:
        return None

def check_option_valid(input_dict, user_task_raw):
    """
    Überprüft, ob die Eingabe des Users einer der möglichen Eingabeoptionen (Aufgaben) entspricht.

    Args:
        input_dict (dict): Enthält als keys die möglichen Eingabeoptionen
        user_task_raw (str): Enthält rohe Eingabe des Users

    Returns:
        user_message (str): Nachricht an den User, die nur ausgegeben wird, wenn er eine invalide Option eingegeben hat
        opt_valid (bool): Aussage, ob die User-Eingabe valide ist
        user_task (str): Verifizierte User-Aufgabe in Großbuchstaben, die weiterverarbeitet werden kann
    """
    user_message = f'Die Option "{user_task_raw}" wurde nicht gefunden. Bitte versuchen Sie es erneut.'
    opt_valid = False

    user_task = user_task_raw.upper()
    input_dict_key_list = [option.upper() for option in input_dict.keys()]
    if user_task in input_dict_key_list:
        opt_valid = True
    return user_message, opt_valid, user_task

def check_date_valid(raw_date):
    """
    Überprüft, ob die Datum-Eingabe des Users valide (möglich) ist.

    Args:
        raw_date (str): Vom User eingegebenes Datum

    Returns:
        user_message (str): Nachricht an den User, die ausgegeben wird, wenn er ein invalides Datum eingegeben hat
        opt_valid (bool): Aussage, ob das gegebene User-Datum valide ist
        formatted_date (dt.date | str): Verifiziertes Datum (als datetime-Objekt) oder leerer String, wenn Datum invalide ist
    """
    user_message = "Unmögliches Datum oder falsches Format. Bitte versuchen Sie es erneut."
    date_valid = False
    formatted_date = ""

    try:
        formatted_date = dt.datetime.strptime(raw_date, "%d.%m.%Y").date()
        date_valid = True
    except ValueError:
        pass
    return user_message, date_valid, formatted_date

def check_amount_valid(raw_amount):
    """
    Überprüft, ob die Mengeneingabe des Users valide (möglich/sinnhaft) ist.

    Args:
        raw_amount (str): Vom User eingegebene Menge

    Returns:
        amount_valid (bool): Aussage, ob die vom User gegebene Menge valide ist
        amount_tested (int | float): 0 oder verifizierte Wegwerfmenge
    """
    amount_tested = 0
    amount_valid = False

    try:
        amount_tested = float(raw_amount)
        if amount_tested <= 0:
            print("Die weggeworfene Menge kann nicht kleiner oder gleich 0 Gramm sein.\n")
        else:
            amount_valid = True
    except ValueError:
        print("Das ist keine gültige Menge. Bitte versuchen Sie es erneut.\n")

    return amount_valid, amount_tested

def add_entry_to_temporary_dict(fwl_dict, formatted_date, food_name, amount_tested, reason):
    """
    Fügt einem temporären Dictionary, das erst nach Beenden des Programms über die Eingabe "Beenden" in die CSV-Datei
    geschrieben wird, einen Eintrag hinzu.

    Args:
        fwl_dict (dict | None): Enthält alle Einträge aus der CSV-Datei und alle im Zwischenspeicher eingelagerten
        neuen Einträge oder ist None, falls noch keine CSV-Datei existiert und kein Eintrag bisher hinzugefügt wurde
        formatted_date (dt.date): Verifiziertes Datum des Users
        food_name (str): Lebensmitteleingabe des Users
        amount_tested (float): Verifizierte Wegwerfmenge
        reason (str): Eingabe des Users für Wegwerfgrund

    Returns:
        fwl_dict (dict): Aktualisiertes Dictionary, das nun auch oder nur den neuen Eintrag beinhaltet
    """
    entry = {"Datum": str(formatted_date),
             "Lebensmittel": food_name,
             "Menge": str(amount_tested),
             "Grund": reason}

    if fwl_dict is None:
        fwl_dict = {}
        entry_number = 1
        fwl_dict[entry_number] = entry
    else:
        entry_number = len(fwl_dict) + 1
        fwl_dict[entry_number] = entry
    return fwl_dict

def get_full_list_str(fwl_dict):
    """
    Erstellt einen großen String, der die gesamte bisherige Food Waste List samt neuer Einträge aus dem Zwischenspeicher
    enthält.

    Args:
        fwl_dict (dict): Enthält alle Einträge aus der CSV-Datei und dem Zwischenspeicher

    Returns:
        whole_list (str): Langer string, der alle Einträge aus CSV-Datei und Zwischenspeicher enthält
        file_not_found_message (str): Nachricht an den User, wenn die Food Waste List noch keine Einträge enthält
    """
    printed_list_str = ""

    if fwl_dict is not None:
        number_of_entries = len(fwl_dict)

        for row_index in range(1,number_of_entries+1):
            entry = fwl_dict[row_index]
            printed_list_str += (entry['Datum']+","+
                                 entry['Lebensmittel']+","+
                                 str(entry['Menge'])+","+
                                 entry['Grund']+"\n")

        table_head = "\nDatum,Lebensmittel,Menge,Grund\n"
        whole_list = table_head + printed_list_str
        return whole_list
    else:
        return file_not_found_message

def get_total_amount(fwl_dict):
    """
    Addiert die Wegwerfmenge aller Einträge aus CSV-Datei und Zwischenspeicher.

    Args:
        fwl_dict (dict): Enthält alle Einträge aus der CSV-Datei und dem Zwischenspeicher

    Returns:
        total_amount (float | int): Gesamte Wegwerfmenge oder 0, wenn keine Einträge vorhanden sind
        file_found (bool): Aussage, ob Einträge vorhanden sind
    """
    total_amount = 0
    if fwl_dict is None:
        file_found = False

    else:
        file_found = True
        number_of_entries = len(fwl_dict)
        for row_index in range(1,number_of_entries+1):
            entry = fwl_dict[row_index]
            total_amount += float(entry["Menge"])

    return total_amount, file_found

def get_top3(fwl_dict):
    """
    Holt die drei Lebensmittel mit der größten weggeworfenen Menge.

    Args:
        fwl_dict (dict): Enthält alle Einträge aus der CSV-Datei und dem Zwischenspeicher

    Returns:
        top_3_list (list): Enthält drei Tupel mit den drei Lebensmitteln mit der größten Wegwerfmenge und der genauen
        Menge, Form (Lebensmittel, Menge), Liste ist nach absteigender Menge sortiert. Sollte das gegebene fwl_dict
        keine drei unterschiedlichen Lebensmittel enthalten, enthält die Liste so viele Tupel wie es unterschiedliche
        Lebensmittel gibt (kann auch 0 sein, dann wäre es eine leere Liste)
        file_found (bool): Aussage, ob überhaupt Einträge vorhanden sind
    """
    no_doubles_dict = {}
    top_3_list = []
    file_found = False

    if fwl_dict is not None:
        all_entry_list = [(entry["Lebensmittel"], float(entry["Menge"])) for entry in fwl_dict.values()]
        for food_name, food_amount in all_entry_list:
            try:
                no_doubles_dict[food_name] +=  food_amount
            except KeyError:
                no_doubles_dict[food_name] = food_amount

        no_doubles_list = list(no_doubles_dict.items())
        # erzeugt Liste aus Tupeln mit je dem Lebensmittelnamen und der zugehörigen Menge

        sorted_no_doubles_list = sorted(no_doubles_list, key=lambda item: item[1], reverse=True)
        # True: Liste absteigend sortiert, lambda item: item[1]: danach wird sortiert (float mit der Menge)

        top_3_list = sorted_no_doubles_list[:3:]
        # nur erste 3 Elemente der Liste interessieren uns
        file_found = True

    return top_3_list, file_found

def output_top3(top_3_list):
    """
    Holt die drei Lebensmittel mit der größten weggeworfenen Menge.

    Args:
        top_3_list (list): Enthält drei Tupel mit den drei Lebensmitteln mit der größten Wegwerfmenge und der genauen
        Menge, Form (Lebensmittel, Menge), Liste ist nach absteigender Menge sortiert. Möglicherweise enthält diese
        Liste auch weniger als drei Tupel (auch leere Liste möglich)

    Returns:
        top_3_str (str): Enthält entweder die drei Lebensmittel mit der größten Wegwerfmenge und ihrer genauen Platzierung
        oder den Hinweis, dass nicht genug verschiedene Lebensmittel für eine Top 3-Ausgabe vorhanden sind
    """
    output_head = f"\nTop 3 weggeworfene Lebensmittel:\n"
    output_list = ""

    try:
        for place in range(3):
            top3tuple = top_3_list[place]
            output_list  += f"{place+1}. Platz: {top3tuple[0]} mit {top3tuple[1]} g bzw. {top3tuple[1] / 1000} kg\n"
        top_3_str = output_head + output_list
    except IndexError:
        top_3_str = "Es gibt nicht genug verschiedene Lebensmittel (weniger als 3), um die Top 3 weggeworfenen Lebensmittel zu bestimmen."
    return top_3_str

def timeframe_amount(formatted_start_date, formatted_end_date, fwl_dict):
    """
    Findet die Wegwerfmenge innerhalb eines angegebenen Zeitraums.

    Args:
        fwl_dict (dict): Enthält alle Einträge aus der CSV-Datei und dem Zwischenspeicher
        formatted_start_date (dt.date): Bereits verifiziertes (gültiges) Startdatum des Zeitraums
        formatted_end_date (dt.date): Bereits verifiziertes (gültiges) Enddatum des Zeitraums

    Returns:
        summed_amount (int | float): 0, wenn im gegebenen Zeitraum nichts weggeworfen wurde, sonst weggeworfene Menge im Zeitraum
        file_found (bool): Aussage, ob überhaupt Einträge vorhanden sind
    """
    summed_amount = 0
    file_found = False

    if fwl_dict is not None:
        for entry in fwl_dict.values():
            if formatted_start_date <= dt.datetime.strptime(entry["Datum"], "%Y-%m-%d").date() <= formatted_end_date:
                summed_amount += float(entry["Menge"])
        file_found = True

    return summed_amount, file_found

def get_most_frequent_reason(fwl_dict):
    """
    Findet den/die Gründe, wegen dem/denen Lebensmittel am häufigsten weggeworfen wurden.

    Args:
        fwl_dict (dict): Enthält alle Einträge aus der CSV-Datei und dem Zwischenspeicher

    Returns:
        highest_frequency (int): Anzahl, wie oft der häufigste Wegwerfgrund vorkommt oder 0, wenn es keine Einträge gibt
        reasons_with_highest_frequency (list): Enthält den Wegwerfgrund, der am häufigsten vorkommt. Wenn mehrere Gründe
        die höchste Wegwerfanzahl teilen, sind alle diese Gründe Teil der Liste
        file_found (bool): Aussage, ob überhaupt Einträge vorhanden sind
        """
    reasons_and_numbers_dict = {}
    highest_frequency = 0
    reasons_with_highest_frequency = []
    file_found = False

    if fwl_dict is not None:
        all_reasons_list = [entry["Grund"] for entry in fwl_dict.values()]
        for reason in all_reasons_list:
            try:
                reasons_and_numbers_dict[reason] += 1
            except KeyError:
                reasons_and_numbers_dict[reason] = 1
        highest_frequency = 0
        for reason_count in reasons_and_numbers_dict.values():
            if reason_count > highest_frequency:
                highest_frequency = reason_count
        reasons_with_highest_frequency = []
        for reason, frequency in reasons_and_numbers_dict.items():
            if frequency == highest_frequency:
                reasons_with_highest_frequency.append(reason)
        file_found = True
    return highest_frequency, reasons_with_highest_frequency, file_found

def output_most_frequent_reasons(highest_frequency, list_most_frequent_reasons):
    """
    Erstellt eine Nachricht für den User, sodass dieser lesen kann, weswegen Lebensmittel am häufigsten weggeworfen wurden.

    Args:
        highest_frequency (int): Anzahl, wie oft der häufigste Wegwerfgrund vorkommt
        list_most_frequent_reasons (list): Enthält den Wegwerfgrund, der am häufigsten vorkommt. Wenn mehrere Gründe
        die höchste Wegwerfanzahl teilen, sind alle diese Gründe Teil der Liste

    Returns:
        concatenated_output (str): Nachricht an den User, die alle häufigsten Gründe und ihre Vorkommenszahl enthält
    """
    safe_return = f"\n'{list_most_frequent_reasons[0]}' ist mit {highest_frequency} mal der häufigste Grund für das Wegwerfen."
    concatenated_output = safe_return

    if len(list_most_frequent_reasons) > 1:
        other_reasons_names = [item for item in list_most_frequent_reasons[1:]]
        concatenated_other_reasons = "\nWeitere Gründe mit der selben Häufigkeit:"

        for other_reason in other_reasons_names:
            concatenated_other_reasons += f"\n- '{other_reason}'"
        concatenated_output += concatenated_other_reasons

    return concatenated_output

def final_write_fwl(fwl_dict, entry_available, original_fwl_dict):
    """
    Schreibt die temporären Einträge und die vorher bereits in der CSV-Datei enthaltenen Einträge (falls es solche gibt)
    in die CSV-Datei. Somit sind die neuen Einträge gespeichert.

    Args:
        fwl_dict (dict): Enthält alle Einträge aus der CSV-Datei und dem Zwischenspeicher
        entry_available (bool): Aussage, ob ein neuer Eintrag hinzugefügt wurde
        original_fwl_dict (None | dict): None, falls noch keine "food_waste_list.csv" existiert oder dict mit
        CSV-Einträgen ohne zwischengespeicherte Einträge

    Returns:
        fwl_dict (dict): Beinhaltet alle Einträge aus der ursprünglichen CSV-Datei und dem Zwischenspeicher
        None (None): Wird zurückgegeben, wenn kein Eintrag hinzugefügt wurde (nur Nutzung von Analysefunktionen oder
        Beendung des Programms, ohne eine Liste zu erstellen)
    """
    if entry_available:
        with open ("food_waste_list.csv", "w", newline="", encoding="utf-8") as fwl:
            table_head = ["Datum","Lebensmittel","Menge","Grund"]
            fwl_writer = csv.DictWriter(fwl, fieldnames=table_head)

            fwl_writer.writeheader()
            for row in fwl_dict.values():
                fwl_writer.writerow(row)

        if original_fwl_dict is None:
            pretext = '\nKeine Liste vorhanden. Neue Liste mit folgenden Einträgen erstellt:\n'
            added_entries = [f"{entry["Datum"]},{entry["Lebensmittel"]},{entry["Menge"]},{entry["Grund"]}" for entry in fwl_dict.values()]
        else:
            pretext = '\nEinträge hinzugefügt:\n'
            original_keys = list(original_fwl_dict.keys())
            fwl_keys = list(fwl_dict.keys())
            new_keys = [key for key in fwl_keys if key not in original_keys]
            added_entries = []
            for key in new_keys:
                entry = fwl_dict[key]
                added_entries.append(f"{entry["Datum"]},{entry["Lebensmittel"]},{entry["Menge"]},{entry["Grund"]}")

        new_entries_str = ""
        for added_entry_str in added_entries:
            new_entries_str += f"{added_entry_str}\n"
        print(pretext + new_entries_str)
        return fwl_dict

    else:
        return None

def main():
    print("ACHTUNG:\n"
          "Bitte stellen Sie vor dem Fortfahren sicher, dass keine Datei 'food_waste_list.csv' bereits im Ordner des Programmes vorhanden ist,\n"
          "es sei denn, diese ist bereits von diesem Programm erstellt worden.\n")

    print("Eingabemöglichkeiten:\n")

    input_options_and_functions_dict = get_input_options_and_functions()
    formatted_input_options_and_functions = add_indent_to_dict(input_options_and_functions_dict)
    for option_and_func in formatted_input_options_and_functions:
        print(option_and_func)

    original_fwl_dict = read_csv()
    fwl_dict = read_csv()
    entry_available = False

    while True:

        user_task_raw = input("\nWas möchten Sie tun / wissen? ").strip()
        error_message, opt_valid, user_task  = check_option_valid(input_options_and_functions_dict, user_task_raw)
        if not opt_valid:
            print(error_message)

        if user_task == "EINTRAG":
            while True:
                raw_date = input("Wegwerfdatum (Format: DD.MM.YYYY): ").strip()
                user_message, date_valid, formatted_date = check_date_valid(raw_date)
                if date_valid:
                    break
                else:
                    print(user_message)

            # Groß- und Kleinschreibung wird berücksichtigt
            food_name_raw = input("Weggeworfenes Lebensmittel: ").strip()
            food_name = food_name_raw

            while True:
                raw_amount = input("Weggeworfene Menge in Gramm: ").strip()
                amount_valid, amount_tested = check_amount_valid(raw_amount)
                if amount_valid:
                    break

            raw_reason = input("Grund für Entsorgung: ").strip()
            reason = raw_reason

            fwl_dict = add_entry_to_temporary_dict(fwl_dict, formatted_date, food_name, amount_tested, reason)
            entry_available = True
            print(f"\nEintrag '{formatted_date},{food_name},{amount_tested},{reason}' in Zwischenspeicher aufgenommen.\n"
                  f"Hinzufügen zur Liste erfolgt nach dem Beenden des Programms. "
                  f"Alle Analysefunktionen berücksichtigen bereits den neuen Eintrag.")

        elif user_task == "LISTE":
            print(get_full_list_str(fwl_dict))

        elif user_task == "MENGE":
            total_amount, file_found = get_total_amount(fwl_dict)
            if file_found:
                print(f"Die gesamte weggeworfene Lebensmittelmenge beträgt {total_amount} g bzw. {total_amount/1000} kg.")
            else:
                print(file_not_found_message)

        elif user_task == "TOP3":
            top3_list, file_found = get_top3(fwl_dict)
            if file_found:
                print(output_top3(top3_list))
            else:
                print(file_not_found_message)

        elif user_task == "ZEITRAUM":
            if fwl_dict is not None:
                while True:
                    start_date = input("Zeitraumstart (Format: DD.MM.YYYY): ")
                    user_message, date_valid, formatted_start_date = check_date_valid(start_date)
                    if date_valid:
                        break
                    else:
                        print(user_message)

                while True:
                    end_date = input("Zeitraumende (Format: DD.MM.YYYY): ")
                    user_message, date_valid, formatted_end_date = check_date_valid(end_date)
                    if date_valid:
                        break
                    else:
                        print(user_message)

                amount_in_timeframe, file_found = timeframe_amount(formatted_start_date, formatted_end_date, fwl_dict)
                print(f"Die weggeworfene Menge von {start_date} bis {end_date} beträgt {amount_in_timeframe} g.")
            else:
                print(file_not_found_message)

        elif user_task == "GRUND":
            highest_frequency, list_most_frequent_reasons, file_found = get_most_frequent_reason(fwl_dict)
            if file_found:
                print(output_most_frequent_reasons(highest_frequency, list_most_frequent_reasons))
            else:
                print(file_not_found_message)

        elif user_task == "BEENDEN":
            break

    final_write_fwl(fwl_dict, entry_available, original_fwl_dict)

    print("\nProgramm beendet.")

if __name__ == "__main__":
    main()