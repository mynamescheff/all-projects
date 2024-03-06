from flask import Flask, render_template, request, jsonify
import requests
import json

# Replace with your Dolphin API details
API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "dolphin-mixtral:latest"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.form["message"]
    options = {
        "temperature": 0.7, # Example option
        "stream": False # Add stream option here
    }

    data = {
        "model": MODEL_NAME,
        "prompt": message,
        "options": options,
    }
    
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}

    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        generated_text = response_data.get("generated_text", "No response generated") 
        return jsonify({"message": generated_text})
    else:
        error_message = f"Error: Received status code {response.status_code}"
        print(error_message, response.text)
        return jsonify({"error": error_message})

if __name__ == "__main__":
    app.run(debug=True)
