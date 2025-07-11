# main.py
from speech.transcriber import transcribe_from_mic
from models.model import ask_ollama
from models.load_model import is_model_installed, install_model_if_needed
from speech.speaker import speak

if __name__ == "__main__":
    # Models installation
    install_model_if_needed("phi3:mini")

    # Hearing
    text = transcribe_from_mic()
    print("You said:", text)

    # Model response
    response = ask_ollama(text)

    # Answer
    if response:
        print("Ollama says:", response)
        speak(response)
