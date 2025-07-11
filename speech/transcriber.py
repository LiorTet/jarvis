import whisper
import os
import warnings
from pathlib import Path
from .utils.whisper_utils import record_audio, save_audio_to_wav, transcribe_audio

warnings.filterwarnings(
    "ignore", message="FP16 is not supported on CPU; using FP32 instead"
)

SAMPLE_RATE = 16000
DURATION = 5
MODEL_NAME = "base"

# Dynamically build absolute path to ffmpeg/bin
CURRENT_DIR = Path(__file__).resolve().parent
FFMPEG_BIN_PATH = CURRENT_DIR / "ffmpeg" / "ffmpeg-7.1.1-essentials_build" / "bin"
os.environ["PATH"] += os.pathsep + str(FFMPEG_BIN_PATH)

model = whisper.load_model(MODEL_NAME)


def transcribe_from_mic() -> str:
    """
    Function to transcribe the audio. It records saves and transcribes.
    """
    audio = record_audio(DURATION, SAMPLE_RATE)
    audio_path = save_audio_to_wav(audio, SAMPLE_RATE)
    return transcribe_audio(audio_path, model)
