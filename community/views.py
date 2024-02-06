from django.utils import timezone
from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from .modules.data_anal import female_senior_input_predict, female_adult_input_predict, female_adolescent_input_predict, female_child_input_predict, male_senior_input_predict, male_adult_input_predict, male_adolescent_input_predict, male_child_input_predict 
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from decouple import config
from django.contrib.auth import get_user_model
from .models import Point, Exercise, Daily, Meal, UsersAppUser
import json
import time
from django.db.models import Avg,Sum, Count
from django.db.models import DateField
from django.db.models.functions import Cast
# .env 파일에서 OPENAI_API_KEY 가져오기
openai_api_key = config('OPENAI_API_KEY')

# OpenAI API 초기화
openai = OpenAI(api_key=openai_api_key)


def fitness_grade(request):
    if not request.user.is_authenticated:
        return redirect('main')  # 메인페이지로 리디렉션

    user = request.user

    if hasattr(user, 'user_birth') and hasattr(user, 'user_gender'):
        age = calculate_age(user.user_birth)
        gender = user.user_gender

        # 노인
        if age >= 65:
            if gender == 0:
                return render(request, 'community/male_senior.html', {'user': user})
            elif gender == 1:
                return render(request, 'community/female_senior.html', {'user': user})

        # 성인
        elif 19 <= age < 65:
            if gender == 0:
                return render(request, 'community/male_adult.html', {'user': user})
            elif gender == 1:
                return render(request, 'community/female_adult.html', {'user': user})

        # 청소년
        elif 13 <= age < 19:
            if gender == 0:
                return render(request, 'community/male_adolescent.html', {'user': user})
            elif gender == 1:
                return render(request, 'community/female_adolescent.html', {'user': user})

        # 유소년
        elif age < 13:
            if gender == 0:
                return render(request, 'community/male_child.html', {'user': user})
            elif gender == 1:
                return render(request, 'community/female_child.html', {'user': user})

        else:
            return redirect('main')
    else:
        # 필요한 정보가 없는 경우 메시지 설정
        messages.error(request, '필요한 정보가 부족합니다.')
        return redirect('main')  # 메인 페이지로 리디렉션


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def female_senior_predict_ajax(request):
    if request.method == "POST":
        sit_and_reach = request.POST.get('sit_and_reach', '')
        chair_stand_test = request.POST.get('chair_stand_test', '')
        two_minute_step_test = request.POST.get('two_minute_step_test', '')
        grip_strength_left = request.POST.get('grip_strength_left', '')
        grip_strength_right = request.POST.get('grip_strength_right', '')
        # 앉아윗몸앞으로굽히기(cm)', '의자에앉았다일어서기(회)', '2분제자리걷기(회)', '악력_좌(kg)', '악력_우(kg)'
        # sit_and_reach_(cm), chair_stand_test_(repetitions), two_minute_step_test_(steps), grip_strength_left_(kg), grip_strength_right_(kg)
        class_name = female_senior_input_predict(sit_and_reach, chair_stand_test, two_minute_step_test, grip_strength_left, grip_strength_right)
    
        return JsonResponse({'class_name': class_name})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def female_adult_predict_ajax(request):
    if request.method == "POST":
        crossover_situp = request.POST.get('crossover_situp', '')
        sit_and_reach = request.POST.get('sit_and_reach', '')
        standing_long_jump = request.POST.get('standing_long_jump', '')
        step_test_output = request.POST.get('step_test_output', '')
        grip_strength_left = request.POST.get('grip_strength_left', '')
        grip_strength_right = request.POST.get('grip_strength_right', '')
        # crossover_situp(repetitions), sit_and_reach(cm), standing_long_jump(cm), step_test_output(vo2max), grip_strength_left(kg), grip_strength_right(kg)
        # '교차윗몸일으키기(회)', '앉아윗몸앞으로굽히기(cm)', '제자리 멀리뛰기(cm)', '스텝검사출력(VO₂max)', '악력_좌(kg)', '악력_우(kg)'
        class_name = female_adult_input_predict(crossover_situp, sit_and_reach, standing_long_jump, step_test_output, grip_strength_left, grip_strength_right)
    
        return JsonResponse({'class_name': class_name})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def female_adolescent_predict_ajax(request):
    if request.method == "POST":
        sit_and_reach = request.POST.get('sit_and_reach', '')
        shuttle_run = request.POST.get('shuttle_run', '')
        repeated_jumps = request.POST.get('repeated_jumps', '')
        standing_long_jump = request.POST.get('standing_long_jump', '')
        hang_time = request.POST.get('hang_time', '')
        # sit_and_reach(cm), shuttle_run(repetitions), repeated_jumps(repetitions), standing_long_jump(cm), hang_time(seconds)
        # '앉아윗몸앞으로굽히기(cm)', '왕복오래달리기(회)', '반복점프(회)', '제자리 멀리뛰기(cm)', '체공시간(초)'
        class_name = female_adolescent_input_predict(sit_and_reach, shuttle_run, repeated_jumps, standing_long_jump, hang_time)
    
        return JsonResponse({'class_name': class_name})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def female_child_predict_ajax(request):
    if request.method == "POST":
        sit_and_reach = request.POST.get('sit_and_reach', '')
        sit_ups = request.POST.get('sit_ups', '')
        standing_long_jump = request.POST.get('standing_long_jump', '')
        shuttle_run = request.POST.get('shuttle_run', '')
        # sit_and_reach(cm), sit_ups(repetitions), standing_long_jump(cm), shuttle_run(repetitions)
        # '앉아윗몸앞으로굽히기(cm)', '윗몸말아올리기(회)', '제자리 멀리뛰기(cm)', '왕복오래달리기(회)'
        class_name = female_child_input_predict(sit_and_reach, sit_ups, standing_long_jump, shuttle_run)
    
        return JsonResponse({'class_name': class_name})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    


