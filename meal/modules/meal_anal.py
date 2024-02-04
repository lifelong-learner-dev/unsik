# import joblib
from PIL import Image
import torch
from django.conf import settings
from ultralytics import YOLO

def predict_meal(image):
    food_cls = {0: '곰탕', 1: '도토리묵', 2: '콩나물국', 3: '비빔밥', 4: '연근조림', 5: '두부조림',
                6: '브로콜리', 7: '불고기', 8: '배추김치', 9: '탕수육', 10: '된장찌개', 11: '조미김',
                12: '계란국', 13: '식빵', 14: '후라이드치킨', 15: '계란프라이', 16: '김밥', 17: '햄구이',
                18: '고등어구이', 19: '짜장면', 20: '메추리알장조림', 21: '잡곡밥', 22: '칼국수', 23: '김치볶음밥',
                24: '김치전', 25: '김치찌개', 26: '깍두기', 27: '깻잎', 28: '상추', 29: '단무지', 30: '피자',
                31: '라면', 32: '쌀밥', 33: '콩나물무침', 34: '양념치킨', 35: '미역국', 36: '설렁탕', 37: '간장',
                38: '시금치나물', 39: '멸치볶음', 40: '제육볶음', 41: '오이소박이', 42: '수육', 43: '고구마',
                44: '토마토', 45: '떡볶이', 46: '육개장'}

    file_path = settings.BASE_DIR / 'meal' / 'modules'
    trained_model = YOLO(file_path / 'Unsik_Yolo_best2.pt')
    img = Image.open(image)
    # print(img)

    results = trained_model.predict(img)

    for result in results:
        class_num = result.boxes.cls.tolist()
        box_xywhn = result.boxes.xywhn.tolist()
    
    detections = {}
    i = 1

    # 클래스 번호에 따라 {음식명: [좌표값]} 으로 묶어주는 for문
    # 1차적인 문제는 해결했다. 논리가 제대로 동작 하나 살펴보자.
    for cls, coords in zip(class_num, box_xywhn):
        if food_cls[cls] in detections.keys():
            class_name = food_cls[cls] + str(i)
            i += 1
            detections[class_name] = coords
        else:
            detections[food_cls[cls]] = coords

    # print(detections)

    return detections