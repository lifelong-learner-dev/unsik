# import joblib
from PIL import Image
import torch
from django.conf import settings
from ultralytics import YOLO

def predict_meal(image):
    food_cls = {0: '곰탕', 1: '도토리묵', 2: '콩나물국', 3: '비빔밥', 4: '연근조림', 5: '두부조림',
            6: '브로콜리', 7: '불고기', 8: '배추김치', 9: '된장찌개', 10: '조미김',
            11: '식빵', 12: '후라이드치킨', 13: '계란프라이', 14: '김밥', 15: '햄구이',
            16: '고등어구이', 17: '짜장면', 18: '메추리알장조림', 19: '잡곡밥', 20: '칼국수',
            21: '김치볶음밥', 22: '김치전', 23: '김치찌개', 24: '깍두기', 25: '깻잎',
            26: '상추', 27: '단무지', 28: '피자', 29: '라면', 30: '쌀밥',
            31: '콩나물무침', 32: '양념치킨', 33: '미역국', 34: '설렁탕', 35: '간장',
            36: '시금치나물', 37: '멸치볶음', 38: '제육볶음', 39: '오이소박이', 40: '수육',
            41: '고구마', 42: '토마토', 43: '떡볶이', 44: '육개장'}

    file_path = settings.BASE_DIR / 'meal' / 'modules'
    trained_model = YOLO(file_path / 'Unsik_Yolo_best.pt')
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