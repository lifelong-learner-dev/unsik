from django.shortcuts import render

# Create your views here.

def meal_index(request):
    return render(request, 'meal/meal_index.html' )