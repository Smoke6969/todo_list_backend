class SubTask:
    def __init__(self, title, description=None, due_date=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = False

    def mark_completed(self):
        self.completed = True

