from flask import Flask, render_template, request, jsonify
import requests

API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:instruct"

app = Flask(__name__)

# Initialize a list to store messages
messages = []

@app.route("/")
def index():
    # Pass existing messages to the template
    return render_template("index.html", messages=messages)

@app.route("/chat", methods=["POST"])
def chat():
    message = request.form["message"]
    # Add the user's message to the list
    messages.append({"text": message, "sender": "user"})

    data = {
        "model": MODEL_NAME,
        "prompt": message,
        "stream": False,
        "temperature": 0.7
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(API_URL, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        generated_text = response_data.get("response")
        # Add the response to the list
        messages.append({"text": generated_text, "sender": "bot"})
        return jsonify({"message": generated_text})
    else:
        error_message = f"Error: Received status code {response.status_code}"
        return jsonify({"error": error_message})

if __name__ == "__main__":
    app.run(debug=True)
