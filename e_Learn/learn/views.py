from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')
def lesson(request):
    return render(request, 'lesson.html')