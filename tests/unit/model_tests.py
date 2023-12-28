import unittest
from src.models.task import Task
from src.models.sub_task import SubTask


class TestModels(unittest.TestCase):
    def test_add_subtask(self):
        task = create_task(1)
        sub_task1 = create_subtask(1)
        sub_task2 = create_subtask(2)
        sub_task3 = create_subtask(3)

        self.assertEqual(len(task.subtasks), 0)
        task.add_subtask(sub_task1)
        task.add_subtask(sub_task2)
        task.add_subtask(sub_task3)
        self.assertEqual(len(task.subtasks), 3)

    def test_remove_subtask(self):
        task = create_task(1)
        sub_task1 = create_subtask(1)
        sub_task2 = create_subtask(2)
        sub_task3 = create_subtask(3)

        task.add_subtask(sub_task1)
        task.add_subtask(sub_task2)
        task.add_subtask(sub_task3)

        task.remove_subtask(sub_task2.title)

        self.assertEqual(len(task.subtasks), 2)
        self.assertEqual(task.subtasks[0].title, sub_task1.title)
        self.assertEqual(task.subtasks[1].title, sub_task3.title)


def create_task(index):
    return Task(f"Test task {index}", f"Test task {index} description")


def create_subtask(index):
    return SubTask(f"Test subtask {index}", f"Test subtask {index} description")


if __name__ == '__main__':
    unittest.main()
