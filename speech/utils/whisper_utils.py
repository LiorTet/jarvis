import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import tempfile
import time
from typing import Optional


CHUNK_DURATION = 0.5
SILENCE_THRESHOLD = 0.005
SILENCE_DURATION = 2.0


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


def rms(audio_chunk: np.ndarray) -> float:
    return np.sqrt(np.mean(np.square(audio_chunk)))


def record_audio(sample_rate: int = 16000) -> np.ndarray:
    print("🎙️ Recording... Speak now.")
    frames = []
    silence_start = None
    chunk_samples = int(CHUNK_DURATION * sample_rate)

    with sd.InputStream(channels=1, samplerate=sample_rate, dtype="float32") as stream:
        while True:
            data, _ = stream.read(chunk_samples)
            data = data.flatten()
            frames.append(data)

            current_rms = rms(data)
            if current_rms < SILENCE_THRESHOLD:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > SILENCE_DURATION:
                    print("Silence detected, stopping recording.")
                    break
            else:
                silence_start = None  # reset silence timer

    audio = np.concatenate(frames)
    print("✅ Recording complete.")
    return audio
