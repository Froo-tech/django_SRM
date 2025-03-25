from django.shortcuts import render

def task(request):
    return render(request, 'sr/task.html')

def index(request):
    return render(request, "sr/index.html")