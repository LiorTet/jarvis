import os

# Audio & Whisper settings
SAMPLE_RATE = 16000
DURATION = 5
MODEL_NAME = "base"

# Silence detection
CHUNK_DURATION = 0.5
SILENCE_THRESHOLD = 0.005
SILENCE_DURATION = 3.0
MIN_RECORDING_DURATION = 2.0

# Ollama
OLLAMA_PATH = r"C:\Users\Lior\AppData\Local\Programs\Ollama\ollama.exe"
OLLAMA_MODEL = "llama3.1:latest"  # phi3:mini
OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"


# Special words
EXIT_COMMANDS = {"exit", "quit", "shutdown", "stop", "bye"}

# Memory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
