from django.shortcuts import render, redirect
from .models import Exercise
from .forms import ExerciseForm  # ExerciseForm은 ModelForm을 사용하여 정의
# Create your views here.

def exercise_index(request):
    return render(request, 'exercise/exercise_index.html' )

def record_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # 성공 시 리디렉션할 페이지
    else:
        form = ExerciseForm()

    return render(request, 'exercise/record.html', {'form': form})