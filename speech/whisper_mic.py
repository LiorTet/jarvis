# main.py
import whisper
from utils.whisper_utils import record_audio, save_audio_to_wav, transcribe_audio

SAMPLE_RATE = 16000
DURATION = 5
model = whisper.load_model("base")

if __name__ == "__main__":
    audio = record_audio(DURATION, SAMPLE_RATE)
    audio_path = save_audio_to_wav(audio, SAMPLE_RATE)
    text = transcribe_audio(audio_path, model)
    print("You said:", text)
