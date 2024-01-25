from django.utils import timezone
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Daily, User, UsersAppUser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserForm, MypageUserForm
from django.db.models import Avg, Sum, Count


# Create your views here.
# 로그인, 회원가입 전용 함수
def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')
    
    return render(request, 'main.html')

def sign_out(request):
    logout(request)
    return redirect('main')

def sign_up(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main')
    else:
        form = UserForm()

    return render(request, "users_app/sign_up.html", {'form': form})

def id_check(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username', None)
            if username:
                if UsersAppUser.objects.filter(username=username).exists():
                    return JsonResponse({'is_taken':True})
                else:
                    return JsonResponse({'is_taken':False})
        except IntegrityError:
            return redirect('sign_up')

    else:
        return JsonResponse({'error':'올바르지 않은 형식입니다.'})

# def password_check(request):
#     if request.method == 'POST':
#         form = PasswordCheckForm(request.POST)

#         if form.is_valid():
#             password = form.cleaned_data['password']
#             password_check = form.cleaned_data['confirm']
    

def my_page(request, username):

    my_page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    id = my_page_user.id

    everyday = Daily.objects.filter(user=id).values('date').annotate(current_weight=Avg('current_weight'), total_meal_calories=Sum('total_meal_calories'), total_exercise_calories=Sum('total_exercise_calories')).order_by('date')
    continuous_days = 0
    max_continuous = 0
    previous_date = None

    today = timezone.localdate()
    todays_total_meal_calories = Daily.objects.filter(user_id=id, date=today).aggregate(Sum('total_meal_calories'))
    todays_meal_calories_sum = todays_total_meal_calories.get('total_meal_calories__sum') or 0
    
    for daily in everyday:
        daily_date = daily['date']
        if previous_date and (daily_date - previous_date).days == 1:
            continuous_days += 1
        else:
            max_continuous = max(max_continuous, continuous_days)
            continuous_days = 1
        previous_date = daily_date
    
    max_continuous = max(max_continuous, continuous_days)

    dates = [daily['date'].strftime('%Y-%m-%d') for daily in everyday]
    weights = [daily['current_weight'] for daily in everyday]
    meal_calories = [daily['total_meal_calories'] for daily in everyday]
    exercise_calories = [daily['total_exercise_calories'] for daily in everyday]
    
    # 특정 기간 내 식단 및 운동 기록을 조회합니다.
    start_date = timezone.now().date() - timezone.timedelta(days=180)  # 30일 전부터
    end_date = timezone.now().date()  # 현재 날짜까지
    # 식단 기록
    meal_records = Daily.objects.filter(
    date__range=(start_date, end_date),
    total_meal_calories__isnull=False
    ).values('date').annotate(
        meal_count=Count('total_meal_calories', distinct=True)
    )

    # 운동 기록
    exercise_records = Daily.objects.filter(
    date__range=(start_date, end_date),
    total_exercise_calories__isnull=False
    ).values('date').annotate(
        exercise_count=Count('total_exercise_calories', distinct=True)
    )

    # 이벤트 데이터를 생성합니다.
    events = []
    for record in meal_records:
        events.append({
            'title': f'식단: {record["meal_count"]}회',
            'start': record['date'].isoformat(),
            'color': '#004085'  # 진한 파랑 색상
        })
    for record in exercise_records:
        events.append({
            'title': f'운동: {record["exercise_count"]}회',
            'start': record['date'].isoformat(),
            'color': '#228B22'  # 포레스트 그린 색상
        })
    
    context = {
        'title': '그래프',
        'dates': json.dumps(dates),
        'weights': json.dumps(weights),
        'meal_calories': json.dumps(meal_calories),
        'exercise_calories': json.dumps(exercise_calories),
        'todays_meal_calories_sum': todays_meal_calories_sum,
        'max_continuous': max_continuous,
        "my_page_user":my_page_user,
        'events': json.dumps(events),
    }

    return render(request, "users_app/my_page.html", context)

def my_page_update(request, username):
    # (1) 전달받은 username에 해당되는 상품 정보 가져와서
    user = get_object_or_404(User, username=username)
        # 유효성 검사 is_valid
    if request.method == "POST":
        # (3) 폼변수의 가져온 값(=user 데이터 내용)을 form 변수에 저장
        form = MypageUserForm(request.POST, instance=user)
        # (4) Django의 기본 기능은 is_valid()라는 메소드를 사용해서 데이터 유효성 확인
        # 마치 수학 공식과 같은 것
        if form.is_valid():
            # (5) form에 저장된 데이터를 아직 완전 저장안하고 
            # (참고로 현재는 이부분 없어도 됨)
            # user = form.save()
            
            user = form.save(commit=True)
            # commit = False 수행할 작업이 있다면 여기서 수행 (우리는 현대 자른 작업 없음)
            # user...() 작업
            # (6) 여기에서 DB에 저장할 것임.
            user.save()
            # (7) DB에 저장 후 결과 확인하기 위해 상품 조회 화면으로 이동 (포워딩)
            # redirect() 사용
            return redirect('my_page', username=user.username)
    else:
        form = MypageUserForm(instance=user) #처음 form 화면 출력
        # form의 user에 해당되는 데이터 출력

    # (8) else : POST 요청이 아니라면 입력 폼 그대로 출력
    return render(request, 'users_app/my_page_update.html', {'form':form})
