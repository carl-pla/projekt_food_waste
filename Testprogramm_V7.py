import datetime as dt
import Food_Waste_Tracker_V7dictread as V7

input_dict = {
        "Eintrag": "Eintrag hinzufügen / neue Liste anlegen; Abfrage zu Datum, Lebensmittel, Menge und Grund für Entsorgung",
        "Liste": "Liste lesen; Ausgabe der Liste zum manuellen Nachlesen",
        "Menge": "Ausgabe der gesamten Menge weggeworfener Lebensmittel",
        "Top3": "Ausgabe der drei Lebensmittel mit größter weggeworfenen Menge",
        "Zeitraum": "Abfrage zu Zeitraum, Ausgabe der Menge weggeworfener Lebensmittel in bestimmtem Zeitraum",
        "Grund": "Ausgabe des häufigsten Grund für das Wegwerfen",
        "Beenden": "Beendet das Programm, speichert Einträge final in der CSV-Datei / einer neuen CSV-Datei"
    }

def TEST_get_input_options_and_functions():
    print("\nTEST: get_input_options_and_functions")
    expected = {
        "Eintrag": "Eintrag hinzufügen / neue Liste anlegen; Abfrage zu Datum, Lebensmittel, Menge und Grund für Entsorgung",
        "Liste": "Liste lesen; Ausgabe der Liste zum manuellen Nachlesen",
        "Menge": "Ausgabe der gesamten Menge weggeworfener Lebensmittel",
        "Top3": "Ausgabe der drei Lebensmittel mit größter weggeworfenen Menge",
        "Zeitraum": "Abfrage zu Zeitraum, Ausgabe der Menge weggeworfener Lebensmittel in bestimmtem Zeitraum",
        "Grund": "Ausgabe des häufigsten Grund für das Wegwerfen",
        "Beenden": "Beendet das Programm, speichert Einträge final in der CSV-Datei / einer neuen CSV-Datei"
    }
    got = V7.get_input_options_and_functions()
    if got == expected:
        print("Bestanden")
    else:
        print(f"Abweichung!\nErwartet: {expected}\nBekommen: {got}")

def TEST_add_indent_to_dict():
    print("\nTEST: add_indent_to_dict")
    expected = [
        "Eintrag   -> Eintrag hinzufügen / neue Liste anlegen; Abfrage zu Datum, Lebensmittel, Menge und Grund für Entsorgung",
        "Liste     -> Liste lesen; Ausgabe der Liste zum manuellen Nachlesen",
        "Menge     -> Ausgabe der gesamten Menge weggeworfener Lebensmittel",
        "Top3      -> Ausgabe der drei Lebensmittel mit größter weggeworfenen Menge",
        "Zeitraum  -> Abfrage zu Zeitraum, Ausgabe der Menge weggeworfener Lebensmittel in bestimmtem Zeitraum",
        "Grund     -> Ausgabe des häufigsten Grund für das Wegwerfen",
        "Beenden   -> Beendet das Programm, speichert Einträge final in der CSV-Datei / einer neuen CSV-Datei",
    ]

    got = V7.add_indent_to_dict(input_dict)
    if got == expected:
        print("Bestanden")
    else:
        print(f"Abweichung!\nErwartet: {expected}\nBekommen: {got}")

def TEST_read_csv():
    print("\nTEST: read_csv")
    expected = {
        1: {'Datum': '2024-08-31', 'Lebensmittel': 'Wurst', 'Menge': '3210', 'Grund': 'Reste vom Kochen'},
        2: {'Datum': '2024-07-23', 'Lebensmittel': 'Gurke', 'Menge': '1400', 'Grund': 'Transport beschädigt'},
        3: {'Datum': '2024-07-29', 'Lebensmittel': 'Kaffee', 'Menge': '2910', 'Grund': 'Reste vom Kochen'},
        4: {'Datum': '2024-05-31', 'Lebensmittel': 'Paprika', 'Menge': '750', 'Grund': 'falsche Lagerung'},
        5: {'Datum': '2024-10-09', 'Lebensmittel': 'Saft', 'Menge': '3380', 'Grund': 'Verpackung beschädigt'},
        6: {'Datum': '2024-02-23', 'Lebensmittel': 'Apfel', 'Menge': '1420', 'Grund': 'Überproduktion'},
        7: {'Datum': '2024-09-11', 'Lebensmittel': 'Eier', 'Menge': '4420', 'Grund': 'Reste vom Kochen'},
        8: {'Datum': '2024-01-12', 'Lebensmittel': 'Kartoffel', 'Menge': '4640', 'Grund': 'Reste vom Kochen'},
        9: {'Datum': '2024-09-19', 'Lebensmittel': 'Kartoffel', 'Menge': '2330', 'Grund': 'verdorben'},
        10: {'Datum': '2024-10-03', 'Lebensmittel': 'Mehl', 'Menge': '4280', 'Grund': 'Versehen'}}

    got = V7.read_csv()
    if got == expected:
        print("Bestanden")
    else:
        print(f"Abweichung!\nErwartet: {expected}\nBekommen: {got}")

