import glob
import json
import os

from supabase import Client, create_client

# Supabase-Einstellungen
SUPABASE_URL = "https://hlqmmgjeixdtdfmhnsiy.supabase.co"
# API KEY aus den Umgebungsvariablen lesen
SUPABASE_API_KEY = os.environ["SUPABASE_API_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)


def upload_data_to_supabase(file_path):
    # JSON-Datei lesen
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Durch die Daten iterieren und in die Supabase-Datenbank einfügen
    for entry in data["events"]:
        try:
            supabase.table("events").insert({
                "description": entry["description"],
                "short_description": entry["shortDescription"],
                "approximate_date": entry["approximateDate"],
                # Der Artikel-ID aus dem Hauptdatensatz
                "article_id": data["id"],
                "duration_from": entry["time"]["from"] if "from" in entry["time"] else None,
                "duration_to": entry["time"]["to"] if "to" in entry["time"] else None,
                "date": entry["time"] if "to" not in entry["time"] else None,
            }).execute()
            # Falls benötigt, können Sie hier weitere Überprüfungen für die Antwort durchführen.
        except Exception as error:
            print(
                f"Fehler beim Hinzufügen des Events mit der Beschreibung '{entry['description']}' für Artikel mit der ID {data['id']}: {error}")


# Automatisches Laden aller JSON-Dateien im angegebenen Ordner
file_paths = glob.glob("events_cleaned/*.json")

for file_path in file_paths:
    upload_data_to_supabase(file_path)
