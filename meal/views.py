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
from .models import CalorieDictionary, Meal, UsersAppUser
from .modules.meal_anal import predict_meal
from django.db.models import Q
from uuid import uuid4
from .foodDict import *
from .models import Meal
from .models import CalorieDictionary
import json
from django.db.models import Sum
from datetime import datetime, timedelta
import ast

# Create your views here.

def meal_index(request):
    return render(request, 'meal/meal_index.html' )

def meal_analyze(request):

    return render(request, 'meal/meal_analyze.html')

def meal_history(request):
    id = request.user.id

    meals = Meal.objects.filter(user_id=id)\
                        .values('meal_date')\
                        .annotate(total_calories=Sum('meal_calories'))\
                        .order_by('meal_date')

    continuous_days = 0
    max_continuous = 0
    previous_date = None

    for meal in meals:
        meal_date = meal['meal_date']
        if previous_date and (meal_date - previous_date).days == 1:
            continuous_days += 1
        else:
            max_continuous = max(max_continuous, continuous_days)
            continuous_days = 1
        previous_date = meal_date
    
    max_continuous = max(max_continuous, continuous_days)

    dates = [meal['meal_date'].strftime('%Y-%m-%d') for meal in meals]
    calories = [meal['total_calories'] for meal in meals]

    context = {
        'title': '그래프',
        'dates': json.dumps(dates),
        'calories': json.dumps(calories),
        'max_continuous': max_continuous
    }

    return render(request, 'meal/meal_history.html', context)

def meal_detail(request, date):
    id = request.user.id

    # 유저별 권장 영양섭취 계산
    user_info = UsersAppUser.objects.filter(id=id).first()

    user_height = user_info.user_height
    user_weight = user_info.user_weight
    user_gender = user_info.user_gender

    user_birth_date = user_info.user_birth
    current_date = datetime.now()

    # 나이 계산
    user_age = current_date.year - user_birth_date.year - ((current_date.month, current_date.day) < (user_birth_date.month, user_birth_date.day)) -1

    # print('나이 : ' ,user_age)

    if user_gender == 0:
        user_bmr = 88.362 + (13.397 * user_weight) + (4.799 * user_height) - (5.677 * user_age)
    elif user_gender == 1:
        user_bmr = 447.593  + (9.247 * user_weight) + (3.098 * user_height) - (4.330 * user_age)
    else:
        user_bmr = 0.0
    
    # 활동 수준에 따른 BMR 값 변화
    user_activity = user_info.user_activity

    if user_activity == "5":
        user_tdee = user_bmr * 1.2
    elif user_activity == "4":
        user_tdee = user_bmr * 1.375
    elif user_activity == "3":
        user_tdee = user_bmr * 1.55
    elif user_activity == "2":
        user_tdee = user_bmr * 1.725
    elif user_activity == "1":
        user_tdee = user_bmr * 1.9
    else:
        user_tdee = 0.0

    # 단백질 총 칼로리의 10-35%
    protein_min, protein_max = user_tdee * 0.10/4 , user_tdee * 0.35 / 4
    # 지방 : 총 칼로리의 20-35 % 
    fat_min, fat_max = user_tdee * 0.20 / 9, user_tdee * 0.35 / 9
    # 탄수화물 : 총 칼로리의 45~65%
    carbs_min, carbs_max = user_tdee * 0.45 / 4, user_tdee * 0.65 / 4
    # 당류 에너지 섭취의 10% 미만
    sugar_max = user_tdee * 0.10 / 4
    # 식이섬류 하루에 25~30g 권장
    fiber_recommended = 25 if user_gender == 1 else 30  # 여성의 경우 25g, 남성의 경우 30g
    # 나트륨 : 1500mg 권장
    natrium_recommended = 1500  # mg   

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
    meal_info = {'아침': {'foods': [], 'calories': 0, 'nutrients': defaultdict(float)},
                 '점심': {'foods': [], 'calories': 0, 'nutrients': defaultdict(float)},
                 '저녁': {'foods': [], 'calories': 0, 'nutrients': defaultdict(float)},
                 '간식': {'foods': [], 'calories': 0, 'nutrients': defaultdict(float)}}


    for meal in meals:
        meal_info_list = ast.literal_eval(meal.meal_info)

        for info in meal_info_list:
            menu = CalorieDictionary.objects.filter(food_code=info).first()

            if menu is not None:
                meal_info[meal.meal_type]['foods'].append(menu.food_name)
                meal_info[meal.meal_type]['calories'] += menu.calories
                meal_info[meal.meal_type]['nutrients']['protein'] += menu.protein
                total_protein += menu.protein
                meal_info[meal.meal_type]['nutrients']['fat'] += menu.fat
                total_fat += menu.fat
                meal_info[meal.meal_type]['nutrients']['carbohydrate'] += menu.carbohydrate
                total_carbs += menu.carbohydrate
                meal_info[meal.meal_type]['nutrients']['suger'] += menu.suger
                total_sugar += menu.suger
                meal_info[meal.meal_type]['nutrients']['dietary_fiber'] += menu.dietary_fiber
                total_fiber += menu.dietary_fiber
                meal_info[meal.meal_type]['nutrients']['natrium'] += menu.natrium
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
        'date': date,
        'meal_info': meal_info,
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
    print(search_query)

    # 대분류, 소분류 항목을 가져와 option 태그에서 for문을 돌려 노출시킨다.
    major_classes = CalorieDictionary.objects.filter(Q(food_name__icontains=search_query)
                                                      | Q(maker__icontains=search_query)).values_list('major_class', flat=True).distinct()
    detail_classes = CalorieDictionary.objects.filter(Q(food_name__icontains=search_query)
                                                       | Q(maker__icontains=search_query)).values_list('detail_class', flat=True).distinct()

    # form name=majorClass, detailClass 인 항목을 가져온다.
    major_class_filter = request.GET.get('majorClass', '')
    print(major_class_filter)
    detail_class_filter = request.GET.get('detailClass', '')
    print(detail_class_filter)
    
    # 각 항목에 맞는 데이터를 필터해온다. 
    if major_class_filter:
        cal_data = cal_data.filter(major_class=major_class_filter)
    if detail_class_filter:
        cal_data = cal_data.filter(detail_class=detail_class_filter)

    # 검색 키워드 개수에 따라 다르게 굴러간다.
    # try except 구문은 크게 필요 없어보이는데, 없으면 오류가 난다.
    try:
        keywords = search_query.split()
        print(keywords)
        if len(keywords)>=2:
            q_obj = Q()

            q_obj |= Q(food_name__icontains=keywords[0]) & Q(maker__icontains=keywords[1])

            print(q_obj)
        
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

    return render(request, 'meal/calorie_dictionary.html', {
        'current_page_data':curruent_page_data,
        'page_range':page_range,
        'major_classes':major_classes,
        'detail_classes':detail_classes,
        'search_query': search_query,
        'major_class_filter': major_class_filter,
        'detail_class_filter': detail_class_filter,
        })

