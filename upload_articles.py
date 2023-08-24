import glob
import json
import os

from supabase import Client, create_client

# Supabase-Einstellungen
SUPABASE_URL = "https://hlqmmgjeixdtdfmhnsiy.supabase.co"
# API KEY aus den Umgebungsvariablen lesen
SUPABASE_API_KEY = os.environ["SUPABASE_API_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)


def convert_to_wkt(geometry):
    if geometry["type"] == "Point":
        x, y = geometry["coordinates"]
        return f"POINT({x} {y})"
    # Sie können ähnliche Konvertierungen für andere Geometrietypen hinzufügen, falls benötigt.
    return None


def upload_data_to_supabase(file_path):
    # JSON-Datei lesen
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Durch die Daten iterieren und in die Supabase-Datenbank einfügen
    for entry in data:
        wkt_coords = convert_to_wkt(entry["main_coords_parsed"])
        if not wkt_coords:
            print(
                f"Konnte Koordinaten für Artikel mit ID {entry['id']} nicht konvertieren")
            continue
        try:
            response = supabase.table("articles").insert({
                "id": entry["id"],
                "title": entry["title"],
                "history": entry["history_text_cleaned"],
                "short_description": entry["short_description_text_cleaned"],
                "coords": wkt_coords
            }).execute()
            # Falls benötigt, können Sie hier weitere Überprüfungen für die Antwort durchführen.
        except Exception as error:
            print(
                f"Fehler beim Hinzufügen des Artikels mit der ID {entry['id']}: {error}")


# Automatisches Laden aller JSON-Dateien im angegebenen Ordner
file_paths = glob.glob("output_cleaned/*.json")

for file_path in file_paths:
    upload_data_to_supabase(file_path)
