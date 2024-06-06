from flask import Flask, render_template, request, jsonify, send_file
import requests
from TTS.api import TTS
import os
import time
import wave

API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:instruct"
OUTPUT_FILE = "output.wav"

app = Flask(__name__)

# Initialize a list to store messages
messages = []
topic = ""
npc1_background = ""
npc2_background = ""

# Initialize TTS with the pre-trained model and set the device to CUDA
try:
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=True)
    print("TTS model initialized with GPU support.")
except Exception as e:
    print("Error initializing TTS model:", e)

@app.route("/")
def index():
    return render_template("index.html", messages=messages)

@app.route("/initialize", methods=["POST"])
def initialize():
    global topic, npc1_background, npc2_background
    topic = request.form["topic"]
    npc1_background = request.form["npc1_background"]
    npc2_background = request.form["npc2_background"]
    messages.clear()
    return jsonify({"status": "initialized"})

@app.route("/chat", methods=["POST"])
def chat():
    global topic, npc1_background, npc2_background

    if not topic or not npc1_background or not npc2_background:
        return jsonify({"error": "Conversation not initialized with topic and backgrounds"})

    user_message = request.form["message"]
    messages.append({"text": user_message, "sender": "user"})

    instruction_npc1 = f"NPC1: {npc1_background} The topic is {topic}. Please do not respond with any numbers or special characters. Please create a prompt that would take around 20 seconds of speech to read. Please respond naturally to the following input: "
    instruction_npc2 = f"NPC2: {npc2_background} The topic is {topic}. Please do not respond with any numbers or special characters. Please create a prompt that would take around 20 seconds of speech to read. Please respond naturally to the following input: "

    npc1_message = generate_response(instruction_npc1, user_message)
    if npc1_message:
        messages.append({"text": npc1_message, "sender": "NPC1"})

        npc2_message = generate_response(instruction_npc2, npc1_message)
        if npc2_message:
            messages.append({"text": npc2_message, "sender": "NPC2"})

            # Generate TTS output for NPC2's message
            try:
                tts.tts_to_file(text=npc2_message, file_path=OUTPUT_FILE)
                print("TTS output generated successfully.")
            except Exception as e:
                print("Error generating TTS output:", e)
                return jsonify({"error": "TTS generation failed"})

            # Check the length of the generated .wav file
            with wave.open(OUTPUT_FILE, 'r') as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / float(rate)
                time.sleep(duration + 2)  # Wait for the duration of the .wav file plus 2 seconds

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
        generated_text = response_data.get("response")
        # Add the response to the list
        messages.append({"text": generated_text, "sender": "bot"})
        
        # Generate TTS output
        try:
            tts.tts_to_file(text=generated_text, file_path=OUTPUT_FILE)
            print("TTS output generated successfully.")
        except Exception as e:
            print("Error generating TTS output:", e)
            return None

        return generated_text
    else:
        error_message = f"Error: Received status code {response.status_code}"
        print(error_message)
        return None

@app.route("/play_tts")
def play_tts():
    if os.path.exists(OUTPUT_FILE):
        return send_file(OUTPUT_FILE, as_attachment=False)
    else:
        return jsonify({"error": "TTS output file not found"})

if __name__ == "__main__":
    app.run(debug=True)