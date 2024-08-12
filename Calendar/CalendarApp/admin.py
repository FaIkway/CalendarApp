from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Event

# Rejestracja modelu Event w adminie
admin.site.register(Event)
