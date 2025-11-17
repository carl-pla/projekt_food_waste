import datetime as dt
import csv

beenden_message = "\nProgramm beendet."
file_not_found_message = "Datei nicht gefunden. Sie müssen zuerst eine Liste anlegen oder die Datei in den Ordner des Programmes verschieben."

def check_amount_valid(raw_amount):
    try:
        amount_tested = int(raw_amount)
        if amount_tested <= 0:
            print("Die weggeworfene Menge kann nicht kleiner oder gleich 0 Gramm sein.")
            return False, 0
        else:
            return True, amount_tested
    except ValueError:
        print("Das ist keine ganze Zahl. Bitte versuchen Sie es erneut.")
        return False, 0

def output_most_frequent_reasons(list_most_frequent_reasons):

    safe_return = f"\n'{list_most_frequent_reasons[0][0]}' ist mit {list_most_frequent_reasons[0][1]} mal der häufigste Grund für das Wegwerfen."

    if len(list_most_frequent_reasons) == 1:
        return safe_return
    else:
        other_reasons_names = [item[0] for item in list_most_frequent_reasons[1:]]
        concatenated_other_reasons = ""
        for index_other_reason in range(len(other_reasons_names)):
            concatenated_other_reasons += f"- '\n{other_reasons_names[index_other_reason]}'"

        return safe_return + "\nWeitere Gründe mit der selben Häufigkeit:" + concatenated_other_reasons

def output_top3(top3_list):
    output_list = [f"\nTop 3 weggeworfene Lebensmittel:\n"]
    try:
        for place in range(3):
            output_list.append(f"1. Platz: {top3_list[place][0]} mit {top3_list[place][1]} g bzw. {top3_list[place][1] / 1000} kg\n")
        return output_list[0]+output_list[1]+output_list[2]+output_list[3]
    except IndexError:
        return "Es gibt nicht genug Einträge (weniger als 3), um die Top 3 weggeworfenen Lebensmittel zu bestimmen."

def display_main_menu():
    """
    Gibt das Menü des Programms aus. Es beinhaltet: Einen Warnhinweis und die mit Fluchtlinie versehenen Eingabeoptionen.
    """
    attention_message = get_attention_message()

    input_options = get_input_options()

    # fügt "Fluchtlinie" bei Ausgabe ein
    formatted_input_options = []
    for inp, func in input_options.items():
        individual_space_before_arrow = (len(find_longest_key_in_dict(input_options)) + 2 - len(inp)) * " "
        formatted_input_options.append(f"{inp}{individual_space_before_arrow}-> {func}")

    return attention_message, "Eingabemöglichkeiten:\n", formatted_input_options

def check_date_validity(date):
    try:
        formatted_date = dt.datetime.strptime(date, "%d.%m.%Y").date()
        return "", True, formatted_date
    except ValueError:
        return "Unmögliches Datum oder falsches Format. Bitte versuchen Sie es erneut.", False, ""

def get_input_options():
    return {
    "Eintrag": "Eintrag hinzufügen / neue Liste anlegen; Abfrage zu Datum, Lebensmittel, Menge und Grund für Entsorgung,",
    "Liste": "Liste lesen; Ausgabe der Liste zum manuellen Nachlesen",
    "Menge": "Ausgabe der gesamten Menge weggeworfener Lebensmittel",
    "Top3": "Ausgabe der drei Lebensmittel mit größter weggeworfenen Menge",
    "Zeitraum": "Abfrage zu Zeitraum, Ausgabe der Menge weggeworfener Lebensmittel in bestimmtem Zeitraum",
    "Grund": "Ausgabe des häufigsten Grund für das Wegwerfen",
    "Beenden": "Beendet das Programm"
    }

def get_attention_message():
    return ("ACHTUNG:\n"
            "Bitte stellen Sie vor dem Fortfahren sicher, dass keine Datei 'food_waste_list.csv' bereits im Ordner des Programmes vorhanden ist,\n"
            "es sei denn, diese ist bereits von diesem Programm erstellt worden.\n")

