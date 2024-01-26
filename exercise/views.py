from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Exercise, UsersAppUser
from .forms import ExerciseForm  # ExerciseForm은 ModelForm을 사용하여 정의
# Create your views here.

def exercise_index(request):
    return render(request, 'exercise/exercise_index.html' )

@login_required
def record_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            # request.user 대신에 UsersAppUser 모델의 인스턴스를 가져옴
            user_instance = UsersAppUser.objects.get(id=request.user.id)
            exercise.user = user_instance  # UsersAppUser 모델의 인스턴스를 할당
            exercise.save()
            return redirect('exercise_index')  # 이동할 URL 이름을 수정
    else:
        form = ExerciseForm()

    return render(request, 'exercise/exercise_form.html', {'form': form})