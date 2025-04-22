from django.shortcuts import render

def index(request):
    return render(request, 'sr/index.html')
def tasks(request):
    return render(request, 'sr/task.html')