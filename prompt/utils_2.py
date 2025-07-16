COMMAND_INSTRUCTIONS = {
    "ADD_TASK": """
                The JSON object MUST have two keys: "task" (string) and "date" (string).
                The "date" key MUST ONLY be "today" or "tomorrow".
                - If the user explicitly mentions "tomorrow", the "date" MUST be "tomorrow".
                - Otherwise, the "date" MUST be "today".
                """,
    "LIST_TASKS": """
                The JSON object MUST have one key: "date" (string).
                The "date" key MUST ONLY be "today", "tomorrow", or "all".
                - If the user explicitly asks for "tomorrow", the "date" MUST be "tomorrow".
                - If the user explicitly asks for "all" tasks, the "date" MUST be "all".
                - Otherwise (e.g., "What do I have to do?"), the "date" MUST be "today".
                """,
    "CLEAR_TASKS": """
                The JSON object MUST have one key: "date" (string).
                The "date" key MUST ONLY be "today", "tomorrow", or "all".
                - If the user explicitly asks for "tomorrow", the "date" MUST be "tomorrow".
                - If the user explicitly asks to clear "all" tasks, the "date" MUST be "all".
                - Otherwise (e.g., "Clear my tasks"), the "date" MUST be "today".
                """,
    "UNRELATED": """
                Answer normally.
                """
    # Add other commands here as needed
    # "OTHER_COMMAND": "Instructions for OTHER_COMMAND..."
}

# Dictionary mapping command names to their specific examples for the LLM.
COMMAND_EXAMPLES = {
    "ADD_TASK": """
        ## Examples for ADD_TASK:

        User: Add 'buy milk' to my tasks.
        Assistant: {{"task": "buy milk", "date": "today"}}

        User: Add 'call mom' for tomorrow.
        Assistant: {{"task": "call mom", "date": "tomorrow"}}
    """,
    "LIST_TASKS": """
        ## Examples for LIST_TASKS:

        User: What do I have to do?
        Assistant: {{"date": "today"}}

        User: List my tasks for tomorrow.
        Assistant: {{"date": "tomorrow"}}

        User: Show me all my tasks.
        Assistant: {{"date": "all"}}
        """,
    "CLEAR_TASKS": """
        ## Examples for CLEAR_TASKS:

        User: Clear my tasks.
        Assistant: {{"date": "today"}}

        User: Clear my tasks for tomorrow.
        Assistant: {{"date": "tomorrow"}}

        User: Clear all my tasks.
        Assistant: {{"date": "all"}}
        """,
    # Add other commands here as needed
    # "OTHER_COMMAND": "Examples for OTHER_COMMAND..."
}
