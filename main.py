from .config import settings as cfg
from .agents import agent_task_classification
from .speech import speak, listen
from .tools import ToolManager, Memory, exit_cond
from .prompt import build_command_identification_prompt, build_task_execution_prompt
from .prompt import COMMAND_EXAMPLES, COMMAND_INSTRUCTIONS

from .schemas import IdentifiedCommand

import json
import re

EXIT_COMMANDS = cfg.EXIT_COMMANDS

# OLLAMA url
OLLAMA_BASE_URL = "http://127.0.0.1:11434"

if __name__ == "__main__":

    memory = Memory()
    
    tool_manager = ToolManager()

    agent = agent_task_classification(cfg.OLLAMA_MODEL, IdentifiedCommand)

    print("Jarvis is now running. Say something...")
    while True:
        try:
            # Listen
            text = ""
            text = listen()

            # Check for exit condition
            exit_value = exit_cond(text)
            if exit_value:
                break

            # Build prompt to define task and call agent
            prompt_identified_task = build_command_identification_prompt(text)
            result = agent.run_sync(prompt_identified_task)
            identified_command_obj: IdentifiedCommand = result.output
            task = identified_command_obj.command
            print(task)

            if task = "UNRELATED":
                print("Will return generic answer")
            else:
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