def TEST_check_option_valid():
    print("\nTEST: check_option_valid")
    samples = {
        "Eintrag": ('Die Option "Eintrag" wurde nicht gefunden. Bitte versuchen Sie es erneut.', True, "EINTRAG"),
        "Beenden": ('Die Option "Beenden" wurde nicht gefunden. Bitte versuchen Sie es erneut.', True, "BEENDEN"),
        "something": ('Die Option "something" wurde nicht gefunden. Bitte versuchen Sie es erneut.', False, "SOMETHING")
    }

    expected = [value for value in samples.values()]
    got = []
    for test_argument in samples.keys():
        got.append(V7.check_option_valid(input_dict, test_argument))

    bestanden = True
    for index in range(3):
        if not expected[index] == got[index]:
            bestanden = False

    if bestanden:
        print("Bestanden")
    else:
        print(f"Abweichung!\nErwartet: {expected}\nBekommen: {got}")

def TEST_check_date_valid():
    print("\nTEST: check_date_valid")
    samples = {
        "31.08.2024": ("Unmögliches Datum oder falsches Format. Bitte versuchen Sie es erneut.", True, dt.date(2024, 8, 31)),
        "31.02.2024": ("Unmögliches Datum oder falsches Format. Bitte versuchen Sie es erneut.", False, ""),
        "abc": ("Unmögliches Datum oder falsches Format. Bitte versuchen Sie es erneut.", False, "")
    }
    expected = [value for value in samples.values()]
    got = []
    for test_argument in samples.keys():
        got.append(V7.check_date_valid(test_argument))

    bestanden = True
    for index in range(3):
        if not expected[index] == got[index]:
            bestanden = False

    if bestanden:
        print("Bestanden")
    else:
        print(f"Abweichung!\nErwartet: {expected}\nBekommen: {got}")

def TEST_check_amount_valid():
    print("\nTEST: check_amount_valid")
    samples = {
        "3210": (True, 3210.0),
        "0": (False, 0.0),
        "-10": (False, -10.0),
        "hallo": (False, 0)
    }

    expected = [value for value in samples.values()]
    got = []
    for test_argument in samples.keys():
        got.append(V7.check_amount_valid(test_argument))

    bestanden = True
    for index in range(4):
        if not expected[index] == got[index]:
            bestanden = False

    if bestanden:
        print("Bestanden")
    else:
        print(f"Abweichung!\nErwartet: {expected}\nBekommen: {got}")

def TEST_add_entry_to_temporary_dict():
    print("\nTEST: add_entry_to_temporary_dict")

    fwl_dict1 = None
    fwl_dict2 = {1: {"Datum": "2023-11-02","Lebensmittel": "Osterei","Menge": "50.0","Grund": "faulig"}}

    test1_bestanden = True
    got1 = V7.add_entry_to_temporary_dict(fwl_dict1, dt.date(2024, 12, 1), "Keks", 5.0, "Probe")
    expected1 = {1: {"Datum": "2024-12-01","Lebensmittel": "Keks","Menge": "5.0","Grund": "Probe"}}
    if got1 != expected1:
        test1_bestanden = False

    test2_bestanden = True
    got2 = V7.add_entry_to_temporary_dict(fwl_dict2, dt.date(2025, 10, 9), "Tomate", 500.0, "Schimmel")
    expected2 = {1: {"Datum": "2023-11-02","Lebensmittel": "Osterei","Menge": "50.0","Grund": "faulig"},
                 2: {"Datum": "2025-10-09","Lebensmittel": "Tomate","Menge": "500.0","Grund": "Schimmel"}}
    if got2 != expected2:
        test2_bestanden = False

    if test1_bestanden and test2_bestanden:
        print("Bestanden")
    elif test1_bestanden and not test2_bestanden:
        print("Abweichung! test2 fehlgeschlagen!")
    elif not test1_bestanden and test2_bestanden:
        print("Abweichung! test1 fehlgeschlagen!")
    else:
        print("Abweichung! test1 und test2 fehlgeschlagen!")

