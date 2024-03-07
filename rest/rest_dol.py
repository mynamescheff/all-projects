from flask import Flask, render_template, request, jsonify
import requests

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

    data = {
        "model": MODEL_NAME,
        "prompt": message,
        "stream": False,  # Assuming 'stream' is at the correct level
        "temperature": 0.7  # Assuming 'temperature' is also expected at this level
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(API_URL, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        # Print the whole response data to check the structure
        print("Response Data:", response_data)

        # Extract the response text using the correct key, based on the API's response format
        generated_text = response_data.get("response")  # Modify this according to your API's response structure
        return jsonify({"message": generated_text})
    else:
        error_message = f"Error: Received status code {response.status_code}"
        print(error_message, response.text)
        return jsonify({"error": error_message})

if __name__ == "__main__":
    app.run(debug=True)