def get_most_frequent_reason():
    reasons_number_dict = {}
    try:
        with open('food_waste_list.csv', "r") as fwl:
            fwl_reader = csv.reader(fwl)
            next(fwl_reader) # überspringt Kopfzeile der Tabelle
            all_reason_list = [row[3] for row in fwl_reader if len(row) == 4]
            for reason in all_reason_list:
                if reason in reasons_number_dict:
                    reasons_number_dict[reason] += 1
                else:
                    reasons_number_dict[reason] = 1
            highest_frequency = 0
            for reason_count in reasons_number_dict.values():
                if reason_count > highest_frequency:
                    highest_frequency = reason_count
            reasons_with_highest_frequency = []
            for reason, frequency in reasons_number_dict.items():
                if frequency == highest_frequency:
                    reasons_with_highest_frequency.append((reason, frequency))
            return reasons_with_highest_frequency, True
    except FileNotFoundError:
        return [], False

def timeframe_amount(formatted_start_date, formatted_end_date):
    try:
        with open('food_waste_list.csv', "r") as fwl:
            fwl_reader = csv.reader(fwl)
            next(fwl_reader)
            summed_amount = 0
            for row in fwl_reader:
                if len(row) == 4 and formatted_start_date <= dt.datetime.strptime(row[0], "%Y-%m-%d").date() <= formatted_end_date:
                    summed_amount = summed_amount + int(row[2])
            return summed_amount, True
    except FileNotFoundError:
        return 0, False

def get_top3():
    no_doubles_dict = {}
    try:
        with open('food_waste_list.csv', "r") as fwl:
            fwl_reader = csv.reader(fwl)
            next(fwl_reader)
            all_entry_list = [(entry[1], int(entry[2])) for entry in fwl_reader if len(entry) == 4]
            for food_name, food_amount in all_entry_list:
                try:
                    no_doubles_dict[food_name] +=  food_amount
                except KeyError:
                    no_doubles_dict[food_name] = food_amount
            no_doubles_list = list(no_doubles_dict.items())
            sorted_no_doubles_list = sorted(no_doubles_list, key=lambda item: item[1], reverse=True)
            # True: Liste absteigend sortiert, lambda item: item[1]: Anonyme Funktion, die item[1] returnt (unseren int)
            top_3_list = sorted_no_doubles_list[:3:]
            return top_3_list, True
    except FileNotFoundError:
        return [], False

def get_total_amount():
    try:
        with open('food_waste_list.csv', "r") as fwl:
            fwl_reader = csv.reader(fwl)
            next(fwl_reader)  # erste Zeile der CSV-Datei wird übersprungen
            total_amount = 0
            for entry in fwl_reader:
                if len(entry) == 4:
                    total_amount = total_amount + int(entry[2])
            return total_amount, True
    except FileNotFoundError:
        return 0, False

# Problem mit read_full_list(): Leerzeile zwischen einzelnen Einträgen
def read_full_list():
    try:
        with open('food_waste_list.csv', "r") as fwl:
            entry_list = fwl.read()
            return entry_list, True
    except FileNotFoundError:
        return [], False

def find_longest_key_in_dict(input_dict):
    longest_key = ""
    for option in input_dict.keys():
        if len(option) > len(longest_key):
            longest_key = option
    return longest_key

def option_valid(user_task, input_dict, user_task_raw):
    input_dict_key_list = [option.upper() for option in input_dict.keys()]
    if user_task in input_dict_key_list:
        return "", True
    return f'Die Option "{user_task_raw}" wurde nicht gefunden. Bitte versuchen Sie es erneut.', False

