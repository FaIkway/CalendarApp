# forms.py

from django import forms
from django.utils import timezone
from .models import Event, Task

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start', 'end', 'color', 'importance']
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'importance': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_start(self):
        start = self.cleaned_data['start']
        if timezone.is_naive(start):
            return timezone.make_aware(start)
        return start

    def clean_end(self):
        end = self.cleaned_data['end']
        if timezone.is_naive(end):
            return timezone.make_aware(end)
        return end

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'completed']