def male_senior_predict_ajax(request):
    if request.method == "POST":
        sit_and_reach = request.POST.get('sit_and_reach', '')
        chair_stand_test = request.POST.get('chair_stand_test', '')
        two_minute_step_test = request.POST.get('two_minute_step_test', '')
        grip_strength_left = request.POST.get('grip_strength_left', '')
        grip_strength_right = request.POST.get('grip_strength_right', '')
        # 앉아윗몸앞으로굽히기(cm)', '의자에앉았다일어서기(회)', '2분제자리걷기(회)', '악력_좌(kg)', '악력_우(kg)'
        # sit_and_reach_(cm), chair_stand_test_(repetitions), two_minute_step_test_(steps), grip_strength_left_(kg), grip_strength_right_(kg)
        class_name = male_senior_input_predict(sit_and_reach, chair_stand_test, two_minute_step_test, grip_strength_left, grip_strength_right)
    
        return JsonResponse({'class_name': class_name})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def male_adult_predict_ajax(request):
    if request.method == "POST":
        crossover_situp = request.POST.get('crossover_situp', '')
        sit_and_reach = request.POST.get('sit_and_reach', '')
        standing_long_jump = request.POST.get('standing_long_jump', '')
        step_test_output = request.POST.get('step_test_output', '')
        grip_strength_left = request.POST.get('grip_strength_left', '')
        grip_strength_right = request.POST.get('grip_strength_right', '')
        # crossover_situp(repetitions), sit_and_reach(cm), standing_long_jump(cm), step_test_output(vo2max), grip_strength_left(kg), grip_strength_right(kg)
        # '교차윗몸일으키기(회)', '앉아윗몸앞으로굽히기(cm)', '제자리 멀리뛰기(cm)', '스텝검사출력(VO₂max)', '악력_좌(kg)', '악력_우(kg)'
        class_name = male_adult_input_predict(crossover_situp, sit_and_reach, standing_long_jump, step_test_output, grip_strength_left, grip_strength_right)
    
        return JsonResponse({'class_name': class_name})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def male_adolescent_predict_ajax(request):
    if request.method == "POST":
        sit_and_reach = request.POST.get('sit_and_reach', '')
        shuttle_run = request.POST.get('shuttle_run', '')
        repeated_jumps = request.POST.get('repeated_jumps', '')
        standing_long_jump = request.POST.get('standing_long_jump', '')
        hang_time = request.POST.get('hang_time', '')
        # sit_and_reach(cm), shuttle_run(repetitions), repeated_jumps(repetitions), standing_long_jump(cm), hang_time(seconds)
        # '앉아윗몸앞으로굽히기(cm)', '왕복오래달리기(회)', '반복점프(회)', '제자리 멀리뛰기(cm)', '체공시간(초)'
        class_name = male_adolescent_input_predict(sit_and_reach, shuttle_run, repeated_jumps, standing_long_jump, hang_time)
    
        return JsonResponse({'class_name': class_name})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def male_child_predict_ajax(request):
    if request.method == "POST":
        sit_and_reach = request.POST.get('sit_and_reach', '')
        sit_ups = request.POST.get('sit_ups', '')
        standing_long_jump = request.POST.get('standing_long_jump', '')
        shuttle_run = request.POST.get('shuttle_run', '')
        # sit_and_reach(cm), sit_ups(repetitions), standing_long_jump(cm), shuttle_run(repetitions)
        # '앉아윗몸앞으로굽히기(cm)', '윗몸말아올리기(회)', '제자리 멀리뛰기(cm)', '왕복오래달리기(회)'
        class_name = male_child_input_predict(sit_and_reach, sit_ups, standing_long_jump, shuttle_run)
    
        return JsonResponse({'class_name': class_name})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def llm_index(request):
    username = request.user.username
    my_page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    id = my_page_user.id

    if Point.objects.filter(user=id).exists():
        latest_point = Point.objects.filter(user=id).latest('gained_date')
    
        # 현재 날짜와 가장 최근의 gained_date를 비교하여 남은 일수를 계산합니다.
        current_date = timezone.now()
        days_left = (latest_point.gained_date + timezone.timedelta(days=30) - current_date).days 
        return render(request, 'community/llm.html', {'days_left':days_left})



