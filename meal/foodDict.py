from .models import CalorieDictionary
from django.db.models import Q
import json
import re

allFoodDict = {
    "곰탕": "D018056",
    "도토리묵": "D018346",
    "콩나물국": "D018103",
    "비빔밥": "D018204",
    "연근조림": "D018450",
    "두부조림": "D018436",
    "브로콜리": "R000988",
    "불고기": "D018039",
    "배추김치": "D018116",
    "된장찌개": "D018480",
    "조미김": "D018045",
    "식빵": "D018312",
    "후라이드치킨": "D018547",
    "계란프라이": "P035755",
    "김밥": "D018190",
    "햄구이": "D018052",
    "고등어구이": "D018018",
    "짜장면": "D018180",
    "메추리알장조림": "D018439",
    "잡곡밥": "D018220",
    "칼국수": "D018183",
    "김치볶음밥": "D018192",
    "김치전": "D018401",
    "김치찌개": "D000385",
    "깍두기": "D018111",
    "깻잎": "R000853",
    "상추": "R001016",
    "단무지": "D018389",
    "피자": "D000297",
    "라면": "D018163",
    "쌀밥": "R000062",
    "콩나물무침": "D018152",
    "양념치킨": "D000475",
    "미역국": "D018071",
    "설렁탕": "D018083",
    "간장": "P014894",
    "시금치나물": "D018141",
    "멸치볶음": "D018263",
    "제육볶음": "D018288",
    "오이소박이": "D018123",
    "수육": "D018516",
    "고구마": "R000452",
    "토마토": "R001224",
    "떡볶이": "D018256",
    "육개장": "D018099",
}

def check_food_code(food_name):
    # 정규식을 사용하여 알파벳 대문자 + 숫자 여섯 자리 패턴을 찾는다
    match = re.search(r"[A-Z]\d{6}", food_name)
    
    if match:
        return match.group()
    else:
        # 만약 정규식에 부합하지 않는다면 그대로 돌려보낸다
        food_name = ''.join([i for i in food_name if not i.isdigit()])
        food_code = allFoodDict.get(food_name)

        # print(food_code)
        if food_code is not None:
            return food_code

# DB에서 칼로리 합산해주는 함수
def total_calories(food_code_list):
    total_calorie = 0

    total_carbohydrate = 0
    total_protein = 0
    total_suger = 0
    total_natrium = 0
    total_sfa = 0
    total_fat = 0
    total_tfa = 0
    total_dietary_fiber = 0

    try:
        for fcode in food_code_list:
            food_info = CalorieDictionary.objects.get(food_code=fcode)
            food_calorie = food_info.calories
            food_carbohydrate = food_info.carbohydrate
            food_protein = food_info.protein
            food_suger = food_info.suger
            food_natrium = food_info.natrium
            food_sfa = food_info.total_sfa
            food_fat = food_info.fat
            food_tfa = food_info.total_tfa
            food_dietary_fiber = food_info.dietary_fiber
            
            # print(food_calorie)
            total_calorie += food_calorie
            total_carbohydrate += food_carbohydrate
            total_protein += food_protein
            total_suger += food_suger
            total_natrium += food_natrium
            total_sfa += food_sfa
            total_fat += food_fat
            total_tfa += food_tfa
            total_dietary_fiber += food_dietary_fiber

    except food_info.DoesNotExist:
        print("DB에 없는 기본키입니다.")

    total_nutrient_list = [total_carbohydrate, total_protein, total_fat, total_suger,
                           total_natrium, total_sfa, total_tfa, total_dietary_fiber]

    return total_calorie, total_nutrient_list

# DB에서 음식코드로 검색한 값만 돌려주는 함수
def each_food_nutrients(food_code_list):
    # 함수 작성 중
    pass