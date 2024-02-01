from datetime import date
from django.shortcuts import redirect, render
from .modules.data_anal import female_senior_input_predict, female_adult_input_predict, female_adolescent_input_predict, female_child_input_predict, male_senior_input_predict, male_adult_input_predict, male_adolescent_input_predict, male_child_input_predict 
from django.http import JsonResponse
from django.contrib import messages
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
from django.views.decorators.csrf import csrf_exempt
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI

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
    