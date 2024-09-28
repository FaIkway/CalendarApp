# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Event, Task
from .forms import EventForm, TaskForm
from django.utils import timezone
import json

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    events = Event.objects.filter(user=request.user)
    return render(request, 'home.html', {'events': events})

@login_required
def add_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = EventForm(data)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            tasks = data.get('tasks', [])
            for task_data in tasks:
                Task.objects.create(
                    event=event,
                    description=task_data['description'],
                    completed=task_data['completed']
                )
            return JsonResponse({'status': 'success', 'event_id': event.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == 'POST':
        data = json.loads(request.body)
        form = EventForm(data, instance=event)
        if form.is_valid():
            form.save()
            # Delete existing tasks
            event.tasks.all().delete()
            # Add updated tasks
            tasks = data.get('tasks', [])
            for task_data in tasks:
                Task.objects.create(
                    event=event,
                    description=task_data['description'],
                    completed=task_data['completed']
                )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = EventForm(instance=event)
    return render(request, 'edit_event.html', {'form': form, 'event': event})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
