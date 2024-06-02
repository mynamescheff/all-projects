from TTS.api import TTS

# Initialize TTS with the pre-trained model and set the device to CUDA
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=True)

# Generate TTS output
output_file = "output.wav"
text = "This is a test to check if CUDA is working correctly."

try:
    tts.tts_to_file(text=text, file_path=output_file)
    print("TTS output generated successfully.")
except Exception as e:
    print("Error generating TTS output:", e)
