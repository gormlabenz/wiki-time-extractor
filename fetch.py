import json

import requests

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

data1 = {
    "model": "llama2:70B",
    "prompt": """
You are a service that translates a JSON into another JSON.

Extract events from the history_text_cleaned and short_description_text_cleaned fields of the input JSON. Return a JSON with the following TypeScript definitions:

type time = Date | duration // choose if the event has a duration or not; use strict ISO 8601 format
type duration = { from: Date; to: Date } // if the event has a duration; use strict ISO 8601 format

type Event = {
  description: string // describe the event
  conclusionWord: string // one word that sums up the event
  time: time | duration // the date when the event takes place in time
}

export type timeline = {
  id: string // the id taken from the input JSON
  events: Event[] // A list of events, leave empty if no events are mentioned
}

You are given the following JSON:

{
"title": "Quirinal Hill",
"history_text_cleaned": "According to Roman legend, the Quirinal Hill was the site of a small village of the Sabines, and king Titus Tatius would have lived there after the peace between Romans and Sabines. These Sabines had erected altars in the honour of their god Quirinus (naming the hill by this god).\n\nTombs from the 8th century BC to the 7th century BC that confirm a likely presence of a Sabine settlement area have been discovered; on the hill, there was the tomb of Quirinus, which Lucius Papirius Cursor transformed into a temple for his triumph after the third Samnite war. Some authors consider it possible that the cult of the Capitoline Triad (Jove, Minerva, Juno) could have been celebrated here well before it became associated with the Capitoline Hill. The sanctuary of Flora, an Osco-Sabine goddess, was here too.JSTOR – Women on th Quirinal Hill: Patronage in Rome, 1560 – 1630 by Carolyn Valone\n\nAccording to Livy, the hill first became part of the city of Rome, along with the Viminal Hill, during the reign of Servius Tullius, Rome' sixth king, in the 6th century BC.Livy, Ab urbe condita, 1.44\n\nIn 446 BC, a temple was dedicated on the Quirinal in honour of Sancus, and it is possible that this temple was erected over the ruins of another temple. Augustus, too, ordered the building of a temple, dedicated to Mars. On a slope of the Quirinal were the extensive gardens of Sallust.\n\nOn the Quirinal Hill Constantine the Great ordered the erection of his baths, the last thermae complex erected in imperial Rome.  These are now lost, having been incorporated into Renaissance Rome, with only some drawings from the 16th century remaining.\n\nIn the Middle Ages, the Torre delle Milizie and the convent of St. Peter and Domenic were built, and above Constantine's building was erected the Palazzo Pallavicini-Rospigliosi; the two famous colossal marble statues of the Horse Tamers, generally identified as the Dioscuri with horses, which now are in the Piazza Quirinale, were originally in this palazzo. They gave to the Quirinal its medieval name Monte Cavallo, which lingered into the 19th century, when the hill was transformed beyond all recognition by urbanization of an expanding capital of a united Italy. In the same palazzo were also the two statues of river gods that Michelangelo moved to the steps of Palazzo Senatorio on the Capitoline Hill.\n\nAccording to the political division of the center of Rome, the Hill belongs to the rione Trevi.",
"short_description_text_cleaned": "\n\nThe Quirinal Hill (; ;  ) is one of the Seven Hills of Rome, at the north-east of the city center. It is the location of the official residence of the Italian head of state, who resides in the Quirinal Palace; by metonymy \"the Quirinal\" has come to stand for the Italian president. The Quirinal Palace has an extension of 1.2 million square feet.",
}

Example input JSON:

{
"title": "Ajanta Caves",
"history_text_cleaned": "\nThe Ajanta Caves are generally agreed to have been made in two distinct phases; first during the 2nd century BCE to 1st century CE, and second several centuries later.\n\nThe caves consist of 36 identifiable foundations, some of them discovered after the original numbering of the caves from 1 through 29. The later-identified caves have been suffixed with the letters of the alphabet, such as 15A, identified between originally numbered caves 15 and 16. The cave numbering is a convention of convenience, and does not reflect the chronological order of their construction.",
"short_description_text_cleaned": "\n\nThe Ajanta Caves are 29 rock-cut Buddhist cave monuments dating from the second century BCE to about 480 CE in the Chatrapati Sambhaji Nagar District of Maharashtra state in India. Ajanta Caves are a  UNESCO World Heritage Site. Universally regarded as masterpieces of Buddhist religious art, the caves include paintings and rock-cut sculptures described as among the finest surviving examples of ancient Indian art, particularly expressive paintings that present emotions through gesture, pose and form.\n\nThe caves were built in two phases, the first starting around the second century BCE and the second occurring from 400 to 650 CE, according to older accounts, or in a brief period of 460–480 CE according to later scholarship.Ajanta Caves: Advisory Body Evaluation, UNESCO International Council on Monuments and Sites. 1982. Retrieved 27 October 2006. , p. 2. \n\nThe Ajanta Caves constitute ancient monasteries (Viharas) and worship-halls (Chaityas) of different Buddhist traditions carved into a  wall of rock. The caves also present paintings depicting the past lives  and rebirths of the Buddha, pictorial tales from Aryasura's Jatakamala, and rock-cut sculptures of Buddhist deities. Textual records suggest that these caves served as a monsoon retreat for monks, as well as a resting site for merchants and pilgrims in ancient India. While vivid colours and mural wall paintings were abundant in Indian history as evidenced by historical records, Caves 1, 2, 16 and 17 of Ajanta form the largest corpus of surviving ancient Indian wall-paintings.\n\n\nThe Ajanta Caves are mentioned in the memoirs of several medieval-era Chinese Buddhist travellers. They were covered by jungle until accidentally \"discovered\" and brought to Western attention in 1819 by a colonial British officer Captain John Smith on a tiger-hunting party. The caves are in the rocky northern wall of the U-shaped gorge of the river Waghur,variously spelled Waghora or Wagura in the Deccan plateau.Map of Ajanta Caves , UNESCO Within the gorge are a number of waterfalls, audible from outside the caves when the river is high.\n\nWith the Ellora Caves, Ajanta is one of the major tourist attractions of Maharashtra. It is about  from the city of Jalgaon, Maharashtra, India,   from the city of Aurangabad, and  east-northeast of Mumbai. Ajanta is  from the Ellora Caves, which contain Hindu, Jain and Buddhist caves, the last dating from a period similar to Ajanta. The Ajanta style is also found in the Ellora Caves and other sites such as the Elephanta Caves, Aurangabad Caves, Shivleni Caves and the cave temples of Karnataka.",
"id": 2642
}

Example respones JSON:

{
  "id": "2642",
  "events": [
    {
      "description": "The Ajanta Caves were made in two distinct phases: first during the 2nd century BCE to 1st century CE, and second several centuries later.",
      "conclusionWord": "Phases",
      "time": {
        "from": "-0199-01-01",
        "to": "0001-01-01"
      }
    },
    {
      "description": "The Ajanta Caves are 29 rock-cut Buddhist cave monuments dating from the second century BCE to about 480 CE.",
      "conclusionWord": "Monuments",
      "time": {
        "from": "-0199-01-01",
        "to": "0480-01-01"
      }
    },
    {
      "description": "The caves were built in two phases, with the first starting around the second century BCE and the second occurring from 400 to 650 CE.",
      "conclusionWord": "Construction",
      "time": {
        "from": "-0199-01-01",
        "to": "0650-01-01"
      }
    },
    {
      "description": "The Ajanta Caves were mentioned in the memoirs of several medieval-era Chinese Buddhist travellers.",
      "conclusionWord": "Memoirs",
      "time": {
        "from": "0500-01-01", 
        "to": "1500-01-01" 
      }
    },
    {
      "description": "The Ajanta Caves were covered by jungle until they were accidentally \"discovered\" and brought to Western attention in 1819 by a colonial British officer Captain John Smith.",
      "conclusionWord": "Discovery",
      "time": "1819-01-01"
    }
  ]
}
"""
}

