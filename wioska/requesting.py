import requests

# The URL for the API endpoint
url = 'http://127.0.0.1:11434'

# Example payload (you'll need to adjust this based on the actual API requirements)
payload = {
    'input': 'Your input text here',
    # Add any other required parameters according to the API documentation
}

# Send a POST request to the model
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Process the response here
    print(response.json())
else:
    print(f"Error: {response.status_code}")