from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta

import pytz

from .services import get_personal_recommended_nutrient, get_recommend_mealtype

from .models import CalorieDictionary, Meal, UsersAppUser
from .modules.meal_anal import predict_meal
from django.db.models import Q, Sum
from uuid import uuid4
from .foodDict import *
from .models import Meal
from .models import CalorieDictionary
from .models import Menu
import json
from django.db.models import Sum
import ast
from random import sample
import pytz
from django.conf import settings
from dotenv import load_dotenv
import os
# Create your views here.


def meal_index(request):
    return render(request, 'meal/meal_index.html' )

def meal_analyze(request):

    return render(request, 'meal/meal_analyze.html')


def meal_recommend(request):
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    # print('dotenv_path : ',dotenv_path)
    load_dotenv(dotenv_path)
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    # print(GOOGLE_API_KEY)

    id = request.user.id

    recommended = []

    chk_meal_type = get_recommend_mealtype(id)

    menu = Menu.objects.filter(menu_classification=chk_meal_type)

    random_menus = sample(list(menu), min(len(menu), 3))

    if menu is None : 
        pass
    else:
        random_menus = sample(list(menu), min(len(menu), 3))

        for data in random_menus:
            # print('data : ',type(data.menu_dtl))
            recommended.append([data.menu_dtl])

    for i in range(len(recommended)):
        recommended[i] = recommended[i][0].split(', ')

    # 수정해서 이제 안씀
    # search_items = [menu[0] for menu in recommended]

    # print('세개 search_items ',search_items)
    msg = ''

    if chk_meal_type == '저염식':
        msg = '식습관 분석에 따르면 나트륨 섭취가 권장량을 초과하는 경향이 있습니다. 건강을 위해 나트륨을 줄인 저염식을 추천해 드립니다.'
    elif chk_meal_type =='당뇨식':
        msg = '분석 결과, 당분 섭취가 일반적인 권장량을 넘는 것으로 나타났습니다. 건강 관리를 위해 혈당 조절에 도움이 되는 당뇨식을 권장합니다'
    else:
        msg = '귀하의 식습관은 대체로 균형 잡힌 것으로 보입니다. 현재의 건강한 식단을 유지하시면서 다양한 영양소가 포함된 일반식을 계속 드실 것을 추천합니다.'

    context = {
        'meal_type': chk_meal_type,
        'recommend': recommended,
        # 'searchText' : search_items
        # 'searchText' : json.dumps(search_items),
        'msg' : msg,
        'GOOGLE_API_KEY' : GOOGLE_API_KEY
    }

    # print('context : ',context)

    return render(request, 'meal/meal_recommend.html', context)


def meal_history(request):
    id = request.user.id

    meals = Meal.objects.filter(user_id=id).order_by('meal_date')

    today = datetime.today()
    month_data = today.month
    first_day_of_month = today.replace(day=1)
    next_month = today.replace(day=28) + timedelta(days=4)
    last_day_of_month = next_month - timedelta(days=next_month.day)

    # 날짜별 칼로리를 계산
    calories_by_date = defaultdict(int)
    for meal in meals:
        date_only = meal.meal_date.date()
        if first_day_of_month.date() <= date_only <= last_day_of_month.date():
            calories_by_date[date_only] += meal.meal_calories

    # 달 계산
    all_dates = [first_day_of_month.date() + timedelta(days=x) for x in range((last_day_of_month - first_day_of_month).days + 1)]
    dates = [date.strftime('%Y-%m-%d') for date in all_dates]
    calories = [calories_by_date[date] for date in all_dates]

    # 데이터가 있는 날짜
    days_with_data = sum(1 for val, cal in calories_by_date.items() if cal > 0)

    context = {
        'title': '그래프',
        'month': month_data ,
        'dates': json.dumps(dates),
        'calories': json.dumps(calories),
        'days_with_data': days_with_data,  # 이번달중 데이터가 있는 날짜
    }

    return render(request, 'meal/meal_history.html', context)

