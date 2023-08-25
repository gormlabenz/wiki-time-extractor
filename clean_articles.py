import json
import os
import re


def comprehensive_clean(text):
    """Comprehensive cleaning function with updated artifacts removal"""

    # Removing specific artifacts identified from the Wikipedia XML Dump
    text = re.sub(r'<<OutputTruncated>>', '', text)

    # Remove content within double curly braces
    text = re.sub(r'{{[^}]*}}', '', text)

    # Remove content within square brackets
    text = re.sub(r'\[\[[^\]]*\]\]', '', text)

    # Remove content with |word|
    text = re.sub(r'\|[^\|]*\|', '', text)

    # Remove file and image related artifacts
    text = re.sub(r'(?i)\[\[file:.*?\]\]', '', text)
    text = re.sub(r'(?i)\[\[image:.*?\]\]', '', text)

    # Remove content within single curly braces
    text = re.sub(r'{[^}]*}', '', text)

    # Remove any URLs
    text = re.sub(r'http[s]?://\S+', '', text)

    # Remove content within parentheses that contains numbers and commas or just commas
    text = re.sub(r'\(\d+,\d+\)', '', text)
    text = re.sub(r'\(,\s, abbreviated', '', text)
    text = re.sub(r'\(\d+\)', '', text)
    text = re.sub(r'\(\)', '', text)

    text = re.sub(r'<<.+?>>', '', text)

    # Remove any single standalone square brackets
    text = re.sub(r'\[|\]', '', text)

    return text


# Pfad zum Ausgabeordner festlegen
output_dir = "articles"
cleaned_output_dir = "articles_cleaned"

# Stellen Sie sicher, dass der cleaned_output_dir existiert
if not os.path.exists(cleaned_output_dir):
    os.makedirs(cleaned_output_dir)

# Durch alle Dateien im Ausgabeordner iterieren
for filename in os.listdir(output_dir):
    # Überprüfen Sie, ob die Datei dem Muster "article_[id].json" entspricht
    if filename.startswith("article") and filename.endswith(".json"):

        # Dateipfad erstellen
        file_path = os.path.join(output_dir, filename)

        # JSON-Daten laden
        with open(file_path, "r") as file:
            data = json.load(file)

        # Daten reinigen
        for entry in data:
            entry['history_text_cleaned'] = comprehensive_clean(
                entry['history_text_cleaned'])
            entry['short_description_text_cleaned'] = comprehensive_clean(
                entry['short_description_text_cleaned'])

        # Pfad für die bereinigte Datei erstellen
        cleaned_file_path = os.path.join(cleaned_output_dir, filename)

        # Bereinigte Daten speichern
        with open(cleaned_file_path, "w") as file:
            json.dump(data, file, indent=4)

print("Cleaning completed and saved to the 'articles_cleaned' directory.")
