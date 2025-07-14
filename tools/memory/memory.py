class Memory:
    """
    Memory class for tasks at this point.
    """

    def __init__(self):
        self.tasks = []

    def add_task(self, task: str):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks.copy()

    def clear_tasks(self):
        self.tasks.clear()

    def __str__(self):
        if not self.tasks:
            return "None"
        return "\n".join(f"- {task}" for task in self.tasks)
