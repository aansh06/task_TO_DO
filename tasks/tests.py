from django.test import TestCase
from .models import Task

class TaskListTests(TestCase):

    def setUp(self):
        Task.objects.create(title="Task 1", due_date="2024-09-11", priority=1, status="To Do")
        Task.objects.create(title="Task 2", due_date="2024-09-12", priority=2, status="In Progress")
        Task.objects.create(title="Task 3", due_date="2024-09-13", priority=3, status="Done")

    def test_filter_by_status(self):
        response = self.client.get('/tasks/?status=To Do')
        self.assertEqual(len(response.context['tasks']), 1)

    def test_sort_by_priority(self):
        response = self.client.get('/tasks/?sort_by=priority')
        tasks = response.context['tasks']
        self.assertEqual(tasks[0].priority, 1)
        self.assertEqual(tasks[2].priority, 3)

    def test_sort_by_due_date(self):
        response = self.client.get('/tasks/?sort_by=due_date')
        tasks = response.context['tasks']
        self.assertEqual(tasks[0].due_date, '2024-09-10')
        self.assertEqual(tasks[2].due_date, '2024-09-20')

    def test_add_new_task(self):
        response = self.client.post('/tasks/', {
            'title': 'New Task',
            'description': 'Test task description',
            'due_date': '2024-09-15',
            'priority': 2,
            'status': 'To Do'
        })
        self.assertEqual(Task.objects.count(), 4)
        self.assertEqual(Task.objects.first().title, 'New Task')
