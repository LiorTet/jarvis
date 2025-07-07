import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile

# Load Whisper model (use "base", "small", "medium", or "large")
model = whisper.load_model("base")

SAMPLE_RATE = 16000
DURATION = 5  # seconds

def record_audio(duration):
    print("Recording...")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    print("Recording complete.")
    return audio

def transcribe_audio(audio):
    # Save to temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        scipy.io.wavfile.write(tmp.name, SAMPLE_RATE, audio)
        result = model.transcribe(tmp.name)
    return result['text']

if __name__ == "__main__":
    audio = record_audio(DURATION)
    text = transcribe_audio(audio)
    print("You said:", text)

    # Now do whatever you want with `text`