def get_monthly_history(request, year, month):

    user_id = request.user.id
    start_date = datetime(year, month, 1)
    end_date = start_date + timedelta(days=31)  
    end_date = end_date.replace(day=1) - timedelta(days=1)

    meals = Meal.objects.filter(user_id=user_id, meal_date__range=[start_date, end_date]).order_by('meal_date')

    calories_by_date = defaultdict(int)

    for meal in meals:
        date_only = meal.meal_date.date()
        if start_date.date() <= date_only <= end_date.date():
            calories_by_date[date_only] += meal.meal_calories
    
    # print('calories_by_date : ' , calories_by_date)

    # 달 계산
    all_dates = [start_date.date() + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    dates = [date.strftime('%Y-%m-%d') for date in all_dates]
    calories = [calories_by_date[date] for date in all_dates]

    # 데이터가 있는 날짜
    days_with_data = sum(1 for val, cal in calories_by_date.items() if cal > 0)

    data = {
        'month': month ,
        'dates': json.dumps(dates),
        'calories': json.dumps(calories),
        'days_with_data': days_with_data,
    }

    return JsonResponse(data)

def meal_detail(request, date):
    # print('date : ', date)
    id = request.user.id
    # print('id = ',id)

    # 유저별 권장 영양섭취 계산
    user_info = UsersAppUser.objects.filter(id=id).first()

    user_height = user_info.user_height
    user_weight = user_info.user_weight
    user_gender = user_info.user_gender

    user_birth_date = user_info.user_birth
    current_date = datetime.now()

    # 나이 계산
    user_age = current_date.year - user_birth_date.year - ((current_date.month, current_date.day) < (user_birth_date.month, user_birth_date.day)) -1

    # 활동 수준에 따른 BMR 값 변화
    user_activity = user_info.user_activity

    nutrient_res = get_personal_recommended_nutrient(user_height, user_weight, user_gender, user_age, user_activity)
   
    protein_min = nutrient_res["protein_min"]
    fat_min = nutrient_res["fat_min"]
    carbs_min = nutrient_res["carbs_min"]
    sugar_max = nutrient_res["sugar_max"]
    fiber_recommended = nutrient_res["fiber_recommended"]
    natrium_recommended = nutrient_res["natrium_recommended"]

    total_protein = 0.0
    total_fat = 0.0
    total_carbs = 0.0
    total_sugar = 0.0
    total_fiber = 0.0
    total_natrium = 0.0
        

    # 날짜 형식으로 변환 필요
    start_date = datetime.strptime(date, '%Y-%m-%d')
    end_date = start_date + timedelta(days=1)

    meals = Meal.objects.filter(user_id=id, meal_date__range=(start_date, end_date))

    # meal_type 별로 분류
    meal_information = {'아침': {'foods': [], 'calories': 0, 'nutrients': defaultdict(float)},
                 '점심': {'foods': [], 'calories': 0, 'nutrients': defaultdict(float)},
                 '저녁': {'foods': [], 'calories': 0, 'nutrients': defaultdict(float)},
                 '간식': {'foods': [], 'calories': 0, 'nutrients': defaultdict(float)}}


    for meal in meals:
        meal_info_list = ast.literal_eval(meal.meal_info)

        for info in meal_info_list:
            menu = CalorieDictionary.objects.filter(food_code=info).first()

            if menu is not None:
                meal_information[meal.meal_type]['foods'].append({
                    'name': menu.food_name,
                    'calories': menu.calories,
                    'protein': menu.protein,
                    'fat': menu.fat,
                    'carbohydrate': menu.carbohydrate,
                    'sugar': menu.suger,
                    'dietary_fiber': menu.dietary_fiber,
                    'natrium': menu.natrium
                })
                total_protein += menu.protein
                total_fat += menu.fat
                total_carbs += menu.carbohydrate
                total_sugar += menu.suger
                total_fiber += menu.dietary_fiber
                total_natrium += menu.natrium
    
    deficient_nutrients = {}

    if total_protein < protein_min:
        deficient_nutrients['단백질'] = {'recommended': protein_min, 'actual': total_protein}
    if total_fat < fat_min:
        deficient_nutrients['지방'] = {'recommended': fat_min, 'actual': total_fat}
    if total_carbs < carbs_min:
        deficient_nutrients['탄수화물'] = {'recommended': carbs_min, 'actual': total_carbs}
    if total_sugar > sugar_max:
        deficient_nutrients['당류'] = {'recommended': sugar_max, 'actual': total_sugar}
    if total_fiber < fiber_recommended:
        deficient_nutrients['식이섬유'] = {'recommended': fiber_recommended, 'actual': total_fiber}
    if total_natrium > natrium_recommended:
        deficient_nutrients['나트륨'] = {'recommended': natrium_recommended, 'actual': total_natrium}

                
    context = {
        'date' : date,
        'meal_info': meal_information,
        'deficient_nutrients' : deficient_nutrients
    }

    return render(request, 'meal/meal_detail.html', context)

# 이미지 파일명에 고유번호를 부여해주는 함수
def rename_imagefile_to_uuid(filename):
    # ext = filename.split('.')[-1]
    uuid = uuid4().hex

    filename = uuid

    return filename

# 예측 함수
def meal_to_analyze(request):
    if request.method == 'POST':
        meal_img = request.FILES.get('fileUpload')
        # print(meal_img.name)

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        file_name = rename_imagefile_to_uuid(meal_img.name)
        file_name = file_name + '_' + meal_img.name
        image_url = fs.save(file_name, meal_img)

        # 이미지를 예측하러 함수로 보내기
        detections = predict_meal(meal_img)
        # print(detections)
        image_url = settings.MEDIA_URL + image_url
        # print(image_url)

        # 돌아온 값 담아서 return
    return render(request, 'meal/meal_analyze_result.html', {'detect_results': detections, 'meal_image': image_url})

# 칼로리 사전 기능
def calorie_dict(request):
    page = request.GET.get('page', 1)
    items_per_page = 30
    page_display = 10

    # 페이지가 첫 로드되면 DB의 모든 데이터를 긁어와 띄운다
    cal_data = CalorieDictionary.objects.all()

    # form name=search인 항목에서 검색어를 가져온다.
    # 첫 로드 시에는 비어있다.
    search_query = request.GET.get('search', '')
    # print(search_query)

    # 대분류, 소분류 항목을 가져와 option 태그에서 for문을 돌려 노출시킨다.
    major_classes = CalorieDictionary.objects.filter(Q(food_name__icontains=search_query)
                                                      | Q(maker__icontains=search_query)).values_list('major_class', flat=True).distinct()
    detail_classes = CalorieDictionary.objects.filter(Q(food_name__icontains=search_query)
                                                       | Q(maker__icontains=search_query)).values_list('detail_class', flat=True).distinct()

    # form name=majorClass, detailClass 인 항목을 가져온다.
    major_class_filter = request.GET.get('majorClass', '')
    # print(major_class_filter)
    detail_class_filter = request.GET.get('detailClass', '')
    # print(detail_class_filter)
    
    # 각 항목에 맞는 데이터를 필터해온다. 
    if major_class_filter:
        cal_data = cal_data.filter(major_class=major_class_filter)
    if detail_class_filter:
        cal_data = cal_data.filter(detail_class=detail_class_filter)

    # 검색 키워드 개수에 따라 다르게 굴러간다.
    # try except 구문은 크게 필요 없어보이는데, 없으면 오류가 난다.
    try:
        keywords = search_query.split()
        # print(keywords)
        if len(keywords)>=2:
            q_obj = Q()

            q_obj |= Q(food_name__icontains=keywords[0]) & Q(maker__icontains=keywords[1])

            # print(q_obj)
        
            cal_data = cal_data.filter(q_obj)

            # 수정된 검색결과에 맞춰 대분류, 소분류 재검색
            major_classes = CalorieDictionary.objects.filter(q_obj).values_list('major_class', flat=True).distinct()
            detail_classes = CalorieDictionary.objects.filter(q_obj).values_list('detail_class', flat=True).distinct()
        else:
            cal_data = cal_data.filter(Q(food_name__icontains=search_query)
                                        | Q(maker__icontains=search_query))
    except:
        cal_data = cal_data.filter(Q(food_name__icontains=search_query)
                                        | Q(maker__icontains=search_query))

    # 페이지 기능 실행을 위한 paginator
    paginator = Paginator(cal_data, items_per_page)

    try:
        curruent_page_data = paginator.page(page)
    except PageNotAnInteger:
        curruent_page_data = paginator.page(1)
    except EmptyPage:
        curruent_page_data = paginator.page(paginator.num_pages)

    index = curruent_page_data.number - 1
    max_index = len(paginator.page_range)
    start_index = max(0, index - page_display // 2)
    end_index = min(max_index, start_index + page_display)

    page_range = paginator.page_range[start_index:end_index]

    context = {
        'current_page_data':curruent_page_data,
        'page_range':page_range,
        'major_classes':major_classes,
        'detail_classes':detail_classes,
        'search_query': search_query,
        'major_class_filter': major_class_filter,
        'detail_class_filter': detail_class_filter,
        }

    return render(request, 'meal/calorie_dictionary.html', context)

# 칼로리 사전에 걸린 링크 기본키로 음식 상세정보 출력
def food_detail(request, food_code):
    food = get_object_or_404(CalorieDictionary, pk=food_code)
    return render(request, 'meal/calorie_dict_detail.html', {'food':food})

# 분석화면에서 검색어 입력하면 검색 후보군 띄워주는 함수
@require_GET
def food_search(request):
    search_word = request.GET.get('searchWord', '')
    # print(search_word)

    results = CalorieDictionary.objects.filter(food_name__icontains=search_word)[:20]
    
    data = {'results': [{'food_code': result.food_code, 'name': result.food_name, 'maker': result.maker} for result in results]}

    return JsonResponse(data)

# 본격적인 식단 POST 함수
@csrf_exempt
def meal_post(request):
    if request.method == "POST":
        meal_data_list = json.loads(request.POST.get('meal_data'))
        # print(meal_data_list[0]) # 리스트를 제대로 받아온다
        # print(meal_data_list[-1])

        filtered_list = []

        for food in meal_data_list[0]:
            # 정규성 검사 함수
            food_code = check_food_code(food)
            if food_code is not None:
                filtered_list.append(food_code)
        
        # 리스트 제대로 변환되어 출력된다.
        # print(filtered_list)

        # 칼로리 합산하는 함수
        meal_calories, nutrient_info = total_calories(filtered_list)
        # print(meal_calories)
        # print(nutrient_info)

        if request.user.is_authenticated:
            user_instance = UsersAppUser.objects.get(id=request.user.id)

            # 옵션 1 파이썬으로 현재 시간 얻기
            current_time = datetime.now()

            # 옵션 2 django.utils timezone을 이용해 시간 얻기
            # current_time = timezone.now().replace(tzinfo=pytz.timezone('Asia/Seoul'))

            # 옵션 3 timezone.datetime.now() 가져오기
            # current_time = timezone.datetime.now()

            # 테스트를 위한 임의 조작 시간
            # current_time = datetime(2024, 1, 31, 13, 22, 34)

            print(f"현재 시간 : {current_time}")

            # 아침, 점심, 저녁, 간식 출력
            if 6 <= current_time.hour <= 9:
                meal_type = "아침"
            elif 11 <= current_time.hour <= 14:
                meal_type = "점심"
            elif 18 <= current_time.hour <= 20:
                meal_type = "저녁"
            else:
                meal_type = "간식"

            # print(meal_type)
            
            # DB에 저장
            # 조작 시간을 사용할 경우 models.py에서 meal_date에 auto_now_add=False로 바꾸자.

            Meal.objects.create(
                user = user_instance,
                meal_date = current_time,
                meal_photo = meal_data_list[-1],
                meal_info = json.dumps(filtered_list),
                meal_type = meal_type,
                meal_calories = meal_calories,
                nutrient_info = json.dumps(nutrient_info)
            )

            ############ DB 저장 완료 후 로직 #############

            # (1) 날짜 기준으로 오늘 칼로리만 합산해오기

            # 파이썬 내장 datetime 사용
            # today = datetime.now()

            # django 내장 timezone 사용
            today = timezone.datetime.now()

            day_start = timezone.datetime.combine(today, timezone.datetime.min.time())
            day_end = timezone.datetime.combine(today, timezone.datetime.max.time())

            # print(day_start)
            # print(day_end)

            all_meal_today = Meal.objects.filter(user=request.user.id,
                                                 meal_date__range=(day_start, day_end))\
                                                 .aggregate(all_calories=Sum("meal_calories"))
            
            # print(f"오늘의 전체 식사 : {all_meal_today}")

            todays_nutrients = Meal.objects.filter(user_id=request.user.id, meal_date__range=[day_start, day_end])

            if todays_nutrients is not None:
                total_nutrient_sum = [0] * 8

                for meal in todays_nutrients:
                    meal_nutrient_text = meal.nutrient_info
                    meal_nutrient_list = eval(meal_nutrient_text)
                    total_nutrient_sum = [x + y for x, y in zip(total_nutrient_sum, meal_nutrient_list)]
            else:
                todays_nutrients = nutrient_info

            calorie_today = all_meal_today["all_calories"] if all_meal_today["all_calories"] is not None else meal_calories

            # print(f"전체 영양소 : {total_nutrient_sum}")
            # print(calorie_today)

            # (2) filtered_list로 칼로리 딕셔너리에서 정보 빼오기
            each_foods = []
            for fcode in filtered_list:
                food_info = get_object_or_404(CalorieDictionary, pk=fcode)
                # food_info.carbohydrate 메서드 체이닝으로 정보 추출하면 될 듯
                each_foods.append(food_info)
            
            # print(each_foods)
            
            # (3) 함수로 보낸 값 받아오기
            nurtient_proportion, warnings_dict, user_max_calorie = nutrient_quotes(request.user.id, today, calorie_today, total_nutrient_sum)
            
            # 모든 단위 g으로 바꾸기
            nutrient_gram = nutrient_info
            # mg_index = 4
            # nutrient_gram[mg_index] /= 1000
            # total_nutrient_sum[mg_index] /= 1000
            meal_calories = round(meal_calories, 2)
            calorie_today = round(calorie_today, 2)
            trimed_nutrient = [round(n, 2) for n in nutrient_gram]
            total_nutrient = [round(n, 2) for n in total_nutrient_sum]

            # print(f"오늘의 영양소 : {trimed_nutrient}")

            context = {
                'this_meal_cal': meal_calories,
                'total_nutrient': trimed_nutrient,
                'each_foods': each_foods,
                'todays_total_cal': calorie_today,
                'todays_total_nut': total_nutrient,
                'meal_type': meal_type,
                'nurtient_proportion': nurtient_proportion,
                'warnings_dict': warnings_dict,
                'user_max_calorie': user_max_calorie,
            }

            return render(request, 'meal/meal_nutrient.html', context)
        else:
            return JsonResponse({'success': False, 'error': "올바르지 않은 데이터 형식"})
    else:
        return JsonResponse({'success': False, 'error': "올바르지 않은 요청사항"})

def test(request):
    # 테스트용 코드
    # 아직 테스트케이스 만들고 설정하는 방법을 잘 모르겠다

    id = request.user.id
    print(f"유저 id : {id}")

    asia_seoul = pytz.timezone('Asia/Seoul')
    # timezone_today = timezone.now().replace(tzinfo=asia_seoul)

    # timezone에서 timedelta 9를 하면 한국 시간이 되겠다.
    timezone_today = timezone.datetime.now()
    today = timezone_today + timedelta(hours=9)
    today = today.replace(tzinfo=asia_seoul)

    print(f"현재 시간 : {today}")
    print(f"타임존 시간 : {timezone_today}")

    day_start = timezone.datetime.combine(timezone_today, timezone.datetime.min.time())
    day_end = timezone.datetime.combine(timezone_today, timezone.datetime.max.time())
    print(f"시작 날짜 : {day_start}")
    print(f"종료 날짜 : {day_end}")

    todays_nutrients = Meal.objects.filter(user_id=request.user.id, meal_date__range=[day_start, day_end])

    print(todays_nutrients.first().meal_date)

    total_nutrient_sum = [0] * 6

    for meal in todays_nutrients:
        meal_nutrient_text = meal.nutrient_info
        meal_nutrient_list = eval(meal_nutrient_text)
        total_nutrient_sum = [x + y for x, y in zip(total_nutrient_sum, meal_nutrient_list)]

    mg_index = 4
    total_nutrient_sum[mg_index] /= 1000

    total_nutrient = [round(n, 2) for n in total_nutrient_sum]
    print(total_nutrient)

    # user_meal = Meal.objects.filter(user_id=id)
    # for meal in user_meal:
    #     # 왜 메서드 체이닝을 잊고 있었을까
    #     print(meal.nutrient_info)
    return render(request, 'meal/test.html')