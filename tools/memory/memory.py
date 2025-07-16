import json
from datetime import datetime, timedelta, date
import os
from jarvis.config import settings as cfg
from jarvis.config import settings as cfg


class Memory:
    """
    Memory class for managing tasks with date associations, persisted to a JSON file.
    Tasks are stored as a dictionary where keys are date strings (YYYY-MM-DD)
    and values are lists of task strings for that date.
    """

    def __init__(self):
        # Construct the full path to the memory file using DATA_DIR from config
        self._memory_file = os.path.join(cfg.DATA_DIR, "tasks.json")
        self.tasks_by_date = {}  # Stores tasks: {'YYYY-MM-DD': ['task1', 'task2']}
        self._ensure_data_directory()
        self._load_tasks()

    def _ensure_data_directory(self):
        """Ensures the data directory exists."""
        os.makedirs(cfg.DATA_DIR, exist_ok=True)

    def _load_tasks(self):
        """Loads tasks from the JSON file."""
        if os.path.exists(self._memory_file):
            try:
                with open(self._memory_file, "r") as f:
                    self.tasks_by_date = json.load(f)
            except json.JSONDecodeError:
                print(
                    f"Warning: Could not decode JSON from {self._memory_file}. Starting with empty memory."
                )
                self.tasks_by_date = {}
            except Exception as e:
                print(
                    f"Error loading tasks from {self._memory_file}: {e}. Starting with empty memory."
                )
                self.tasks_by_date = {}
        else:
            print(
                f"No memory file found at {self._memory_file}. Starting with empty memory."
            )
            self.tasks_by_date = {}

    def _save_tasks(self):
        """Saves current tasks to the JSON file."""
        with open(self._memory_file, "w") as f:
            json.dump(self.tasks_by_date, f, indent=4)  # Use indent for readability

    def add_task(self, task: str, target_date: date = None):
        """
        Adds a task for a specific date. If no date is provided, it defaults to today.
        :param task: The task string.
        :param target_date: A datetime.date object for the task's date.
        """
        if target_date is None:
            target_date = date.today()

        date_str = target_date.isoformat()  # Convert date to 'YYYY-MM-DD' string

        if date_str not in self.tasks_by_date:
            self.tasks_by_date[date_str] = []
        self.tasks_by_date[date_str].append(task)
        self._save_tasks()  # Save after adding

    def get_tasks(self, target_date: date = None):
        """
        Retrieves tasks for a specific date. If no date is provided, it defaults to today.
        :param target_date: A datetime.date object for the tasks' date.
        :return: A list of tasks for the given date, or an empty list if none.
        """
        if target_date is None:
            target_date = date.today()

        date_str = target_date.isoformat()
        return self.tasks_by_date.get(
            date_str, []
        ).copy()  # Return a copy to prevent external modification

    def get_tasks_for_display(self):
        """
        Retrieves all tasks sorted by date for display purposes in the prompt.
        Focuses on upcoming tasks (today, tomorrow, and future).
        """
        all_tasks = []
        today = date.today()

        # Sort dates to display them chronologically
        sorted_dates = sorted(self.tasks_by_date.keys())

        for date_str in sorted_dates:
            task_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Only include tasks from today onwards for context in the prompt
            if task_date >= today:
                date_label = ""
                if task_date == today:
                    date_label = "Today"
                elif task_date == today + timedelta(days=1):
                    date_label = "Tomorrow"
                else:
                    date_label = task_date.strftime(
                        "%A, %B %d, %Y"
                    )  # e.g., Tuesday, July 15, 2025

                tasks_on_date = self.tasks_by_date[date_str]
                if tasks_on_date:
                    all_tasks.append(f"On {date_label}:")
                    for task in tasks_on_date:
                        all_tasks.append(f"- {task}")
        return "\n".join(all_tasks) if all_tasks else "None"

    def clear_tasks(self, target_date: date = None):
        """
        Clears tasks for a specific date. If no date is provided, clears today's tasks.
        If target_date is 'all', clears all tasks from all dates.
        """
        if target_date == "all":
            self.tasks_by_date = {}
            self._save_tasks()
            return

        if target_date is None:
            target_date = date.today()

        date_str = target_date.isoformat()
        if date_str in self.tasks_by_date:
            del self.tasks_by_date[date_str]
            self._save_tasks()  # Save after clearing

    def __str__(self):
        """
        Returns a string representation of the tasks for the prompt.
        This is what the LLM will see.
        """
        return self.get_tasks_for_display()