def TEST_get_full_list_str():
    print("\nTEST: get_full_list_str")

    fwl_dict1 = None
    fwl_dict2 = {1: {"Datum": "2023-11-02","Lebensmittel": "Osterei","Menge": "50.0","Grund": "faulig"},
                 2: {"Datum": "2025-10-09","Lebensmittel": "Tomate","Menge": "500.0","Grund": "Schimmel"}}

    test1_bestanden = True
    got1 = V7.get_full_list_str(fwl_dict1)
    expected1 = "Datei nicht gefunden. Sie müssen zuerst eine Liste anlegen oder die Datei in den Ordner des Programmes verschieben."
    if got1 != expected1:
        test1_bestanden = False

    test2_bestanden = True
    got2 = V7.get_full_list_str(fwl_dict2)
    expected2 = ("\nDatum,Lebensmittel,Menge,Grund\n"
                 "2023-11-02,Osterei,50.0,faulig\n"
                 "2025-10-09,Tomate,500.0,Schimmel\n")
    if got2 != expected2:
        test2_bestanden = False

    if test1_bestanden and test2_bestanden:
        print("Bestanden")
    elif test1_bestanden and not test2_bestanden:
        print("Abweichung! test2 fehlgeschlagen!")
    elif not test1_bestanden and test2_bestanden:
        print("Abweichung! test1 fehlgeschlagen!")
    else:
        print("Abweichung! test1 und test2 fehlgeschlagen!")

def TEST_get_total_amount():
    print("\nTEST: get_total_amount")

    fwl_dict1 = None
    fwl_dict2 = {
        1: {'Datum': '2024-08-31', 'Lebensmittel': 'Wurst', 'Menge': '3210', 'Grund': 'Reste vom Kochen'},
        2: {'Datum': '2024-07-23', 'Lebensmittel': 'Gurke', 'Menge': '1400', 'Grund': 'Transport beschädigt'},
        3: {'Datum': '2024-07-29', 'Lebensmittel': 'Kaffee', 'Menge': '2910', 'Grund': 'Reste vom Kochen'},
        4: {'Datum': '2024-05-31', 'Lebensmittel': 'Paprika', 'Menge': '750', 'Grund': 'falsche Lagerung'},
        5: {'Datum': '2024-10-09', 'Lebensmittel': 'Saft', 'Menge': '3380', 'Grund': 'Verpackung beschädigt'}
    }

    test1_bestanden = True
    got1 = V7.get_total_amount(fwl_dict1)
    expected1 = (0, False)
    if got1 != expected1:
        test1_bestanden = False

    test2_bestanden = True
    got2 = V7.get_total_amount(fwl_dict2)
    expected2 = 3210 + 1400 + 2910 + 750 + 3380, True
    if got2 != expected2:
        test2_bestanden = False

    if test1_bestanden and test2_bestanden:
        print("Bestanden")
    elif test1_bestanden and not test2_bestanden:
        print("Abweichung! test2 fehlgeschlagen!")
    elif not test1_bestanden and test2_bestanden:
        print("Abweichung! test1 fehlgeschlagen!")
    else:
        print("Abweichung! test1 und test2 fehlgeschlagen!")

