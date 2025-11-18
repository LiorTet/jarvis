# jarvis/prompt.py
import json
from datetime import date, timedelta
from jarvis.schemas import IdentifiedCommand

# Helper for current date context (still useful for examples in the second prompt later)
today_dt = date.today()
tomorrow_dt = today_dt + timedelta(days=1)

IDENTIFICATION_SCHEMA = IdentifiedCommand.schema_json(indent=2)


def build_command_identification_prompt(user_input: str) -> str:
    """
    Builds a prompt for the LLM to identify the high-level command from user input.
    The LLM's ONLY job is to output a JSON object matching the IdentifiedCommand schema.
    """
    system_prompt = f"""
        You are a command identifier AI. Your ONLY job is to analyze the user's text and determine the high-level command.
        
        **CRITICAL INSTRUCTION**: Your output MUST be a single JSON object that strictly conforms to the JSON schema provided below.
        
        Do NOT add any explanations, introductory text, or any text whatsoever outside of the JSON object. 
        Do NOT use markdown (e.g., ```json) around the JSON.

        ## JSON Schema to Follow:
        {IDENTIFICATION_SCHEMA}

        ## Valid 'command' values:
        - "ADD_TASK"
        - "LIST_TASKS"
        - "CLEAR_TASKS"
        - "UNRELATED"

        ## Examples:

        User: Add 'buy milk' to my tasks.
        Assistant: {{"command": "ADD_TASK"}}

        User: What do I have to do?
        Assistant: {{"command": "LIST_TASKS"}}

        User: what is the capital of Spain
        Assistant: {{"command": "UNRELATED"}}

        ## User Input to Process:
        User: {user_input}
        Assistant:
        """
    return system_prompt.strip()


def build_task_execution_prompt(
    user_input: str,
    identified_command: str,
    memory_context: str,
    command_specific_instructions: str,
    command_specific_examples: str,
) -> str:
    """
    Builds a prompt for the LLM to extract details for a specific command,
    using a skeleton structure and injecting command-specific content.

    :param user_input: The original user's text.
    :param identified_command: The command identified in the first step (e.g., "ADD_TASK").
    :param memory_context: The string representation of the current memory/task list.
    :param command_specific_instructions: Detailed instructions for the LLM on what keys to output.
    :param command_specific_examples: Examples for the LLM for this specific command.
    """
    general_instructions = f"""
        You are an AI that extracts specific details for a command. Your ONLY job is to analyze the user's text
        and convert it into a SINGLE, specific JSON object containing ONLY the details for the "{identified_command}" command.
        Do NOT add any explanations, introductory text, or any text whatsoever outside of the JSON object.

        Your output MUST be a single JSON object.
        """

    full_prompt = f"""
        {general_instructions.strip()}

        {command_specific_instructions.strip()}

        {command_specific_examples.strip()}

        ## Current Task List (for context only):
        {memory_context}

        ## User Input to Extract Details From:
        User: {user_input}
        Assistant:
    """
    return full_prompt.strip()