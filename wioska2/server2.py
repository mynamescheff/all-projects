from flask import Flask, render_template, request, jsonify, send_file
import requests
from TTS.api import TTS
import os
import time

API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:instruct"
INSTRUCTION_NPC1 = "NPC1: Please respond naturally to the following input: "
INSTRUCTION_NPC2 = "NPC2: Please respond naturally to the following input: "

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
    return render_template("index.html", messages=messages)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]
    messages.append({"text": user_message, "sender": "user"})

    npc1_message = generate_response(INSTRUCTION_NPC1, user_message)
    if npc1_message:
        messages.append({"text": npc1_message, "sender": "NPC1"})

        npc2_message = generate_response(INSTRUCTION_NPC2, npc1_message)
        if npc2_message:
            messages.append({"text": npc2_message, "sender": "NPC2"})

            # Generate TTS output for NPC2's message
            output_file = "output.wav"
            try:
                tts.tts_to_file(text=npc2_message, file_path=output_file)
                print("TTS output generated successfully.")
            except Exception as e:
                print("Error generating TTS output:", e)
                return jsonify({"error": "TTS generation failed"})

            return jsonify({"message": npc2_message})
    
    return jsonify({"error": "Failed to generate conversation"})

def generate_response(instruction, input_message):
    data = {
        "model": MODEL_NAME,
        "prompt": instruction + input_message,
        "stream": False,
        "temperature": 0.7
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(API_URL, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("response")
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

@app.route("/play_tts")
def play_tts():
    output_file = "output.wav"
    if os.path.exists(output_file):
        return send_file(output_file, as_attachment=False)
    else:
        return jsonify({"error": "TTS output file not found"})

if __name__ == "__main__":
    app.run(debug=True)