def TEST_get_top3():
    print("\nTEST: get_top3")
    fwl_dict1 = None
    fwl_dict2 = {
        1: {'Datum': '2024-08-31', 'Lebensmittel': 'Wurst', 'Menge': '3210', 'Grund': 'Reste vom Kochen'},
        2: {'Datum': '2024-07-23', 'Lebensmittel': 'Gurke', 'Menge': '1400', 'Grund': 'Transport beschädigt'},
        3: {'Datum': '2024-07-29', 'Lebensmittel': 'Kaffee', 'Menge': '2910', 'Grund': 'Reste vom Kochen'},
        4: {'Datum': '2024-05-31', 'Lebensmittel': 'Paprika', 'Menge': '750', 'Grund': 'falsche Lagerung'},
        5: {'Datum': '2024-10-09', 'Lebensmittel': 'Saft', 'Menge': '3380', 'Grund': 'Verpackung beschädigt'},
        6: {'Datum': '2024-02-23', 'Lebensmittel': 'Apfel', 'Menge': '1420', 'Grund': 'Überproduktion'},
        7: {'Datum': '2024-09-11', 'Lebensmittel': 'Eier', 'Menge': '4420', 'Grund': 'Reste vom Kochen'},
        8: {'Datum': '2024-01-12', 'Lebensmittel': 'Kartoffel', 'Menge': '4640', 'Grund': 'Reste vom Kochen'},
        9: {'Datum': '2024-09-19', 'Lebensmittel': 'Kartoffel', 'Menge': '2330', 'Grund': 'verdorben'},
        10: {'Datum': '2024-10-03', 'Lebensmittel': 'Mehl', 'Menge': '4280', 'Grund': 'Versehen'}}

    test1_bestanden = True
    got1 = V7.get_top3(fwl_dict1)
    expected1 = ([], False)
    if got1 != expected1:
        test1_bestanden = False

    test2_bestanden = True
    got2 = V7.get_top3(fwl_dict2)
    expected2 = ([("Kartoffel", 6970.0), ("Eier", 4420.0), ("Mehl", 4280.0)], True)
    if got2 != expected2:
        test2_bestanden = False

    if test1_bestanden and test2_bestanden:
        print("Bestanden")
    elif test1_bestanden and not test2_bestanden:
        print("Abweichung! test2 fehlgeschlagen!")
    elif not test1_bestanden and test2_bestanden:
        print("Abweichung! test1 fehlgeschlagen!")
    else:
        print("Abweichung! test1 und test2 fehlgeschlagen!")

def TEST_output_top3():
    print("\nTEST: output_top3")

    top3_list = [("Kartoffel", 6970.0), ("Eier", 4420.0), ("Mehl", 4280.0)]
    incomplete_top3_list = [("Kartoffel", 6970.0), ("Eier", 4420.0)]

    test1_bestanden = True
    got1 = V7.output_top3(incomplete_top3_list)
    expected1 = "Es gibt nicht genug verschiedene Lebensmittel (weniger als 3), um die Top 3 weggeworfenen Lebensmittel zu bestimmen."
    if got1 != expected1:
        test1_bestanden = False

    test2_bestanden = True
    got2 = V7.output_top3(top3_list)
    expected2 = (f"\nTop 3 weggeworfene Lebensmittel:\n"
                 f"1. Platz: Kartoffel mit 6970.0 g bzw. 6.97 kg\n"
                 f"2. Platz: Eier mit 4420.0 g bzw. 4.42 kg\n"
                 f"3. Platz: Mehl mit 4280.0 g bzw. 4.28 kg\n")
    if got2 != expected2:
        test2_bestanden = False

    if test1_bestanden and test2_bestanden:
        print("Bestanden")
    elif test1_bestanden and not test2_bestanden:
        print("Abweichung! test2 fehlgeschlagen!")
    elif not test1_bestanden and test2_bestanden:
        print("Abweichung! test1 fehlgeschlagen!")
    else:
        print("Abweichung! test1 und test2 fehlgeschlagen!")


def TEST_timeframe_amount():
    print("\nTEST: timeframe_amount")
# eier, kartoffel, mehl, saft im zeitraum
    start = dt.date(2024, 9, 11)
    end = dt.date(2024, 10, 9)

    fwl_dict1 = None
    fwl_dict2 = {
        1: {'Datum': '2024-10-09', 'Lebensmittel': 'Saft', 'Menge': '3380', 'Grund': 'Verpackung beschädigt'},
        2: {'Datum': '2024-02-23', 'Lebensmittel': 'Apfel', 'Menge': '1420', 'Grund': 'Überproduktion'},
        3: {'Datum': '2024-09-11', 'Lebensmittel': 'Eier', 'Menge': '4420', 'Grund': 'Reste vom Kochen'},
        4: {'Datum': '2024-01-12', 'Lebensmittel': 'Kartoffel', 'Menge': '4640', 'Grund': 'Reste vom Kochen'},
        5: {'Datum': '2024-09-19', 'Lebensmittel': 'Kartoffel', 'Menge': '2330', 'Grund': 'verdorben'},
        6: {'Datum': '2024-10-03', 'Lebensmittel': 'Mehl', 'Menge': '4280', 'Grund': 'Versehen'}}

    test1_bestanden = True
    got1 = V7.timeframe_amount(start, end, fwl_dict1)
    expected1 = (0, False)
    if got1 != expected1:
        test1_bestanden = False

    test2_bestanden = True
    got2 = V7.timeframe_amount(start, end, fwl_dict2)
    expected2 = (4420 + 2330 + 4280 + 3380, True)
    if got2 != expected2:
        test2_bestanden = False

    if test1_bestanden and test2_bestanden:
        print("Bestanden")
    elif test1_bestanden and not test2_bestanden:
        print("Abweichung! test2 fehlgeschlagen!")
    elif not test1_bestanden and test2_bestanden:
        print("Abweichung! test1 fehlgeschlagen!")
    else:
        print("Abweichung! test1 und test2 fehlgeschlagen!")

