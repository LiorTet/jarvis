# main.py
from jarvis.config import settings as cfg
from .speech import transcribe_from_mic
from .models import ask_ollama
from .models import is_model_installed, install_model_if_needed
from .speech import speak


if __name__ == "__main__":
    # Models installation
    install_model_if_needed(cfg.OLLAMA_MODEL)

    # Hearing
    text = transcribe_from_mic()
    print("You said:", text)

    # Model response
    response = ask_ollama(text)

    # Answer
    if response:
        print("Ollama says:", response)
        speak(response)
