"""
To-do-list Project: Created a simple CMD style task manager to further our understanding of object oriented programming.
"""

import sys
import os
import json


TASK_FILE = "tasks.json"


class Task:
    """Represents a standard task."""

    def __init__(self, title, completed=False):
        """
        Initialize a new task.

        Args:
            title (str): The title or description of the task.
            completed (bool, optional): The completion status of the task.
                Defaults to False.
        """
        self.title = title
        self.completed = completed

    @staticmethod
    def from_dict(data):
        """
        Create a Task or UrgentTask object from a dictionary.

        Args:
            data (dict): A dictionary containing task data.

        Returns:
            Task: A Task or UrgentTask instance based on the
                provided data.
        """
        if data.get("type") == "Urgent":
            return UrgentTask(data["title"], data["completed"])
        return Task(data["title"], data["completed"])

    def to_dict(self):
        """
        Convert the task to a dictionary representation.

        Returns:
            dict: The dictionary representation of the task.
        """
        return {
            "title": self.title,
            "completed": self.completed,
            "type": "Normal"
        }

    def mark_complete(self):
        """Mark the task as completed."""
        self.completed = True

    def __str__(self):
        """
        Return a string representation of the task.

        Returns:
            str: The task string formatted with its completion status.
        """
        status = "X" if self.completed else " "
        return f"[{status}] {self.title}"


class UrgentTask(Task):
    """Represents an urgent task, which is a specialized type of Task."""

    def __str__(self):
        """
        Return a string representation of the urgent task.

        Returns:
            str: The urgent task string formatted with its completion status.
        """
        status = "X" if self.completed else " "
        return f"[{status}]! {self.title} (Urgent)"

    def to_dict(self):
        """
        Convert the urgent task to a dictionary representation.

        Returns:
            dict: The dictionary representation of the urgent task.
        """
        return {
            "title": self.title,
            "completed": self.completed,
            "type": "Urgent"
        }


class TaskManager:
    """Manages a collection of tasks, saving and loading from a file."""

    def __init__(self):
        """Initialize the TaskManager and load existing tasks."""
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """
        Load tasks from the JSON storage file.

        Returns:
            list: A list of Task and UrgentTask objects.
        """
        if not os.path.exists(TASK_FILE):
            return []
        with open(TASK_FILE, "r") as file:
            data = json.load(file)
        return [Task.from_dict(item) for item in data]

    def save_tasks(self):
        """Save the current list of tasks to the JSON storage file."""
        with open(TASK_FILE, "w") as file:
            tasks_data = [task.to_dict() for task in self.tasks]
            json.dump(tasks_data, file, indent=4)

    def add_task(self, title, urgent=False):
        """
        Add a new task to the manager.

        Args:
            title (str): The title of the task.
            urgent (bool, optional): Whether the task is urgent.
                Defaults to False.
        """
        if urgent:
            self.tasks.append(UrgentTask(title))
        else:
            self.tasks.append(Task(title))
        self.save_tasks()
        print(f'Task "{title}" added.')

    def view_tasks(self):
        """Display all tasks to the console."""
        if not self.tasks:
            print("No tasks found")
            return
        for i, task in enumerate(self.tasks, start=1):
            print(f"{i}. {task}")

    def complete_task(self, index):
        """
        Mark a task as complete by its 1-based index.

        Args:
            index (int): The 1-based index of the task to complete.
        """
        if 1 <= index <= len(self.tasks):
            self.tasks[index - 1].mark_complete()
            self.save_tasks()
            print("Task completed")
        else:
            print("Invalid task number")

    def delete_task(self, index):
        """
        Delete a task by its 1-based index.

        Args:
            index (int): The 1-based index of the task to delete.
        """
        if 1 <= index <= len(self.tasks):
            removed = self.tasks.pop(index - 1)
            self.save_tasks()
            print(f'Task "{removed.title}" deleted.')
        else:
            print("Invalid task number")


def main():
    """Run the main interactive command-line loop."""
    manager = TaskManager()
    while True:
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Quit")
        
        choice = input("Choice: ").strip()
        
        if choice == "1":
            title = input("Task title: ").strip()
            urgent = input("Urgent? (y/n): ").strip().lower()
            while urgent not in ("y", "n", "Y", "N"):
                print("Please enter a valid value")
                urgent = input("Urgent? (y/n): ").strip().lower()
            urgent = urgent == "y"
            manager.add_task(title, urgent)
        elif choice == "2":
            manager.view_tasks()
        elif choice == "3":
            manager.view_tasks()
            if manager.tasks:
                try:
                    number = int(input("Task number: "))
                    manager.complete_task(number)
                except ValueError:
                    print("Invalid task number")
        elif choice == "4":
            manager.view_tasks()
            if manager.tasks:
                try:
                    number = int(input("Task number: "))
                    manager.delete_task(number)
                except ValueError:
                    print("Invalid task number")
        elif choice == "5":
            print("GOODBYE!!!")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
