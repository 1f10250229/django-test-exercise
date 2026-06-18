from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from todo.models import Task

# Create your tests here.


class SampleTestCase(TestCase):
    def test_sample1(self):
        self.assertEqual(1 + 2, 3)


class TaskModelTestCase(TestCase):
    def test_create_task1(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        task = Task(title='task1', due_at=due)
        task.save()

        self.assertEqual(task.title, 'task1')
        self.assertFalse(task.completed)
        self.assertLessEqual(task.posted_at, timezone.now())
        self.assertEqual(task.due_at, due)

    def test_create_task2(self):
        task = Task(title='task2')
        task.save()

        self.assertEqual(task.title, 'task2')
        self.assertFalse(task.completed)
        self.assertLessEqual(task.posted_at, timezone.now())
        self.assertIsNone(task.due_at)

    def test_is_overdue_future(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        task = Task(title='task1', due_at=due)
        dt = timezone.make_aware(datetime(2024, 6, 30, 0, 0, 0))
        self.assertFalse(task.is_overdue(dt))

    def test_is_overdue_past(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        task = Task(title='task1', due_at=due)
        dt = timezone.make_aware(datetime(2024, 7, 1, 0, 0, 0))
        self.assertTrue(task.is_overdue(dt))

    def test_is_overdue_none(self):
        task = Task(title='task2')
        dt = timezone.make_aware(datetime(2024, 7, 1, 0, 0, 0))
        self.assertFalse(task.is_overdue(dt))
