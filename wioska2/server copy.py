from flask import Flask, render_template, request, jsonify, send_file
import requests
from TTS.api import TTS
import os
import time

API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:instruct"
INSTRUCTION = "please do not answer with anything other than letters (so for example 'four' instead of '4' and nothing else than a comma and separator (, or .)), but make the response sound as natural as possible, instead of one word reply: "

app = Flask(__name__)

# Initialize a list to store messages
messages = []

# Initialize TTS with the pre-trained model and set the device to CUDA
try:
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=True)
    print("TTS model initialized with GPU support.")
except Exception as e:
    print("Error initializing TTS model:", e)

@app.route("/")
def index():
    # Pass existing messages to the template
    return render_template("index.html", messages=messages)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]
    # Prepend the instruction to the user's message
    message = INSTRUCTION + user_message
    # Add the user's message to the list
    messages.append({"text": user_message, "sender": "user"})

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
        
        # Generate TTS output
        output_file = "c:\\projects\\all-projects\\tts\\coqui\\TTS\\output.wav"
        try:
            tts.tts_to_file(text=generated_text, file_path=output_file)
            print("TTS output generated successfully.")
        except Exception as e:
            print("Error generating TTS output:", e)
            return jsonify({"error": "TTS generation failed"})

        return jsonify({"message": generated_text})
    else:
        error_message = f"Error: Received status code {response.status_code}"
        return jsonify({"error": error_message})

@app.route("/play_tts")
def play_tts():
    # Send the TTS output file to the client with a unique query parameter to prevent caching
    output_file = "c:\\projects\\all-projects\\tts\\coqui\\TTS\\output.wav"
    if os.path.exists(output_file):
        return send_file(output_file, as_attachment=False)
    else:
        return jsonify({"error": "TTS output file not found"})

if __name__ == "__main__":
    app.run(debug=True)
