from src.database.json_loader import JsonLoader


class TasksController:
    def __init__(self, file_path):
        self.json_loader = JsonLoader(file_path)
        self.tasks = self.json_loader.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.json_loader.save_tasks(self.tasks)

    def remove_task(self, title):
        self.tasks = [task for task in self.tasks if task.title != title]
        self.json_loader.save_tasks(self.tasks)

    def edit_task(self, original_title, new_title=None, new_description=None, new_due_date=None):
        for task in self.tasks:
            if task.title == original_title:
                if new_title is not None:
                    task.title = new_title
                if new_description is not None:
                    task.description = new_description
                if new_due_date is not None:
                    task.due_date = new_due_date
                self.json_loader.save_tasks(self.tasks)
                break
