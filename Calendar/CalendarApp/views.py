# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def home(request):
    return render(request, 'home.html')


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
    if request.method == 'POST':
        logout(request)
        return redirect('login')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm
from django.utils import timezone

@login_required
def home(request):
    events = Event.objects.filter(user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            print(f"Wydarzenie dodane: {event.title}, {event.start}, {event.end}")  # Debugowanie
            return redirect('home')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = EventForm()
    return render(request, 'home.html', {'events': events, 'form': form})


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})
