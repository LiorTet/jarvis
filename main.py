from jarvis.config import settings as cfg
from .speech import transcribe_from_mic
from .models import is_model_installed, install_model_if_needed, ask_ollama
from .speech import speak
from .tools import ToolManager, Memory
from .prompt import build_command_identification_prompt, build_task_execution_prompt
from .prompt import COMMAND_EXAMPLES, COMMAND_INSTRUCTIONS

from pydantic_ai import extract
from .schemas import IdentifiedCommand

import json
import re

EXIT_COMMANDS = cfg.EXIT_COMMANDS


def extract_first_json(response: str):
    """
    Extracts the first valid JSON object from the LLM response.
    Works even if extra text or reasoning is present.
    """
    match = re.search(r"\{.*?\}", response, re.DOTALL)
    if match:
        return match.group(0)
    raise ValueError(f"No JSON object found in response: {response}")


if __name__ == "__main__":
    # Models installation
    install_model_if_needed(cfg.OLLAMA_MODEL)

    memory = Memory()
    tool_manager = ToolManager()

    print("Jarvis is now running. Say something...")
    while True:
        try:
            # Listen
            text = ""
            while not text.strip():
                print("Waiting for valid speech input...")
                text = transcribe_from_mic().strip()

            print("You said:", text)

            # Check for exit condition
            cleaned_text = text.lower().strip()
            if any(re.search(rf"\b{kw}\b", cleaned_text) for kw in EXIT_COMMANDS):
                print("Exiting Jarvis. Goodbye!")
                speak("Goodbye!")
                break

            # Build prompt to define task
            prompt_identified_task = build_command_identification_prompt(text)

            # Get model response to which task
            json_identified_task = ask_ollama(prompt_identified_task)

            # Execute task prompt
            print(json_identified_task)
            try:
                identified_command_obj: IdentifiedCommand = extract(
                    text=json_identified_task, 
                    model=IdentifiedCommand
                )
                # Access the validated command directly
                task = identified_command_obj.command 

            except Exception as e:
                print(f"Error parsing identified command with PydanticAI: {e}")
                speak("I couldn't understand what task you wanted. Please try again.")
                continue # Skip to next loop iteration


            prompt_execute_task = build_task_execution_prompt(
                text,
                json.loads(json_identified_task)["command"],
                memory,
                COMMAND_INSTRUCTIONS[task],
                COMMAND_EXAMPLES[task],
            )

            # Get model response to execute task
            json_execute_task = ask_ollama(prompt_execute_task)

            print(json_execute_task)

            # Let tool manager handle external tools (including JSON parsing)
            # final_output = tool_manager.process_response(full_prompt)

            if json_execute_task:
                print("Jarvis says:", json_execute_task)
                speak(json_execute_task)

        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            speak("I encountered an unexpected error. Please try again.")
