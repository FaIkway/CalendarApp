# models.py

from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    COLOR_CHOICES = [
        ('red', 'Czerwony'),
        ('blue', 'Niebieski'),
        ('green', 'Zielony'),
        ('orange', 'Pomarańczowy'),
        ('purple', 'Fioletowy'),
        ('yellow', 'Żółty'),
        ('gray', 'Grafitowy'),
    ]

    IMPORTANCE_CHOICES = [
        ('lime', 'Ważne (Limonkowy)'),
        ('cyan', 'Średnie (Cyjan)'),
        ('pink', 'Mało ważne (Różowy)'),
        ('', 'Standardowy (Grafitowy)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='blue')
    importance = models.CharField(max_length=10, choices=IMPORTANCE_CHOICES, default='cyan')

    def __str__(self):
        return self.title

class Task(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tasks')
    description = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.description