# 칼로리 사전에 걸린 링크 기본키로 음식 상세정보 출력
def food_detail(request, food_code):
    food = get_object_or_404(CalorieDictionary, pk=food_code)
    return render(request, 'meal/calorie_dict_detail.html', {'food':food})

# 분석화면에서 검색어 입력하면 검색 후보군 띄워주는 함수
@require_GET
def food_search(request):
    search_word = request.GET.get('searchWord', '')
    # print(search_word)

    results = CalorieDictionary.objects.filter(food_name__icontains=search_word)[:10]
    
    data = {'results': [{'food_code': result.food_code, 'name': result.food_name, 'maker': result.maker} for result in results]}

    return JsonResponse(data)

# 본격적인 식단 POST 함수
@csrf_exempt
def meal_post(request):
    if request.method == "POST":
        meal_data_list = json.loads(request.POST.get('meal_data'))
        print(meal_data_list[0]) # 리스트를 제대로 받아온다
        print(meal_data_list[-1])

        filtered_list = []

        for food in meal_data_list[0]:
            # 정규성 검사 함수
            food_code = check_food_code(food)
            if food_code is not None:
                filtered_list.append(food_code)
        
        # 리스트 제대로 변환되어 출력된다.
        print(filtered_list)

        # 칼로리 합산하는 함수
        meal_calories, nutrient_info = total_calories(filtered_list)
        print(meal_calories)
        print(nutrient_info)

        if request.user.is_authenticated:
            # print(user_id) 유저 id도 제대로 받아온다. bigint 값이다.
            user_instance = UsersAppUser.objects.get(id=request.user.id)

            # 현재 시간 얻기
            current_time = timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone())
            # print(current_time.hour)

            # 테스트를 위한 임의 조작 시간
            # current_time = datetime(2021, 8, 31, 23, 30, 11)

            # 이건 꼼수인데, UTC로 저장되는 시간에 억지로 9시간을 추가해 저장하는 수법이다.
            # 좀 짜증나지만, 이럴 경우 korea_time 변수에 담긴 시간은 한국 시간에서 9시간이 추가된 시간이다.
            plus_9 = timedelta(hours=9)
            korea_time = current_time + plus_9
            print(current_time)
            print(korea_time.strftime("%Y-%m-%d %H:%M:%S"))

            
            # 아침, 점심, 저녁, 간식 출력
            if 6 <= current_time.hour <= 9:
                meal_type = "아침"
            elif 11 <= current_time.hour <= 14:
                meal_type = "점심"
            elif 18 <= current_time.hour <= 20:
                meal_type = "저녁"
            else:
                meal_type = "간식"

            print(meal_type)
            
            Meal.objects.create(
                user = user_instance,
                # meal_date = current_time.strftime("%Y-%m-%d %H:%M:%S"),
                meal_date = korea_time,
                meal_photo = meal_data_list[-1],
                meal_info = json.dumps(filtered_list),
                meal_type = meal_type,
                meal_calories = meal_calories,
                nutrient_info = json.dumps(nutrient_info)
            )

            # return JsonResponse({'success': True, 'meal_calories': meal_calories, 'nutrient_info': nutrient_info})
            # ajax로 html 낑겨넣는 수법을 써 봐야겠다.
            # 이러면 장점이 html에서 장고 문법 사용이 가능해진다.

            # 그런데.... 이 함수 블록에서 해야되는 일이 너무 많아지는 게 흠이다.
            return render(request, 'meal/meal_nutrient.html', {'meal_cal': meal_calories, 'nutrient': nutrient_info})
        else:
            return JsonResponse({'success': False, 'error': "올바르지 않은 데이터 형식"})
    else:
        return JsonResponse({'success': False, 'error': "올바르지 않은 요청사항"})

def test(request):
    user_id = 4

    user_meal = Meal.objects.filter(user=user_id).values_list()
    print(user_meal.values())
    return render(request, 'meal/test.html', {'testDB': user_meal})