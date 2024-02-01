from .models import Meal, UsersAppUser
from .models import CalorieDictionary
from .models import Menu
import ast

import pytz

from datetime import datetime, timedelta
from django.utils import timezone

def get_recommend_mealtype(id):

    # 일주일치 먹은 식사정보를 기반으로 어떤 식단을 추천해줄지 결정
    # settings.py USE_TZ = True
    # current_time = datetime.now(pytz.utc)

    # settings.py USE_TZ = False
    current_time = timezone.datetime.now()

    seven_days_ago = current_time - timedelta(days=7)

    meals = Meal.objects.filter(user_id=id, meal_date__gte=seven_days_ago).order_by('meal_date')

    # print('services meals : ', meals)

    total_protein = 0.0
    total_fat = 0.0
    total_carbs = 0.0
    total_sugar = 0.0
    total_fiber = 0.0
    total_natrium = 0.0

    for meal in meals:
        meal_info_list = ast.literal_eval(meal.meal_info)
        for code in meal_info_list:

            menu = CalorieDictionary.objects.filter(food_code=code).first()
            
            if menu is not None:
                total_protein += menu.protein
                total_fat += menu.fat
                total_carbs += menu.carbohydrate
                total_sugar += menu.suger
                total_fiber += menu.dietary_fiber
                total_natrium += menu.natrium

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
   
    recommended_weekly_sugar = 7 * nutrient_res["sugar_max"]

    recommended_weekly_natrium = 7 * nutrient_res["natrium_recommended"]

    if total_sugar > recommended_weekly_sugar:
        return '당뇨식'
    elif total_natrium < recommended_weekly_natrium:
        return '저염식'
    else:
        return '일반식'

# 유저 정보별로 영양소 권장 섭취 칼로리 계산
def get_personal_recommended_nutrient(user_height, user_weight, user_gender, user_age, user_activity):
    if user_gender == 0:
        user_bmr = 88.362 + (13.397 * user_weight) + (4.799 * user_height) - (5.677 * user_age)
    elif user_gender == 1:
        user_bmr = 447.593  + (9.247 * user_weight) + (3.098 * user_height) - (4.330 * user_age)
    else:
        user_bmr = 0.0
    
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
    
    res = {}
    
    # 단백질 총 칼로리의 10-35%
    res["protein_min"], res["protein_max"] = user_tdee * 0.10/4 , user_tdee * 0.35 / 4
    # 지방 : 총 칼로리의 20-35 % 
    res["fat_min"], res["fat_max"] = user_tdee * 0.20 / 9, user_tdee * 0.35 / 9
    # 탄수화물 : 총 칼로리의 45~65%
    res["carbs_min"], res["carbs_max"] = user_tdee * 0.45 / 4, user_tdee * 0.65 / 4
    # 당류 에너지 섭취의 10% 미만
    res["sugar_max"] = user_tdee * 0.10 / 4
    # 식이섬류 하루에 25~30g 권장
    res["fiber_recommended"] = 25 if user_gender == 1 else 30  # 여성의 경우 25g, 남성의 경우 30g
    # 나트륨 : 1500mg 권장
    res["natrium_recommended"] = 1500  # mg

    return res