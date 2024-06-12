from flask import Flask, render_template, request, jsonify, send_file
import requests
from TTS.api import TTS
import os
import wave
import glob
import random

API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:instruct"
OUTPUT_DIR = "c:\\projects\\all-projects\\tts\\coqui\\TTS\\"

app = Flask(__name__)

# Initialize a list to store messages
messages = []
topic = ""
npc_backgrounds = []
current_speaker = "NPC1"
response_count = {"NPC1": 0, "NPC2": 0}
user_background = "You are a helpful AI model."

# Initialize TTS with the pre-trained model and set the device to CUDA
try:
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=True)
    print("TTS model initialized with GPU support.")
except Exception as e:
    print("Error initializing TTS model:", e)

@app.route("/")
def index():
    return render_template("index2.html", messages=messages)

@app.route("/initialize", methods=["POST"])
def initialize():
    global topic, npc_backgrounds, current_speaker, response_count
    topic = request.form["topic"]
    npc_count = int(request.form["npc_count"])
    npc_backgrounds = request.form.getlist("npc_backgrounds[]")
    messages.clear()
    current_speaker = "NPC1"
    response_count = {f"NPC{i+1}": 0 for i in range(npc_count)}

    # Generate random backgrounds if not provided
    for i in range(npc_count):
        if not npc_backgrounds[i]:
            npc_backgrounds[i] = generate_random_background()

    # Start the conversation with NPC1
    instruction_npc1 = f"NPC1: {npc_backgrounds[0]} The topic is {topic}. Please do not respond with any numbers or special characters. Please create a prompt that would take around 20 seconds of speech to read. Please respond naturally to the following input: "
    initial_message = "npc1 can start"
    npc1_message = generate_response(instruction_npc1, initial_message)
    if npc1_message:
        messages.append({"text": npc1_message, "sender": "NPC1"})
        generate_tts(npc1_message)
        response_count["NPC1"] += 1
    
    return jsonify({"status": "initialized", "message": npc1_message})

@app.route("/npc_chat", methods=["POST"])
def npc_chat():
    global topic, npc_backgrounds, current_speaker

    if not topic or not npc_backgrounds:
        return jsonify({"error": "Conversation not initialized with topic and backgrounds"})

    user_message = request.form["message"]
    messages.append({"text": user_message, "sender": "user"})

    current_npc_index = int(current_speaker[3:]) - 1

    next_npc_index = (current_npc_index + 1) % len(npc_backgrounds)
    next_npc = f"NPC{next_npc_index + 1}"

    current_instruction = f"{current_speaker}: {npc_backgrounds[current_npc_index]} The topic is {topic}. Please do not respond with any numbers or special characters. Please create a prompt that would take around 20 seconds of speech to read. Please respond naturally to the following input: "
    next_instruction = f"{next_npc}: {npc_backgrounds[next_npc_index]} The topic is {topic}. Please do not respond with any numbers or special characters. Please create a prompt that would take around 20 seconds of speech to read. Please respond naturally to the following input: "

    current_npc_message = generate_response(current_instruction, user_message)
    if current_npc_message:
        messages.append({"text": current_npc_message, "sender": current_speaker})
        generate_tts(current_npc_message)
        response_count[current_speaker] += 1
        current_speaker = next_npc
        return jsonify({"message": current_npc_message, "sender": f"{current_speaker} (response {response_count[current_speaker]})"})

    return jsonify({"error": "Failed to generate conversation"})

@app.route("/user_chat", methods=["POST"])
def user_chat():
    user_message = request.form["message"]
    messages.append({"text": user_message, "sender": "user"})

    instruction = f"Model: {user_background} Please respond naturally to the following input: "
    model_response = generate_response(instruction, user_message)
    if model_response:
        messages.append({"text": model_response, "sender": "Model"})
        return jsonify({"message": model_response})

    return jsonify({"error": "Failed to generate response"})

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
        # Sanitize the generated text to remove problematic characters
        sanitized_text = sanitize_text(generated_text)
        return sanitized_text
    else:
        error_message = f"Error: Received status code {response.status_code}"
        print(error_message)
        return None

def sanitize_text(text):
    sanitized_text = text.replace('"""', '').replace("'''", '').replace('"', '').replace("'", "")
    return sanitized_text

def generate_tts(text):
    output_files = glob.glob(os.path.join(OUTPUT_DIR, "output_*.wav"))
    file_number = len(output_files) + 1
    output_file = os.path.join(OUTPUT_DIR, f"output_{file_number}.wav")
    
    try:
        tts.tts_to_file(text=text, file_path=output_file)
        print(f"TTS output generated successfully: {output_file}")
    except Exception as e:
        print("Error generating TTS output:", e)
        return None

    return output_file

def generate_random_background():
    backgrounds = [
        "You are a villager on a remote island, taking care mostly of fishing and hunting.",
        "You are a blacksmith in a medieval village, crafting weapons and tools.",
        "You are a farmer in a rural area, growing crops and raising livestock.",
        "You are a scholar in an ancient city, studying old texts and teaching students."
    ]
    return random.choice(backgrounds)

@app.route("/play_tts")
def play_tts():
    output_files = glob.glob(os.path.join(OUTPUT_DIR, "output_*.wav"))
    if output_files:
        latest_file = sorted(output_files, key=os.path.getctime)[-1]
        return send_file(latest_file, as_attachment=False)
    else:
        return jsonify({"error": "TTS output file not found"})

@app.route("/cleanup")
def cleanup():
    output_files = glob.glob(os.path.join(OUTPUT_DIR, "output_*.wav"))
    for file in output_files:
        os.remove(file)
    return jsonify({"status": "cleaned up"})

if __name__ == "__main__":
    app.run(debug=True)
