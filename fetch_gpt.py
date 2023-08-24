import json
import logging
import os
import re

import openai

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to extract and validate the output JSON


def extract_events_from_json(input_json_string):

    logging.info('Starting extraction for input data...')

    # Construct the initial prompt for the API
    prompt = (f"You are a service that translates a JSON into another JSON based on historical events. "
              f"Given the JSON below, extract significant events from the \"history_text_cleaned\" "
              f"and \"short_description_text_cleaned\" fields.\n\n"
              f"```"
              f"{input_json_string.replace('{', '{{').replace('}', '}}')}"
              f"```\n\n"
              "Please generate the expected output as a valid JSON format and place it between code fences.\n\n"
              "Expected Output Format:\n\n"
              "```\n"
              "{\n"
              "  \"id\": \"Extracted from the input JSON.\",\n"
              "  \"events\": [\n"
              "    {\n"
              "      \"description\": \"A brief summary of the event.\",\n"
              "      \"conclusionWord\": \"One word that sums up the event.\",\n"
              "      \"time\": \"Either a single Date in strict ISO 8601 format 'YYYY-MM-DD' or a duration object with 'from' and 'to' dates in strict ISO 8601 format 'YYYY-MM-DD'.\",\n"
              "      \"approximateDate\": \"true if the date is approximate, false otherwise.\"\n"
              "    }\n"
              "  ]\n"
              "}\n"
              "```\n\n"
              "Please make sure your response contains a valid JSON structure wrapped between code fences.")

    # Fetch the API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a specialist in converting and extracting information from JSON based on historical events."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and validate the response JSON
    output_text = response.choices[0].message['content'].strip()

    # Extract JSON between code fences using regex
    match = re.search(r'```\n(.*?)\n```', output_text, re.DOTALL)
    if not match:
        logging.error('No JSON found between code fences.')
        return refetch_api_with_error_message("No JSON found between code fences.", input_json_string)

    json_str_between_fences = match.group(1)

    try:
        output_json = json.loads(json_str_between_fences)
        logging.info('JSON extraction successful.')
        return output_json
    except json.JSONDecodeError as e:
        logging.error(f'Error decoding JSON: {e}')
        return refetch_api_with_error_message(str(e), input_json_string)
# Function to refetch the API on error


def refetch_api_with_error_message(error_message, input_json_string):

    logging.info('Refetching with error message...')

    retry_prompt = f"""The JSON structure returned was incorrect because of the following reason: {error_message}. 
Given the original data, can you generate the expected JSON format as specified earlier?

{input_json_string}

Expected Output Format:

id: Extracted from the input JSON.
events: A list of events. For each event:
description: A brief summary of the event.
conclusionWord: One word that sums up the event.
time: Either a single Date in strict ISO 8601 format "YYYY-MM-DD" or a duration object with "from" and "to" dates in strict ISO 8601 format "YYYY-MM-DD".
approximateDate: true if the date is approximate, false otherwise.

Return the translated JSON."""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a specialist in converting and extracting information from JSON based on historical events."},
            {"role": "user", "content": retry_prompt}
        ]
    )

    output_text = response.choices[0].message['content'].strip()

    # Extract JSON between code fences using regex, if present
    match = re.search(r'```\n(.*?)\n```', output_text, re.DOTALL)
    json_to_parse = match.group(1) if match else output_text

    try:
        output_json = json.loads(json_to_parse)
        logging.info('JSON extraction successful in refetch.')
        return output_json
    except json.JSONDecodeError as e:
        logging.error(f'Error decoding JSON on refetch: {e}')
        return None


# Read the input JSON file
with open('output/filtered_dump_1.json', 'r') as file:
    data = json.load(file)

# Process each item in the input JSON
for item in data:
    # Remove the "main_coords_parsed" entry before constructing the prompt
    if 'main_coords_parsed' in item:
        del item['main_coords_parsed']

    # Extract events from the JSON and save the response to a separate JSON file
    output_data = extract_events_from_json(json.dumps(item))
    if output_data:
        with open(f"generated_output/{item['id']}.json", 'w') as outfile:
            json.dump(output_data, outfile)

logging.info('Script execution completed.')