def TEST_get_most_frequent_reason():
    print("\nTEST: get_most_frequent_reason")

    fwl_dict1 = None
    fwl_dict2 = {
        1: {'Datum': '2024-08-31', 'Lebensmittel': 'Wurst', 'Menge': '3210', 'Grund': 'Reste vom Kochen'},
        2: {'Datum': '2024-07-23', 'Lebensmittel': 'Gurke', 'Menge': '1400', 'Grund': 'Transport beschädigt'},
        3: {'Datum': '2024-07-29', 'Lebensmittel': 'Kaffee', 'Menge': '2910', 'Grund': 'Reste vom Kochen'},
        4: {'Datum': '2024-05-31', 'Lebensmittel': 'Paprika', 'Menge': '750', 'Grund': 'falsche Lagerung'},
        5: {'Datum': '2024-10-09', 'Lebensmittel': 'Saft', 'Menge': '3380', 'Grund': 'Verpackung beschädigt'},
        6: {'Datum': '2024-02-23', 'Lebensmittel': 'Apfel', 'Menge': '1420', 'Grund': 'Überproduktion'},
        7: {'Datum': '2024-09-11', 'Lebensmittel': 'Eier', 'Menge': '4420', 'Grund': 'Reste vom Kochen'},
        8: {'Datum': '2024-01-12', 'Lebensmittel': 'Kartoffel', 'Menge': '4640', 'Grund': 'Reste vom Kochen'},
        9: {'Datum': '2024-09-19', 'Lebensmittel': 'Kartoffel', 'Menge': '2330', 'Grund': 'verdorben'},
        10: {'Datum': '2024-10-03', 'Lebensmittel': 'Mehl', 'Menge': '4280', 'Grund': 'Versehen'}}

    test1_bestanden = True
    got1 = V7.get_most_frequent_reason(fwl_dict1)
    expected1 = (0, [], False)
    if got1 != expected1:
        test1_bestanden = False

    test2_bestanden = True
    got2 = V7.get_most_frequent_reason(fwl_dict2)
    expected2 = (4, ["Reste vom Kochen"], True)
    if got2 != expected2:
        test2_bestanden = False

    if test1_bestanden and test2_bestanden:
        print("Bestanden")
    elif test1_bestanden and not test2_bestanden:
        print("Abweichung! test2 fehlgeschlagen!")
    elif not test1_bestanden and test2_bestanden:
        print("Abweichung! test1 fehlgeschlagen!")
    else:
        print("Abweichung! test1 und test2 fehlgeschlagen!")

def TEST_output_most_frequent_reasons():
    print("\nTEST: output_most_frequent_reasons")

    test1_bestanden = True
    got1 = V7.output_most_frequent_reasons(4, ["Reste vom Kochen"])
    expected1 = "\n'Reste vom Kochen' ist mit 4 mal der häufigste Grund für das Wegwerfen."
    if got1 != expected1:
        test1_bestanden = False

    test2_bestanden = True
    got2 = V7.output_most_frequent_reasons(6, ["Schimmel", "abgelaufen"])
    expected2 = ("\n'Schimmel' ist mit 6 mal der häufigste Grund für das Wegwerfen."
                 "\nWeitere Gründe mit der selben Häufigkeit:"
                 "\n- 'abgelaufen'")
    if got2 != expected2:
        test2_bestanden = False

    if test1_bestanden and test2_bestanden:
        print("Bestanden")
    elif test1_bestanden and not test2_bestanden:
        print("Abweichung! test2 fehlgeschlagen!")
    elif not test1_bestanden and test2_bestanden:
        print("Abweichung! test1 fehlgeschlagen!")
    else:
        print("Abweichung! test1 und test2 fehlgeschlagen!")