data2 = {
    "model": "llama2:70B",
    "prompt": """
You are a service that translates a JSON into another JSON based on historical events.

Given the JSON below, extract significant events from the "history_text_cleaned" and "short_description_text_cleaned" fields. Return a JSON in the format described afterwards.

Input JSON:

{
"title": "Quirinal Hill",
"history_text_cleaned": "...",
"short_description_text_cleaned": "..."
}

Expected Output Format:

id: Extracted from the input JSON.
events: A list of events. For each event:
description: A brief summary of the event.
conclusionWord: One word that sums up the event.
time: Either a single Date in strict ISO 8601 format "YYYY-MM-DD" or a duration object with "from" and "to" dates in strict ISO 8601 format "YYYY-MM-DD".
"approximateDate": true if the date is approximate, false otherwise.

Return the translated JSON.

To ensure that the date formats adhere to the strict ISO 8601 format, you can emphasize in your prompt that all dates must be in the "YYYY-MM-DD" format or an appropriate duration format. Let's refactor the prompt accordingly:

You are a service that translates a JSON into another JSON based on historical events.

Given the JSON below, extract significant events from the "history_text_cleaned" and "short_description_text_cleaned" fields. Return a JSON in the format described afterwards.
"""
}

full_response = ""

# Make the POST request
with requests.post(url, json=data2, headers=headers, stream=True) as response:
    response.raise_for_status()

    for line in response.iter_lines():
        # Decode the line and parse the JSON
        json_line = json.loads(line.decode('utf-8'))

        # Concatenate the "response" value to the full response, if it exists
        if "response" in json_line:
            full_response += json_line["response"]
            print(json_line["response"])

        # Check if "done" is true and break out of the loop if it is
        if json_line.get("done"):
            break

# Print the full response
print(full_response)
