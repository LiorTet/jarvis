# jarvis/tools/tool_manager.py

import json
from .memory import Memory


class ToolManager:
    def __init__(self):
        self.memory = Memory()

    def process_response(self, response: str) -> str:
        """
        Analyze model response (expected to be JSON), decide if a tool needs to be used,
        update state accordingly, and return the text to speak.
        """
        try:
            response_json = json.loads(response)
            command = response_json.get("command")
            details = response_json.get("details")

            if command == "ADD_TASK":
                if details:
                    self.memory.add_task(details)
                    return f"Okay, I added: {details}"
                else:
                    return "I couldn't find a task to add. Please tell me what to add."

            elif command == "LIST_TASKS":
                tasks = self.memory.get_tasks()
                if tasks:
                    return "Here are your tasks: " + ", ".join(tasks)
                else:
                    return "You have no tasks."

            elif command == "UNRELATED":
                return f"I'm not sure how to help with that. You said: '{details}'"

            else:
                return "I received an unrecognised command from the model."

        except json.JSONDecodeError:
            return "I received an unreadable response from the model. It wasn't valid JSON."
        except Exception as e:
            return f"An error occurred while processing the model's response: {e}"
