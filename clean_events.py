import copy
import json
import os
import pprint
import re

# Convert to BC format


def is_valid_date(date_str):
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str) or re.fullmatch(r"\d{4}-\d{2}-\d{2} BC", date_str):
        return True
    else:
        return False


def convert_date_format(date_str):
    # Überprüfen, ob das Datum im "-YYYY-MM-DD"-Format vorliegt
    if re.match(r"-\d{4}-\d{2}-\d{2}", date_str):
        # Entfernen des vorangestellten Minuszeichens
        return date_str[1:] + " BC"
    else:
        # Wenn nicht im gesuchten Format, ursprüngliches Datum zurückgeben
        return date_str


def clean_date(date_str):
    """
    Final clean_date function to handle various date formats.
    """
    # Check for "present" immediately
    if date_str.strip().lower() == "present":
        return "2023-01-01"

    # Step 1: Check if the date is already in the correct format
    if is_valid_date(date_str):
        return date_str

    # Step 2: Check if the date contains two dates
    # a) -1861-1865
    match = re.fullmatch(r"(-?\d{4})-(-?\d{4})", date_str)
    if match:
        return {
            "from": convert_date_format(match.group(1) + "-01-01"),
            "to": convert_date_format(match.group(2) + "-01-01")
        }
    # b) -1700/1799
    match = re.fullmatch(r"(-?\d{4})/(-?\d{4})", date_str)
    if match:
        return {
            "from": convert_date_format(match.group(1) + "-01-01"),
            "to": convert_date_format(match.group(2) + "-01-01")
        }
    # c) -1700-01-01/1799-12-31
    match = re.fullmatch(
        r"(-?\d{4}-\d{2}-\d{2})/(-?\d{4}-\d{2}-\d{2})", date_str)
    if match:
        return {
            "from": convert_date_format(match.group(1)),
            "to": convert_date_format(match.group(2))
        }
    # d) 1750/01/01 to 1807/12/31
    match = re.fullmatch(
        r"(-?\d{4}/\d{2}/\d{2}) to (-?\d{4}/\d{2}/\d{2})", date_str)
    if match:
        return {
            "from": clean_date(match.group(1).replace("/", "-")),
            "to": clean_date(match.group(2).replace("/", "-"))
        }
    # e) 1807-Present
    match = re.fullmatch(r"(-?\d{4})-Present", date_str, re.IGNORECASE)
    if match:
        return {
            "from": clean_date(match.group(1)),
            "to": "2023-01-01"
        }
    # f) 1750/01/01
    match = re.fullmatch(r"(-?\d{4}/\d{2}/\d{2})", date_str)
    if match:
        return clean_date(match.group(1).replace("/", "-"))

    # Step 3: Remove all characters that are not a number, hyphen or slash
    cleaned_date = re.sub(r"[^0-9\-/]", "", date_str)

    # Step 4: Transformations
    # a) -1972 => -1972-01-01
    if re.fullmatch(r"-?\d{4}", cleaned_date):
        return cleaned_date + "-01-01"
    # b) "" => Replace with None
    if cleaned_date == "":
        return None
    # c) 2013-03 => 2013-03-01
    if re.fullmatch(r"-?\d{4}-\d{2}", cleaned_date):
        return cleaned_date + "-01"
    # d) 500-01-01 => 0500-01-01
    if re.fullmatch(r"\d{3}-\d{2}-\d{2}", cleaned_date):
        return "0" + cleaned_date

    cleaned_date = convert_date_format(cleaned_date)

    # Step 5: Re-check if the date is valid
    if not is_valid_date(cleaned_date):
        return None

    return cleaned_date


def transform_and_clean_data(data):
    # copy data["events"] to old_events
    old_events = copy.deepcopy(data["events"])

    for event in data["events"]:
        time = event["time"]

        if isinstance(time, str):
            event["time"] = clean_date(time)
        elif isinstance(time, dict) and 'from' in time and 'to' in time:
            event["time"]["from"] = clean_date(time["from"])
            event["time"]["to"] = clean_date(time["to"])

    for event in data["events"]:
        if event["time"] is None:
            # print old_event
            old_event = filter(
                lambda x: x["description"] == event["description"], old_events)
            print(list(old_event)[0]["time"], data["id"])

    data["events"] = [event for event in data["events"]
                      if event["time"] is not None]

    return data


def main():
    source_dir = "events"
    dest_dir = "events_cleaned"

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for filename in os.listdir(source_dir):
        if filename.endswith('.json'):
            with open(os.path.join(source_dir, filename), 'r') as f:
                data = json.load(f)

            cleaned_data = transform_and_clean_data(data)

            with open(os.path.join(dest_dir, filename), 'w') as f:
                json.dump(cleaned_data, f, indent=4)

    print("Transformation and cleaning completed!")


if __name__ == "__main__":
    main()
