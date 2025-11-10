# Test FUnktion soll nicht an die datei gebunden sein 
# einzlene funktion für file handling (nicht testen), unabhängig von Datenbank testen
# interne Struktur prüfen

"""
Beispiel: 
# Simulierte "Tabelle" Users
users = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
]

# Funktion, die User nach Alter filtert
def get_users_older_than(users, age):
    return [u for u in users if u["age"] > age]

# Test
older_users = get_users_older_than(users, 26)
print(older_users)  # [{'id': 2, 'name': 'Bob', 'age': 30}]


""" 
