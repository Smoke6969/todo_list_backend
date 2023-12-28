import json

from src.models.sub_task import SubTask
from src.models.task import Task


class JsonLoader:

    def __init__(self, file_path):
        self.file_path = file_path

    def load_tasks(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            tasks = []
            for task_data in data:
                task = Task(task_data['title'], task_data['description'], task_data.get('due_date'))
                for subtask_data in task_data['subtasks']:
                    subtask = SubTask(subtask_data['title'], subtask_data.get('due_date'))
                    task.add_subtask(subtask)
                tasks.append(task)
            return tasks

    def save_tasks(self, tasks):
        def default_converter(o):
            return o.__dict__

        with open(self.file_path, 'w') as file:
            json.dump(tasks, file, default=default_converter, indent=4)
