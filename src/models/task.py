class Task:
    def __init__(self, title, description, due_date=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = False
        self.subtasks = []

    def add_subtask(self, subtask):
        self.subtasks.append(subtask)

    def remove_subtask(self, title):
        self.subtasks = [subtask for subtask in self.subtasks if subtask.title != title]

    def mark_completed(self):
        self.completed = True