@csrf_exempt
def healthcareassistant(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # JSON 본문 데이터 처리
        subject = data.get('subject')
        user_message = data.get('userMessage')
        thread_id = data.get('threadId', '')
        assistant_id = "asst_8e76VIfVh7fuLMMXM8fKUoG1"
        username = request.user.username    
        context = my_page(username)
        weight_dates = context['weight_dates']
        weights = context['weights']
        graph_dates = context['graph_dates']
        meal_calories = context['graph_meal_calories']
        exercise_calories = context['graph_exercise_calories']
        todays_meal_calories_sum = context['todays_meal_calories_sum']    

        user_birth = UsersAppUser.objects.filter(username=username).values('user_birth')
        user_birth = user_birth[0]['user_birth']
        user_height = UsersAppUser.objects.filter(username=username).values('user_height')
        user_height = user_height[0]['user_height']
        user_weight = UsersAppUser.objects.filter(username=username).values('user_weight')
        user_weight = user_weight[0]['user_weight']
        user_target_weight = UsersAppUser.objects.filter(username=username).values('user_target_weight')
        user_target_weight = user_target_weight[0]['user_target_weight']
        user_exercise_purpose = UsersAppUser.objects.filter(username=username).values('user_exercise_purpose')
        user_exercise_purpose = user_exercise_purpose[0]['user_exercise_purpose']
        if user_exercise_purpose == "health":
            user_exercise_purpose = "건강"
        elif user_exercise_purpose == "bulkup":
            user_exercise_purpose = "벌크업"
        else:
            user_exercise_purpose = "다이어트"
        
        user_activity = UsersAppUser.objects.filter(username=username).values('user_activity')
        user_activity = user_activity[0]['user_activity']
        if user_activity == "1":
            user_activity = "거의 활동이 없음"
        elif user_activity == "2":
            user_activity = "약간의 활동"
        elif user_activity == "3":
            user_activity = "보통 활동"
        elif user_activity == "4":
            user_activity = "활발한 활동"
        else:
            user_activity = "매우 활발한 활동"

        user_gender = UsersAppUser.objects.filter(username=username).values('user_gender')
        user_gender = user_gender[0]['user_gender']
        if user_gender == "0":
            user_gender = "남자"
        else: 
            user_gender = "여자"
       
        # # 추출한 데이터 사용

        try:
            # 스레드가 없으면 새로운 스레드 생성
            if not thread_id:
                empty_thread = openai.beta.threads.create()
                thread_id = empty_thread.id
                thread = empty_thread  # 스레드 객체로 초기화
                openai.beta.threads.messages.create(
                    thread_id=thread_id,
                    role="user",
                    content=f"""세계 최고의 건강관리사님, 저의 생일은{user_birth}이고, 키는 {user_height}cm 이고, 몸무게는 {user_weight}kg 입니다. 
                                제 목표 몸무게는 {user_target_weight}kg 입니다.
                                저는 평소에 {user_activity}하는 편입니다.
                                제가 운동을 하고자 하는 목표는 {user_exercise_purpose}입니다.
                                오늘은 {todays_meal_calories_sum}칼로리를 섭취했네요.
                                저는 아래와 같이 몸무게와 식단, 운동을 기록하고 있습니다.
                                식단 섭취칼로리 또는 운동 소모칼로리 중 하나라도 기록은 한 날짜들 : {graph_dates},
                                식단 섭취칼로리 기록들 : {meal_calories},
                                운동 소모칼로리 기록들 : {exercise_calories},
                                몸무게를 기록한 날짜들 : {weight_dates},
                                몸무게 기록들 : {weights}kg,
                                위의 모든 정보들을 토대로
                                저에게 {subject}에 대한 조언을 먼저 해주실 수 있나요?"""
                )

            # 사용자 메시지 추가
            message = openai.beta.threads.messages.create(
                    thread_id=thread_id,
                    role="user",
                    content=user_message
                )

            # OpenAI Assistant 실행
            run = openai.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )

            while run.status != "completed":
                run = openai.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
                time.sleep(0.5)
                # time.sleep(0.5)  # Django에서는 sleep 함수 대신에 await new Promise((resolve) => setTimeout(resolve, 500)); 사용

            messages = openai.beta.threads.messages.list(thread_id=thread_id)
            assistant_last_msg = messages.data[0].content[0].text.value

            response_data = {"assistant": assistant_last_msg, "threadId": thread_id}
            return JsonResponse(response_data)  # JSON 형식으로 응답
        except Exception as e:
            # 예외가 발생하면 오류 응답 반환
            print("An error occurred:", str(e))  # 오류 메시지 출력
            return JsonResponse({"error": str(e)}, status=500)

