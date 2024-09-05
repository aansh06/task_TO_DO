from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()

    # Filtering by status
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    # Sorting by priority or due date
    sort_by = request.GET.get('sort_by')
    if sort_by == 'priority':
        tasks = tasks.order_by('priority')
    elif sort_by == 'due_date':
        tasks = tasks.order_by('due_date')

    # Handle form submission
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to task list after adding new task
    else:
        form = TaskForm()

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})
