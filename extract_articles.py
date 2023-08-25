import json
import logging
import re

import mwparserfromhell
import mwxml

logging.basicConfig(level=logging.INFO)

patterns = [
    re.compile(r'\[\[File:.*?\]\]', re.IGNORECASE),
    re.compile(r'^thumb\s*\|.*$', re.IGNORECASE | re.MULTILINE),
    re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
]


def get_next_filename(base_filename, counter):
    return f"{base_filename.rsplit('.', 1)[0]}_{counter}.json"


def clean_text(text):
    for pattern in patterns:
        text = pattern.sub('', text)
    return text


def parse_coord(template):
    # Entferne '{{' am Anfang, wenn vorhanden
    if template.startswith('{{'):
        template = template[2:]

    parts = template.split('|')

    # Entferne 'coord' oder 'Coord' und leere Einträge
    parts = [part.strip()
             for part in parts if part and not re.match(r'coord', part, re.I)]

    try:
        if len(parts) >= 5 and any(x in parts[2] for x in ['N', 'S']) and any(x in parts[5] for x in ['E', 'W']):
            # Format: {{coord|33|22.5|N|43|43|E|...}}
            lat, lon = float(parts[0]) + float(parts[1]) / \
                60, float(parts[3]) + float(parts[4])/60
            if 'S' in parts[2]:
                lat = -lat
            if 'W' in parts[5]:
                lon = -lon
        elif len(parts) >= 8 and any(x in parts[3] for x in ['N', 'S']) and any(x.strip() in parts[7] for x in ['E', 'W']):
            # Format: {{coord|20|33|12|N|75|42|01|E|...}}
            lat = float(parts[0]) + float(parts[1])/60 + float(parts[2])/3600
            lon = float(parts[4]) + float(parts[5])/60 + float(parts[6])/3600
            if 'S' in parts[3]:
                lat = -lat
            if 'W' in parts[7].strip():
                lon = -lon
        elif len(parts) >= 8 and any(x in parts[2] for x in ['N', 'S']) and any(x.strip() in parts[6] for x in ['E', 'W']):
            # Format: {{coord|40|45|06|N|73|58|31|W|...}}
            lat = float(parts[0]) + float(parts[1])/60 + float(parts[2])/3600
            lon = float(parts[3]) + float(parts[4])/60 + float(parts[5])/3600
            if 'S' in parts[2]:
                lat = -lat
            if 'W' in parts[6].strip():
                lon = -lon
        elif len(parts) >= 4 and any(x in parts[1] for x in ['N', 'S']) and any(x in parts[3] for x in ['E', 'W']):
            # Format: {{Coord|10|S|52|W|...}}
            lat, lon = float(parts[0]), float(parts[2])
            if 'S' in parts[1]:
                lat = -lat
            if 'W' in parts[3]:
                lon = -lon
        elif len(parts) >= 2:
            # Format: {{coord|-16.712|-64.666|...}} or {{Coord|44.532447|N|10.864137|E|...}}
            lat = float(parts[0])
            lon = float(parts[1])
            if len(parts) > 2 and 'S' in parts[2] and lat > 0:
                lat = -lat
            # Correcting Grinnell College error
            elif len(parts) > 2 and 'N' in parts[2] and lat < 0:
                lat = abs(lat)
            if len(parts) > 3 and 'W' in parts[3]:
                lon = -lon
        else:
            return None
    except ValueError:
        # Ein unbekanntes Format oder ein Fehler beim Parsen; wir geben None zurück
        return None

    # Rückgabe im GeoJSON "Point" Format
    return {
        "type": "Point",
        "coordinates": [lon, lat]
    }


def process_dump(dump_file, base_output_file):
    dump = mwxml.Dump.from_file(open(dump_file))
    saved_articles = 0
    file_counter = 1
    processed_articles = 0
    articles_list = []

    for page in dump:
        if page.redirect or page.namespace != 0:
            continue

        for revision in page:
            try:
                wikicode = mwparserfromhell.parse(revision.text)
                main_coords = [template for template in wikicode.filter_templates(
                ) if template.name.matches("Coord") and "display=title" in template]
                sections = wikicode.get_sections(include_lead=True, flat=True)
                history_section = list(
                    filter(lambda section: '== History ==' in section, sections))
                short_description_section = list(
                    filter(lambda section: '{{short description' in section, sections))

                if any(history_section) and any(short_description_section) and any(main_coords):
                    history_text = mwparserfromhell.parse(history_section[0]).strip_code(
                        normalize=True, collapse=True, keep_template_params=False)

                    short_description_text = mwparserfromhell.parse(short_description_section[0]).strip_code(
                        normalize=True, collapse=True, keep_template_params=False)

                    # Remove the first line if it contains "History"
                    lines = history_text.split("\n")

                    if lines and "History" in lines[0]:
                        lines = lines[1:]

                    history_text = "\n".join(lines)

                    title = page.title
                    history_text_cleaned = clean_text(history_text)
                    short_description_text_cleaned = clean_text(
                        short_description_text)
                    main_coords_parsed = parse_coord(str(main_coords[0]))

                    if history_text_cleaned == "" or short_description_text_cleaned == "" or main_coords_parsed is None:
                        continue

                    # Store the data into the buffer
                    article_data = {
                        'title': title,
                        'history_text_cleaned': history_text_cleaned,
                        'short_description_text_cleaned': short_description_text_cleaned,
                        'main_coords_parsed': main_coords_parsed,
                        'id': page.id,

                    }
                    articles_list.append(article_data)

                    saved_articles += 1

                    if saved_articles % 100 == 0:
                        output_file = get_next_filename(
                            base_output_file, file_counter)
                        with open(output_file, 'w', encoding='utf-8') as file:
                            json.dump(articles_list, file,
                                      ensure_ascii=False, indent=4)
                        articles_list.clear()
                        file_counter += 1
                        logging.info(
                            f"{page.title} - Processed articles: {processed_articles} and saved to {output_file}")

                processed_articles += 1
            except Exception as e:
                logging.error(
                    f"Error processing: {page.title} Nr. {saved_articles}. Error: {e}")

   # Save any remaining articles to a new JSON file
    if articles_list:
        output_file = get_next_filename(base_output_file, file_counter)
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(articles_list, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    process_dump("dump.xml", "output/filtered_dump.json")
