import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import tempfile
from typing import Optional


def record_audio(duration: int, sample_rate: int = 16000) -> np.ndarray:
    print("🎙️ Recording...")
    audio = sd.rec(
        int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="float32"
    )
    sd.wait()
    print("✅ Recording complete.")
    return np.squeeze(audio)  # squeeze shape from (N, 1) → (N,)


def save_audio_to_wav(audio: np.ndarray, sample_rate: int) -> str:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        scipy.io.wavfile.write(tmp.name, sample_rate, audio)
        return tmp.name


def transcribe_audio(filepath: str, model) -> str:
    result = model.transcribe(filepath)
    return result["text"]


def transcribe_audio_from_array(
    audio: np.ndarray, model, sample_rate: int = 16000
) -> str:
    """
    Transcribes raw audio (NumPy array) without saving to disk.
    """
    # Ensure it's float32 mono audio
    if audio.ndim > 1:
        audio = audio[:, 0]
    audio = audio.astype("float32")

    result = model.transcribe(audio, fp16=False)  # fp16=False if running on CPU
    return result["text"]
