from django import forms
from django.utils import timezone
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start', 'end']
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def clean_start(self):
        start = self.cleaned_data['start']
        # Jeśli datetime jest "naive", zamieniamy na "aware"
        if timezone.is_naive(start):
            return timezone.make_aware(start)
        return start  # Jeśli datetime jest już "aware", zwracamy go bez zmian

    def clean_end(self):
        end = self.cleaned_data['end']
        # Jeśli datetime jest "naive", zamieniamy na "aware"
        if timezone.is_naive(end):
            return timezone.make_aware(end)
        return end  # Jeśli datetime jest już "aware", zwracamy go bez zmian
