from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import CalorieDictionary, Meal
from .modules.meal_anal import predict_meal
from .foodDict import check_food_code
from django.db.models import Q
from uuid import uuid4
import json

# Create your views here.

def meal_index(request):
    return render(request, 'meal/meal_index.html' )

def meal_analyze(request):
    return render(request, 'meal/meal_analyze.html')

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

@require_GET
def food_search(request):
    search_word = request.GET.get('searchWord', '')
    # print(search_word)

    results = CalorieDictionary.objects.filter(food_name__icontains=search_word)[:10]
    
    data = {'results': [{'food_code': result.food_code, 'name': result.food_name, 'maker': result.maker} for result in results]}

    return JsonResponse(data)

@csrf_exempt
def meal_post(request):
    if request.method == "POST":
        meal_data_str = request.POST.get('meal_data')
        meal_data_list = json.loads(meal_data_str)
        print(meal_data_list) # 리스트를 제대로 받아온다

        filtered_list = []

        for food in meal_data_list:
            # print(food)
            food_code = check_food_code(food)
            if food_code is not None:
                filtered_list.append(food_code)
        
        # 현 단계에서 함수가 안 돌아가고 있다. 내부 문제가 있는 건가?
        print(filtered_list)

        if request.user.is_authenticated:
            user_id = request.user.id
            # print(user_id) 유저 id도 제대로 받아온다. bigint 값이다.
            pass

        # meal = Meal.objects.create(data=meal_data)