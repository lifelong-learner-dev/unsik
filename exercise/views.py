from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Exercise, UsersAppUser
from .forms import ExerciseForm  # ExerciseForm은 ModelForm을 사용하여 정의
from django.http import JsonResponse
from django.utils import timezone
from django.db import connection
from django.db.models import Sum
from django.db.models.functions import TruncDay
from datetime import datetime, date
from django.views.decorators.csrf import csrf_exempt
from .apps import ExerciseConfig
from .moduls.data_anal import calories_model_load
from django.core.exceptions import ObjectDoesNotExist
import json
import pandas as pd

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

# 기존의 index페이지 views.py 함수
# @login_required
# def exercise_index(request):
#     user_instance = UsersAppUser.objects.get(id=request.user.id)

#     # 현재 날짜를 naive datetime 객체로 가져오기
#     today = datetime.date.today()

#     if request.method == "POST":
#         search_date = request.POST.get('search_date')

#         if search_date:
#             search_date = datetime.datetime.strptime(search_date, '%Y-%m-%d').date()
#             exercises = Exercise.objects.filter(user=user_instance, exercise_date__date=search_date)
#         else:
#             exercises = Exercise.objects.none()
#     else:
#         # 처음 페이지에 접속했거나 GET 요청인 경우 오늘 날짜의 운동 기록을 보여줌
#         exercises = Exercise.objects.filter(user=user_instance, exercise_date__date=today).order_by('exercise_date')

#     return render(request, 'exercise/exercise_index.html', {'exercises': exercises, 'today': today})

@login_required
def exercise_index(request):
    user_instance = UsersAppUser.objects.get(id=request.user.id)
    today = date.today()

    if request.method == "POST":
        search_date = request.POST.get('search_date')
        if search_date:
            search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
            exercises = Exercise.objects.filter(user=user_instance, exercise_date__date=search_date)
        else:
            exercises = Exercise.objects.none()
    else:
        exercises = Exercise.objects.filter(user=user_instance, exercise_date__date=today).order_by('exercise_date')

    # 날짜별로 칼로리 합계를 계산
    calorie_data = Exercise.objects.filter(user=user_instance).annotate(date=TruncDay('exercise_date')).values('date').annotate(total_calories=Sum('calories_burned')).order_by('date')
    dates = [data['date'].strftime("%Y-%m-%d") for data in calorie_data]
    calories = [data['total_calories'] for data in calorie_data]

    return render(request, 'exercise/exercise_index.html', {
        'exercises': exercises, 
        'today': today,
        'dates': dates, 
        'calories': calories
    })

@login_required
def exercise_edit(request, id):
    exercise = get_object_or_404(Exercise, postnum=id)
    if request.method == "POST":
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('exercise_index')
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'exercise/exercise_edit.html', {'form': form})

@login_required
def exercise_delete(request, id):
    exercise = Exercise.objects.get(postnum=id)
    exercise.delete()
    return redirect('exercise_index')

@csrf_exempt
def predict_calories(request):
    if request.method == 'POST':
        try:
            exercise_amount = request.POST['exercise_amount']
            id = request.POST['id']
            
    # 사용자 정보 가져오기
            user = UsersAppUser.objects.get(id=id)
            
            # 나이 계산
            current_year = datetime.now().year
            age = current_year - user.user_birth.year if user.user_birth else 0

            # 성별 데이터 준비
            gender_male = 1 if user.user_gender == 'Male' else 0
            gender_female = 1 if user.user_gender == 'Female' else 0
            
            # data_anal.py의 함수를 사용하여 칼로리 예측
            predicted_calories = calories_model_load(
                age=age,
                height=user.user_height,
                weight=user.user_weight,
                exercise_amount=exercise_amount,
                heart_rate=110,
                body_temp=39,
                gender_female=gender_female,
                gender_male=gender_male
            )

            # JSON 응답 반환
            return JsonResponse({"predicted_calories": predicted_calories}, status=200)
            
        except UsersAppUser.DoesNotExist:
            # 사용자가 존재하지 않는 경우
            return JsonResponse({"error": "User not found"}, status=404)
        except json.JSONDecodeError:
            # JSON 파싱 오류
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            # 그 외 예외 처리
            return JsonResponse({"error": str(e)}, status=500)
    else:
        # POST 요청이 아닌 경우
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)
