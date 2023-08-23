import requests

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

data = {
    "model": "llama2",
    "prompt": "Why is the sky blue?"
}

# response = requests.post(url, json=data, headers=headers, stream=True)

# Make the POST request
with requests.post(url, json=data, headers=headers, stream=True) as response:
    response.raise_for_status()

    for line in response.iter_lines():
        print(line.decode('utf-8'))
