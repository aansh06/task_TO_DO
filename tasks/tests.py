from django.test import TestCase
from django.urls import reverse
from .models import Task

class TaskListTests(TestCase):

    def setUp(self):
        """Create initial tasks for testing."""
        Task.objects.create(title="Task 1", due_date="2024-09-11", priority=1, status="To Do")
        Task.objects.create(title="Task 2", due_date="2024-09-12", priority=2, status="In Progress")
        Task.objects.create(title="Task 3", due_date="2024-09-13", priority=3, status="Done")

    def test_filter_by_status(self):
        """Test filtering tasks by status."""
        response = self.client.get(reverse('task_list') + '?status=To Do')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 1)

    def test_sort_by_priority(self):
        """Test sorting tasks by priority."""
        response = self.client.get(reverse('task_list') + '?sort_by=priority')
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(tasks[0].priority, 1)
        self.assertEqual(tasks[2].priority, 3)

    def test_sort_by_due_date(self):
        """Test sorting tasks by due date."""
        response = self.client.get(reverse('task_list') + '?sort_by=due_date')
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(tasks[0].due_date.strftime('%Y-%m-%d'), '2024-09-11')
        self.assertEqual(tasks[2].due_date.strftime('%Y-%m-%d'), '2024-09-13')

    def test_add_new_task(self):
        """Test adding a new task."""
        response = self.client.post(reverse('task_list'), {
            'title': 'New Task',
            'description': 'Test task description',
            'due_date': '2024-09-15',
            'priority': 2,
            'status': 'To Do'
        })
        self.assertEqual(Task.objects.count(), 4)
        new_task = Task.objects.last()
        self.assertEqual(new_task.title, 'New Task')
        self.assertEqual(new_task.due_date.strftime('%Y-%m-%d'), '2024-09-15')
