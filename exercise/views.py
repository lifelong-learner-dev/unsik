from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Exercise, UsersAppUser
from .forms import ExerciseForm  # ExerciseForm은 ModelForm을 사용하여 정의
from django.http import JsonResponse

# def exercise_index(request):
    
#     return render(request, 'exercise/exercise_index.html' )

@login_required
def exercise_index(request):
    # 현재 로그인한 사용자의 운동 정보만 조회
    user_instance = UsersAppUser.objects.get(id=request.user.id)
    exercises = Exercise.objects.filter(user=user_instance).order_by('exercise_date')

    return render(request, 'exercise/exercise_index.html', {'exercises': exercises})

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

@login_required
def get_exercises_for_date(request, year, month, day):
    user_instance = UsersAppUser.objects.get(id=request.user.id)
    date = f"{year}-{month}-{day}"
    exercises = Exercise.objects.filter(user=user_instance, exercise_date=date)
    data = list(exercises.values('exercise_date', 'exercise_type', 'exercise_name', 'exercise_amount', 'calories_burned', 'weight', 'reps', 'sets'))  # 필요한 필드 나열
    return JsonResponse(data, safe=False)