from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def communicate_with_mistral(messages, temperature=0.7):
    url = 'http://localhost:1234/v1/chat/completions'  # Endpoint for chat completions
    payload = {
        'messages': messages,
        'temperature': temperature
    }
    headers = {
        'Content-Type': 'application/json',
        # If your server requires an API key, uncomment and update the line below
        # 'Authorization': 'Bearer YOUR_API_KEY'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            # Extracting the message from the first choice
            return response.json().get('choices', [{}])[0].get('message', {}).get('content', "No response received")
        else:
            return f"Error from Mistral: {response.status_code}"
    except Exception as e:
        return f"Failed to communicate with Mistral: {e}"

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    messages = data.get('messages', [])
    temperature = data.get('temperature', 0.7)
    response = communicate_with_mistral(messages, temperature)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
