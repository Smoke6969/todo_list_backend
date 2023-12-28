import unittest
import os

from src.database.json_loader import JsonLoader
from tests.unit.model_tests import create_task
from tests.unit.model_tests import create_subtask


class TestDb(unittest.TestCase):
    def test_save_load_tasks(self):
        loader = JsonLoader("../../data/tasks.json")
        tasks = create_default_tasks()

        loader.save_tasks(tasks)

        tasks = loader.load_tasks()

        self.assertEqual(len(tasks[0].subtasks), 3)
        self.assertEqual(len(tasks[1].subtasks), 4)

        self.assertEqual(tasks[0].title, "Test task 1")
        self.assertEqual(tasks[1].subtasks[2].title, "Test subtask 2-3")


def create_default_tasks():
    tasks = []

    task1 = create_task("1")
    subtask11 = create_subtask("1-1")
    subtask12 = create_subtask("1-2")
    subtask13 = create_subtask("1-3")
    task1.subtasks.append(subtask11)
    task1.subtasks.append(subtask12)
    task1.subtasks.append(subtask13)

    task2 = create_task("2")
    subtask21 = create_subtask("2-1")
    subtask22 = create_subtask("2-2")
    subtask23 = create_subtask("2-3")
    subtask24 = create_subtask("2-4")
    task2.subtasks.append(subtask21)
    task2.subtasks.append(subtask22)
    task2.subtasks.append(subtask23)
    task2.subtasks.append(subtask24)

    tasks.append(task1)
    tasks.append(task2)

    return tasks


if __name__ == '__main__':
    unittest.main()