def payment(request, username):

    if not request.user.is_authenticated:
        return redirect('main')  # 메인페이지로 리디렉션

    user = request.user
    my_page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    id = my_page_user.id

    if Point.objects.filter(user=id).exists():
        latest_point = Point.objects.filter(user=id).latest('gained_date')
    
        # 현재 날짜와 가장 최근의 gained_date를 비교하여 남은 일수를 계산합니다.
        current_date = timezone.now()
        days_left = (latest_point.gained_date + timezone.timedelta(days=30) - current_date).days 
        return render(request, 'community/llm.html', {'days_left':days_left})
    
    try:
        point_entry = Point.objects.get(user=id)
        latest_point = Point.objects.filter(user=id).latest('gained_date')
    
        # 현재 날짜와 가장 최근의 gained_date를 비교하여 남은 일수를 계산합니다.
        current_date = timezone.now()
        days_left = (latest_point.gained_date + timezone.timedelta(days=30) - current_date).days    
        return render(request, 'community/llm.html', {'days_left':days_left})
    except Point.DoesNotExist:

        return render(request, 'community/payment.html')
    
@csrf_exempt
def create_point_entry(request):
    if request.method == 'POST':
        try:
            # JSON 요청에서 데이터 추출
            data = json.loads(request.POST.get('payment_user_data'))  # request.body를 JSON으로 파싱
            user_id = data.get('user')
            point_value = data.get('point')
            gaining_method = data.get('gaining_method')
            gained_date = data.get('gained_date')

            # 새 Point 항목 생성
            Point.objects.create(
                user_id=user_id,
                point=point_value,
                gaining_method=gaining_method,
                gained_date=gained_date
            )

            # 필요한 경우 성공 응답 반환
            return JsonResponse({'message': 'Point 항목이 성공적으로 생성되었습니다.'})

        except Exception as e:
            # 예외 또는 오류 처리
            print("오류 발생: ", str(e))  # 서버 측에서 로그 출력
            return JsonResponse({'error': str(e)}, status=400)

    # 다른 HTTP 메서드 또는 잘못된 요청 처리
    return JsonResponse({'error': '잘못된 요청 메서드입니다.'}, status=405)


