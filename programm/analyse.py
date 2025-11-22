from datetime import datetime

def gesamte_verschwendung(data):
    summe = 0
    for row in data.values():
        try:
            summe += float(row["waste"])
        except (KeyError, ValueError):
            continue
    return summe

def lebensmittel_meiste_verschwendung(data):
    aggregiert = {}
    for row in data.values():
        try:
            key = row["lebensmittel"]
            waste = float(row["waste"])

            if key not in aggregiert:
                aggregiert[key] = waste
            else:
                aggregiert[key] += waste
        except (KeyError, ValueError):
            continue
    
    top3 = sorted(aggregiert.items(), key = lambda x: x[1], reverse = True)[0:3]
    return top3    
            
def zeitraum(eingabe_start, eingabe_ende, data):
    start_datum = datetime.strptime(eingabe_start, "%Y-%m-%d").date()
    ende_datum = datetime.strptime(eingabe_ende, "%Y-%m-%d").date()
    daten_im_zeitraum = []

    for row in data.values():
        try:
            datum = datetime.strptime(row["datum"], "%Y-%m-%d").date()
            if start_datum <= datum <= ende_datum:
                daten_im_zeitraum.append(row)
        except (KeyError, ValueError):
            continue

    return daten_im_zeitraum  

def grund(data):
    gruende = {}
    for row in data.values():
        try:
            key = row["grund"]
            anzahl = 1

            if key not in gruende:
                gruende[key] = anzahl
            else:
                gruende[key] += anzahl
        except (KeyError, ValueError):
                continue
        
        top5 = sorted(gruende.items(), key = lambda x: x[1], reverse = True)[0:5]
    return top5