def TEST_final_write_fwl():
    print("\nTEST: final_write_fwl")

    original_fwl_dict2 = {
        1: {'Datum': '2024-08-31', 'Lebensmittel': 'Wurst', 'Menge': '3210', 'Grund': 'Reste vom Kochen'},
        2: {'Datum': '2024-07-23', 'Lebensmittel': 'Gurke', 'Menge': '1400', 'Grund': 'Transport beschädigt'},
        3: {'Datum': '2024-07-29', 'Lebensmittel': 'Kaffee', 'Menge': '2910', 'Grund': 'Reste vom Kochen'},
        4: {'Datum': '2024-05-31', 'Lebensmittel': 'Paprika', 'Menge': '750', 'Grund': 'falsche Lagerung'},
        5: {'Datum': '2024-10-09', 'Lebensmittel': 'Saft', 'Menge': '3380', 'Grund': 'Verpackung beschädigt'},
        6: {'Datum': '2024-02-23', 'Lebensmittel': 'Apfel', 'Menge': '1420', 'Grund': 'Überproduktion'}
    }
    fwl_dict2 = {
        1: {'Datum': '2024-08-31', 'Lebensmittel': 'Wurst', 'Menge': '3210', 'Grund': 'Reste vom Kochen'},
        2: {'Datum': '2024-07-23', 'Lebensmittel': 'Gurke', 'Menge': '1400', 'Grund': 'Transport beschädigt'},
        3: {'Datum': '2024-07-29', 'Lebensmittel': 'Kaffee', 'Menge': '2910', 'Grund': 'Reste vom Kochen'},
        4: {'Datum': '2024-05-31', 'Lebensmittel': 'Paprika', 'Menge': '750', 'Grund': 'falsche Lagerung'},
        5: {'Datum': '2024-10-09', 'Lebensmittel': 'Saft', 'Menge': '3380', 'Grund': 'Verpackung beschädigt'},
        6: {'Datum': '2024-02-23', 'Lebensmittel': 'Apfel', 'Menge': '1420', 'Grund': 'Überproduktion'},
        7: {'Datum': '2024-09-11', 'Lebensmittel': 'Eier', 'Menge': '4420', 'Grund': 'Reste vom Kochen'},
        8: {'Datum': '2024-01-12', 'Lebensmittel': 'Kartoffel', 'Menge': '4640', 'Grund': 'Reste vom Kochen'},
        9: {'Datum': '2024-09-19', 'Lebensmittel': 'Kartoffel', 'Menge': '2330', 'Grund': 'verdorben'},
        10: {'Datum': '2024-10-03', 'Lebensmittel': 'Mehl', 'Menge': '4280', 'Grund': 'Versehen'}
    }

    test1_bestanden = True
    got1 = V7.final_write_fwl(fwl_dict2, False, original_fwl_dict2)
    expected1 = None
    if got1 != expected1:
        test1_bestanden = False

    test2_bestanden = True
    got2 = V7.final_write_fwl(fwl_dict2, True, original_fwl_dict2)
    expected2 = fwl_dict2
    if got2 != expected2:
        test2_bestanden = False

    if test1_bestanden and test2_bestanden:
        print("Bestanden")
    elif test1_bestanden and not test2_bestanden:
        print("Abweichung! test2 fehlgeschlagen!")
    elif not test1_bestanden and test2_bestanden:
        print("Abweichung! test1 fehlgeschlagen!")
    else:
        print("Abweichung! test1 und test2 fehlgeschlagen!")

def main():
    TEST_get_input_options_and_functions()
    TEST_add_indent_to_dict()
    TEST_read_csv()
    TEST_check_option_valid()
    TEST_check_date_valid()
    TEST_check_amount_valid()
    TEST_add_entry_to_temporary_dict()
    TEST_get_full_list_str()
    TEST_get_total_amount()
    TEST_get_top3()
    TEST_output_top3()
    TEST_timeframe_amount()
    TEST_get_most_frequent_reason()
    TEST_output_most_frequent_reasons()
    TEST_final_write_fwl()

if __name__ == "__main__":
    main()