def my_page(username):

    my_page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    id = my_page_user.id

    everyday_weight = Daily.objects.filter(user=id).values('date').annotate(current_weight=Avg('current_weight')).order_by('date')
    everyday_meal = Meal.objects.filter(user=id).values('meal_date').annotate(meal_calories=Sum('meal_calories')).order_by('meal_date')
    everyday_exercise = Exercise.objects.filter(user=id).values('exercise_date').annotate(calories_burned=Sum('calories_burned')).order_by('exercise_date')
    
    continuous_days = 0
    max_continuous = 0
    previous_date = None

    today = timezone.now().date()
    
    for daily_weight in everyday_weight:
        daily_date = daily_weight['date']
        if previous_date and (daily_date - previous_date).days == 1:
            continuous_days += 1
        else:
            max_continuous = max(max_continuous, continuous_days)
            continuous_days = 1
        previous_date = daily_date
    
    max_continuous = max(max_continuous, continuous_days)

    weight_dates = [daily_weight['date'].strftime('%Y-%m-%d') for daily_weight in everyday_weight]
    weights = [daily_weight['current_weight'] for daily_weight in everyday_weight]

    # 날짜를 키로 사용하여 데이터를 결합
    combined_data = {}
    for daily_meal in everyday_meal:
        date_str = daily_meal['meal_date'].strftime('%Y-%m-%d')
        combined_data.setdefault(date_str, {'meal_calories': 0, 'exercise_calories': 0})
        combined_data[date_str]['meal_calories'] += daily_meal['meal_calories']

    for daily_exercise in everyday_exercise:
        if daily_exercise['calories_burned'] is not None:
            date_str = daily_exercise['exercise_date'].strftime('%Y-%m-%d')
            combined_data.setdefault(date_str, {'meal_calories': 0, 'exercise_calories': 0})
            combined_data[date_str]['exercise_calories'] += daily_exercise['calories_burned']


    # 정렬된 날짜 리스트 생성
    sorted_dates = sorted(combined_data.keys())


    # 그래프 데이터 준비
    graph_dates = []
    graph_meal_calories = []
    graph_exercise_calories = []
    for date_str in sorted_dates:
        graph_dates.append(date_str)
        graph_meal_calories.append(combined_data[date_str]['meal_calories'])
        graph_exercise_calories.append(combined_data[date_str]['exercise_calories'])

    
    # 특정 기간 내 식단 및 운동 기록을 조회합니다.
    start_date = timezone.now().date() - timezone.timedelta(days=180)  # 30일 전부터
    end_date = timezone.now().date() + timezone.timedelta(days=1)

    # 식단 기록
    meal_records = Meal.objects.filter(user=id,
        meal_date__range=(start_date, end_date),
        meal_calories__isnull=False
    ).annotate(
        meal_date_date=Cast('meal_date', DateField())
    ).values('meal_date_date').annotate(
        meal_count=Count('meal_calories')
    )

    # 운동 기록
    exercise_records = Exercise.objects.filter(user=id,
        exercise_date__range=(start_date, end_date),
        calories_burned__isnull=False
    ).annotate(
        exercise_date_date=Cast('exercise_date', DateField())
    ).values('exercise_date_date').annotate(
        exercise_count=Count('calories_burned')
    )

    # 이벤트 데이터를 생성합니다.
    events = []
    for record in meal_records:
        events.append({
            'title': f'식단: {record["meal_count"]}회',
            'start': record['meal_date_date'].isoformat(),
            'color': '#004085',  # 진한 파랑 색상
            'url': '/meal/meal_history'
        })

    for record in exercise_records:
        events.append({
            'title': f'운동: {record["exercise_count"]}회',
            'start': record['exercise_date_date'].isoformat(),
            'color': '#228B22',  # 포레스트 그린 색상
            'url' : '/exercise/exercise/index/'
        })
    
    today_str = today.strftime('%Y-%m-%d')

    # 오늘 날짜의 총 식사 칼로리를 가져옵니다. 데이터가 없으면 0을 반환합니다.
    todays_meal_calories_sum = combined_data.get(today_str, {}).get('meal_calories', 0)
    todays_meal_calories_sum = "{:.2f}".format(todays_meal_calories_sum)

    context = {
        'title': '그래프',
        'weight_dates': json.dumps(weight_dates),
        'weights': json.dumps(weights),
        'graph_dates' : json.dumps(graph_dates),
        'graph_meal_calories' : json.dumps(graph_meal_calories),
        'graph_exercise_calories' : json.dumps(graph_exercise_calories),
        'todays_meal_calories_sum': todays_meal_calories_sum,
        'max_continuous': max_continuous,
        "my_page_user":my_page_user,
        'events': json.dumps(events),
    }

    return context
