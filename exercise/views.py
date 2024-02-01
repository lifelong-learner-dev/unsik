from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Exercise, UsersAppUser
from .forms import ExerciseForm  # ExerciseForm은 ModelForm을 사용하여 정의
from django.http import JsonResponse
from django.utils import timezone
from django.db import connection
import datetime

# def exercise_index(request):
    
#     return render(request, 'exercise/exercise_index.html' )

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
def get_exercises_for_date(request, date):
# def get_exercises_for_date(request):
    print(date)
    user_instance = UsersAppUser.objects.get(id=request.user.id)
    # 날짜 문자열을 datetime 객체로 변환
    date_obj = timezone.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").date()
    exercises = Exercise.objects.filter(user=user_instance, exercise_date__date=date_obj)
    data = list(exercises.values('exercise_date', 'exercise_type', 'exercise_name', 'exercise_amount', 'calories_burned', 'weight', 'reps', 'sets'))
    return JsonResponse(data, safe=False)

# @login_required
# def exercise_index(request):
#     # 현재 로그인한 사용자의 운동 정보만 조회
#     user_instance = UsersAppUser.objects.get(id=request.user.id)
#     exercises = Exercise.objects.filter(user=user_instance).order_by('exercise_date')

#     if request.method == "POST":
#         search_date = request.POST.get('search_date')

#         if search_date:
#             search_date = datetime.datetime.strptime(search_date, '%Y-%m-%d').date()
#             exercises = Exercise.objects.filter(user=user_instance, exercise_date__date=search_date)

#         else:
#             exercises = Exercise.objects.none()

#     return render(request, 'exercise/exercise_index.html', {'exercises': exercises})

@login_required
def exercise_index(request):
    user_instance = UsersAppUser.objects.get(id=request.user.id)

    # 현재 날짜를 naive datetime 객체로 가져오기
    today = datetime.date.today()

    if request.method == "POST":
        search_date = request.POST.get('search_date')

        if search_date:
            search_date = datetime.datetime.strptime(search_date, '%Y-%m-%d').date()
            exercises = Exercise.objects.filter(user=user_instance, exercise_date__date=search_date)
        else:
            exercises = Exercise.objects.none()
    else:
        # 처음 페이지에 접속했거나 GET 요청인 경우 오늘 날짜의 운동 기록을 보여줌
        exercises = Exercise.objects.filter(user=user_instance, exercise_date__date=today).order_by('exercise_date')

    return render(request, 'exercise/exercise_index.html', {'exercises': exercises, 'today': today})