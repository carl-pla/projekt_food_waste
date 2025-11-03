import datetime
import csv

datei_name = input("Geben Sie den Dateinamen ohne Format ein: ")

with open f("{datei_name}.csv", mode="r") as datei:
    reader = csv.reader(datei)
    daten = list(reader)
