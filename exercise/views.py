from django.shortcuts import render

# Create your views here.

def exercise_index(request):
    return render(request, 'exercise/exercise_index.html' )