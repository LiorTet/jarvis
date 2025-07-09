import whisper
import sounddevice as sd
import scipy.io.wavfile
import tempfile


def record_audio(duration, sample_rate=16000):
    print("Recording...")
    audio = sd.rec(
        int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="float32"
    )
    sd.wait()
    print("Recording complete.")
    return audio


def save_audio_to_wav(audio, sample_rate):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        scipy.io.wavfile.write(tmp.name, sample_rate, audio)
        return tmp.name


def transcribe_audio(filepath, model):
    result = model.transcribe(filepath)
    return result["text"]
