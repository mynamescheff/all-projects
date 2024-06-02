from TTS.api import TTS

# Initialize TTS with the pre-trained model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

# Run TTS
tts.tts_to_file(text="I like to meow hella lot.", file_path="output.wav")
