from jarvis.config import settings as cfg
from .speech import transcribe_from_mic
from .models import is_model_installed, install_model_if_needed, ask_ollama
from .speech import speak
from .tools import ToolManager, Memory
from .prompt import build_prompt

import re

EXIT_COMMANDS = cfg.EXIT_COMMANDS

if __name__ == "__main__":
    # Models installation
    install_model_if_needed(cfg.OLLAMA_MODEL)

    memory = Memory()
    tool_manager = ToolManager()

    print("🤖 Jarvis is now running. Say something...")
    while True:
        try:
            # Listen
            text = ""
            while not text.strip():
                print("🎧 Waiting for valid speech input...")
                text = transcribe_from_mic().strip()

            print("You said:", text)

            # Check for exit condition
            cleaned_text = text.lower().strip()
            if any(re.search(rf"\b{kw}\b", cleaned_text) for kw in EXIT_COMMANDS):
                print("👋 Exiting Jarvis. Goodbye!")
                speak("Goodbye!")
                break

            # Preprocessing the request
            full_prompt = build_prompt(text, memory)

            print(full_prompt)

            # Get model response
            response = ask_ollama(text)

            # Let tool manager handle external tools
            final_output = tool_manager.process_response(response)

            if final_output:
                print("Jarvis says:", final_output)
                speak(final_output)

        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user.")
            break
