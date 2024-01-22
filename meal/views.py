from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import CalorieDictionary
from .modules.meal_anal import predict_meal
from django.db.models import Q
from uuid import uuid4

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
                meal_info[meal.meal_type]['nutrients']['fat'] += menu.fat
                meal_info[meal.meal_type]['nutrients']['carbohydrate'] += menu.carbohydrate
                meal_info[meal.meal_type]['nutrients']['suger'] += menu.suger
                meal_info[meal.meal_type]['nutrients']['dietary_fiber'] += menu.dietary_fiber
                meal_info[meal.meal_type]['nutrients']['natrium'] += menu.natrium
                
    context = {
        'date': date,
        'meal_info': meal_info,
    }

    return render(request, 'meal/meal_detail.html', context)

# 이미지 파일명에 고유번호를 부여해주는 함수
def rename_imagefile_to_uuid(filename):
    ext = filename.split('.')[-1]
    uuid = uuid4().hex

    filename = '{}.{}'.format(uuid, ext)

    return filename

# 예측 함수
def meal_to_analyze(request):
    if request.method == 'POST':
        meal_img = request.FILES.get('fileUpload')
        # print(meal_img.name)

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        file_name = rename_imagefile_to_uuid(meal_img.name)
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

# def upload_and_detect(request):
#     if request.method == 'POST':
#         image = request.FILES.get('fileUpload')
    

#     return True