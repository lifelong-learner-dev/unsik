from .models import CalorieDictionary, UsersAppUser
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
    "쌀밥": "D018226",
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
def nutrient_quotes(id, current_time, todays_calorie, todays_nutrients):
    # todays_nutrients의 길이는 8이다.

    natrium_today = todays_nutrients[4]
    dietary_fiber_today = todays_nutrients[-1]
    five_nut_list = todays_nutrients.copy()

    # 이 중 index 4, index 7은 나트륨과 식이섬유이므로 비율 계산에서 빠진다.
    del five_nut_list[4]
    del five_nut_list[-1]

    nurtient_proportion = []
    for nutrient in five_nut_list:
        nurtient_proportion.append(round(float(nutrient) / sum(five_nut_list) * 100, 2))

    # user_daily_calorie 값이 곧 max 값이 된다.
    user_info = UsersAppUser.objects.filter(id=id).first()

    # 1. max 칼로리 구하는 공식. 몸무게, 키, 나이 필요
    user_weight = user_info.user_weight
    user_height = user_info.user_height

    # 1-1 나이 구하기
    user_birth_date = user_info.user_birth
    user_age = current_time.year - user_birth_date.year - ((current_time.month, current_time.day) < (user_birth_date.month, user_birth_date.day)) -1
    
    print(user_age)

    # 유저가 남자라면
    if user_info.user_gender == 0:
        user_base_calorie = (10 * user_weight) + (6.25 * user_height) - (5 * user_age) + 5
    else:
        # 여자라면
        user_base_calorie = (10 * user_weight) + (6.25 * user_height) - (5 * user_age) - 161

    print(f"유저 기초대사량 : {user_base_calorie}")

    # 활동계수 곱
    if user_info.user_activity == "1":
        user_max_calorie = user_base_calorie * 1.2
    elif user_info.user_activity == "2":
        user_max_calorie = user_base_calorie * 1.375
    elif user_info.user_activity == "3":
        user_max_calorie = user_base_calorie * 1.55
    elif user_info.user_activity == "4":
        user_max_calorie = user_base_calorie * 1.725
    else:
        user_max_calorie = user_base_calorie * 1.725

    print(f"유저 기본 칼로리 : {user_max_calorie}")

    user_exercise_purpose = user_info.user_exercise_purpose

    print("유저 운동 목표 : ", user_exercise_purpose)

    if user_exercise_purpose == "bulkup":
        user_max_calorie = round(user_max_calorie * 1.2, 2)
    if user_exercise_purpose == "diet":
        user_max_calorie = round(user_max_calorie * 0.8, 2)

    print(f"유저 목표 칼로리 : {user_max_calorie}")

    warnings_dict = {}

    if not 7 <= current_time.hour < 20:
        time_warning = "불규칙한 식사는 건강에 좋지 않아요."
        if current_time.hour < 7:
            time_warning += " 새벽 시간에 음식 섭취를 피해주세요."
            warnings_dict["식사 시간"] = time_warning
        if current_time.hour > 20:
            time_warning += " 가급적 저녁 8시 이전까지 식사를 마쳐주세요."
            warnings_dict["식사 시간"] = time_warning

    if todays_calorie > user_max_calorie:
        calorie_quote = "하루 권장량보다 많이 드셨어요!"

        # 만약 목표가 체중 감량이라면
        if user_exercise_purpose == "diet":
            calorie_quote += " 고열량 식품, 과식을 주의해주세요."

        warnings_dict["칼로리"] = calorie_quote

    # 탄수화물
    if nurtient_proportion[0] < 40:
        carbohydrate_quote = "탄수화물 비중이 40% 이하에요. 부족한 탄수화물은 일상생활에 지장을 줄 수 있어요."
        warnings_dict["탄수화물"] = carbohydrate_quote
    elif nurtient_proportion[0] > 55:
        carbohydrate_quote = "탄수화물 비중이 55% 이상입니다!"

        # 만약 목표가 체중 감량이라면
        if user_exercise_purpose == "diet":
            carbohydrate_quote += " 탄수화물 과다 섭취는 비만의 원인이에요."
        
        #만약 목표가 벌크업이라면
        if user_exercise_purpose == "bulkup":
            carbohydrate_quote += " 적정 칼로리 내에서 밥이나 빵을 줄여보세요."

        warnings_dict["탄수화물"] = carbohydrate_quote

    # 단백질
    if nurtient_proportion[1] < 7:
        protein_quote = "단백질 비중이 7% 이하에요. 부족한 단백질은 신체 활동에 좋지 않아요."

        # 만약 목표가 벌크업이라면
        if user_exercise_purpose == "bulkup":
            protein_quote += " 충분한 단백질이 멋진 근육을 만들어요."
        warnings_dict["단백질"] = protein_quote

    elif nurtient_proportion[1] > 20:
        protein_quote = "단백질 비중이 20% 이상입니다! 과도한 단백질 섭취는 칼슘을 배출하여 뼈와 신장을 약화시켜요."
        warnings_dict["단백질"] = protein_quote

    # 지방
    if nurtient_proportion[2] > 30:
        fat_quote = "지방 비중이 30% 이상입니다! 하루 권장량 이상 섭취하면 비만과 고혈압을 유발할 수 있어요."

        # 만약 목표가 체중 감량이라면
        if user_exercise_purpose == "diet":
            fat_quote += " 지방을 줄이고 단백질 비중을 늘려 꾸준히 운동해보세요!"

        warnings_dict["지방"] = fat_quote

    # 나트륨
    if natrium_today > 2300:
        natrium_quote = "나트륨 섭취량이 너무 높아요! 성인병 예방을 위해 하루 권장량 2300mg 이하로 낮춰주세요."
        warnings_dict["나트륨"] = natrium_quote

    # 당
    if nurtient_proportion[3] > 20:
        suger_quote = "당 비중이 20% 이상입니다! 당뇨병 환자라면 주의해주세요."
        warnings_dict["당"] = suger_quote

    # 포화지방
    if nurtient_proportion[4] > 7:
        sfat_quote = "포화지방 비중이 7% 이상입니다! 성인병 예방을 위해 가급적 낮추는 것이 좋아요. 불포화지방이나 단백질로 대체해보세요."
        warnings_dict["포화지방"] = sfat_quote

    # 트랜스지방
    if nurtient_proportion[5] > 1:
        tfat_quote = "트랜스지방 비중이 1% 이상으로 높아요! 패스트푸드나 튀긴 음식은 주의해주세요."
        warnings_dict["트랜스지방"] = tfat_quote

    # 식이섬유
    if dietary_fiber_today < 23:
        dietary_fiber_quote = "식이섬유 섭취량이 23g 이하입니다."

        # 단백질 비중이 20% 이상일 경우
        if nurtient_proportion[1] > 20:
            dietary_fiber_quote += " 육류를 줄이고 채소 식단을 구성해보아요."

        # 당 비중이 20% 이상일 경우
        if nurtient_proportion[3] > 20:
            dietary_fiber_quote += " 주스나 잼보다 생과일을 섭취해보아요."

        warnings_dict["식이섬유"] = dietary_fiber_quote
    
    print(f"적정 칼로리 : {user_max_calorie}")
    print(f"영양소 비율 : {nurtient_proportion}")
    print(f"주의 경고 : {warnings_dict}")

    # 돌려줄 값 :
    # 전체 비율 리스트, 위험 감지된 경고문, max 칼로리 값
    return nurtient_proportion, warnings_dict, user_max_calorie