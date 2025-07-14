# jarvis/tools/tool_manager.py

from .memory import Memory


class ToolManager:
    def __init__(self):
        self.memory = Memory()

    def process_response(self, response: str) -> str:
        """
        Analyze model response, decide if a tool needs to be used,
        update state accordingly, and return the text to speak.
        """

        if response.startswith("TASK_ADDED:"):
            task = response.replace("TASK_ADDED:", "").strip()
            self.memory.add_task(task)
            return f"Okay, I added: {task}"

        elif response.startswith("TASK_LIST:"):
            tasks = self.memory.get_tasks()
            if tasks:
                return "Here are your tasks: " + ", ".join(tasks)
            else:
                return "You have no tasks."

        # Here you can add more tools, e.g. calendar, reminders, etc.

        # If no tool is invoked, just return the original response
        return response
