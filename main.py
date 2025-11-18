from .config import settings as cfg
from .models import is_model_installed, install_model_if_needed, ask_ollama
from .speech import speak, listen
from .tools import ToolManager, Memory, exit_cond
from .prompt import build_command_identification_prompt, build_task_execution_prompt
from .prompt import COMMAND_EXAMPLES, COMMAND_INSTRUCTIONS

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai import Agent
from .schemas import IdentifiedCommand

import json
import re

EXIT_COMMANDS = cfg.EXIT_COMMANDS

# OLLAMA url
OLLAMA_BASE_URL="http://127.0.0.1:11434"

if __name__ == "__main__":
    # Models installation
    #install_model_if_needed(cfg.OLLAMA_MODEL)

    memory = Memory()
    tool_manager = ToolManager()

    ollama_model = OpenAIChatModel(
        model_name=cfg.OLLAMA_MODEL,
        provider=OllamaProvider(base_url="http://127.0.0.1:11434/v1"),
    )

    agent = Agent(
        ollama_model,
        output_type=IdentifiedCommand,
        system_prompt="Use the following schema to decide which command to run.",
    )

    print("Jarvis is now running. Say something...")
    while True:
        try:
            # Listen
            text = listen()

            # Check for exit condition
            exit_value = exit_cond()
            if exit_value:
                break

            # Build prompt to define task
            prompt_identified_task = build_command_identification_prompt(text)

            result = agent.run_sync(prompt_identified_task)

            # `result.data` is now an instance of IdentifiedCommand, validated
            identified_command_obj: IdentifiedCommand = result.data
            task = identified_command_obj.command

            prompt_execute_task = build_task_execution_prompt(
                text,
                task,
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
