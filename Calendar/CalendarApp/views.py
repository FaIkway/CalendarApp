from django.shortcuts import render, HttpResponse

# Create your views here.
def home(reguest):
    return HttpResponse('Hello World')