def add_entry(entry):
    try:
        _ = open('food_waste_list.csv', "r")
        _.close()
        with open("food_waste_list.csv", "a", newline="") as fwl:
            fwl_writer = csv.writer(fwl)
            fwl_writer.writerow(entry)
            return f'\nEintrag hinzugefügt:\n{entry[0]},{entry[1]},{entry[2]},{entry[3]}'
    except FileNotFoundError:
        with open("food_waste_list.csv", "w", newline="") as fwl:
            fwl_writer = csv.writer(fwl)
            head = ["Datum", "Lebensmittel", "Menge", "Grund"]
            fwl_writer.writerow(head)
            fwl_writer.writerow(entry)
        return f'\nKeine Liste vorhanden.\nNeue Liste mit Eintrag "{entry[0]},{entry[1]},{entry[2]},{entry[3]}" erstellt.'

def main():
    attention_message, headline, input_options_and_funcs = display_main_menu()
    print(attention_message)
    print(headline)
    for option_and_func in input_options_and_funcs:
        print(option_and_func)

    input_options_dict = get_input_options()

    while True:
        user_task_raw = input("\nWas möchten Sie tun / wissen? ")
        user_task = user_task_raw.upper()
        error_message, opt_valid  = option_valid(user_task, input_options_dict, user_task_raw)
        if opt_valid:
            pass
        else:
            print(error_message)

        # hier stehen geblieben, verbleibend: Bündeln von Funktionen (falls es überhaupt noch geht), doc-strings, Testprogramm
        if user_task == "EINTRAG":
            while True:
                raw_date = input("Wegwerfdatum (Format: DD.MM.YYYY): ")
                user_message, date_valid, formatted_date = check_date_validity(raw_date)
                if date_valid:
                    break
                else:
                    print(user_message)

            food_name_raw = input("Weggeworfenes Lebensmittel: ")
            food_name = food_name_raw

            while True:
                raw_amount = input("Weggeworfene Menge in Gramm (keine Kommazahlen): ")
                amount_valid, amount_tested = check_amount_valid(raw_amount)
                if amount_valid:
                    break

            raw_reason = input("Grund für Entsorgung: ")
            reason = raw_reason

            entry = [formatted_date, food_name, amount_tested, reason]
            added_entry = add_entry(entry)
            print(added_entry)

        elif user_task == "LISTE":
            full_list, file_found = read_full_list()
            if file_found:
                print(full_list)
            else:
                print(file_not_found_message)

        elif user_task == "MENGE":
            total_amount, file_found = get_total_amount()
            if file_found:
                print(f"Die gesamte weggeworfene Lebensmittelmenge beträgt {total_amount} g bzw. {total_amount/1000} kg.")
            else:
                print(file_not_found_message)

        elif user_task == "TOP3":
            top3_list, file_found = get_top3()
            if file_found:
                print(output_top3(top3_list))
            else:
                print(file_not_found_message)

        elif user_task == "ZEITRAUM":
            full_list, file_found = read_full_list()
            if file_found:
                while True:
                    start_date = input("Zeitraumstart (Format: DD.MM.YYYY): ")
                    user_message, date_valid, formatted_start_date = check_date_validity(start_date)
                    if date_valid:
                        break
                    else:
                        print(user_message)

                while True:
                    end_date = input("Zeitraumende (Format: DD.MM.YYYY): ")
                    user_message, date_valid, formatted_end_date = check_date_validity(end_date)
                    if date_valid:
                        break
                    else:
                        print(user_message)

                amount_in_timeframe, file_found = timeframe_amount(formatted_start_date, formatted_end_date)
                print(f"Die weggeworfene Menge von {start_date} bis {end_date} beträgt {amount_in_timeframe} g.")
            else:
                print(file_not_found_message)

        elif user_task == "GRUND":
            list_most_frequent_reasons, file_found = get_most_frequent_reason()
            if file_found:
                print(output_most_frequent_reasons(list_most_frequent_reasons))
            else:
                print(file_not_found_message)

        elif user_task == "BEENDEN":
            print(beenden_message)
            break

if __name__ == "__main__":
    main()