import os
import json
import unittest
from todo import load_tasks, save_tasks, add_task, list_tasks, complete_task, delete_task

TEST_FILE = "test_tasks.json"


class TestTodoManager(unittest.TestCase):

    def setUp(self):
        """Ensure clean state before each test."""
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def tearDown(self):
        """Clean up test file after test."""
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def test_add_task(self):
        tasks = []
        result = add_task(tasks, "Buy groceries", category="Personal", priority="High", filepath=TEST_FILE)
        self.assertTrue(result)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], 1)
        self.assertEqual(tasks[0]["title"], "Buy groceries")
        self.assertEqual(tasks[0]["category"], "Personal")
        self.assertEqual(tasks[0]["priority"], "High")
        self.assertFalse(tasks[0]["completed"])

    def test_add_empty_task_fails(self):
        tasks = []
        result = add_task(tasks, "   ", filepath=TEST_FILE)
        self.assertFalse(result)
        self.assertEqual(len(tasks), 0)

    def test_complete_task(self):
        tasks = []
        add_task(tasks, "Read a book", filepath=TEST_FILE)
        self.assertFalse(tasks[0]["completed"])

        success = complete_task(tasks, 1, filepath=TEST_FILE)
        self.assertTrue(success)
        self.assertTrue(tasks[0]["completed"])

    def test_delete_task(self):
        tasks = []
        add_task(tasks, "Task 1", filepath=TEST_FILE)
        add_task(tasks, "Task 2", filepath=TEST_FILE)
        self.assertEqual(len(tasks), 2)

        success = delete_task(tasks, 1, filepath=TEST_FILE)
        self.assertTrue(success)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], 2)

    def test_load_and_save_tasks(self):
        tasks = [{"id": 1, "title": "Persistent Task", "category": "Work", "priority": "Low", "completed": False}]
        save_tasks(tasks, TEST_FILE)

        loaded = load_tasks(TEST_FILE)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["title"], "Persistent Task")


if __name__ == "__main__":
    unittest.main()
