# import pickle

# def load_calories_model(model_path='modules/calories_model.pkl'):
#     """
#     저장된 칼로리 예측 모델을 불러오는 함수.
#     """
#     with open(model_path, 'rb') as file:
#         model = pickle.load(file)
#     return model

# def predict_calories(exercise_type, exercise_duration, user_weight, model):
#     """
#     칼로리 소비량을 예측하는 함수.
#     """
#     # 모델에 전달할 입력 데이터 준비
#     input_data = [[exercise_type, exercise_duration, user_weight]]

#     # 예측 수행
#     predicted_calories = model.predict(input_data)
    
#     return predicted_calories[0]

# # 모델 불러오기 예제
# if __name__ == "__main__":
#     # 모델 불러오기
#     calories_model = load_calories_model()

#     # 예제 데이터로 예측 수행
#     exercise_type = '유산소'  # 예시 데이터, 실제 모델에 맞게 조정 필요
#     exercise_duration = 30  # 예시 데이터
#     user_weight = 70  # 예시 데이터

#     # 칼로리 소비량 예측
#     predicted_calories = predict_calories(exercise_type, exercise_duration, user_weight, calories_model)
#     print(f"예상 칼로리 소비량: {predicted_calories} kcal")

# from django.conf import settings
# import joblib

# def calories_model_load():
#     file_path = settings.BASE_DIR / 'exercise' / 'moduls'
#     loaded_model = joblib.load(file_path / 'calories_model.pkl')
#     pred = loaded_model.predict([input_data])

#     input_data = [[exercise_type, exercise_duration, user_weight]]
#     if pred[0] == 0:
#         result = 'setosa'
#     elif  pred[0] == 1:
#         result = 'versicolor'
#     else:
#         result = 'virginica'

#     return result

from django.conf import settings
import joblib
from pathlib import Path
import pandas as pd

def calories_model_load(age, height, weight, exercise_amount, gender_male, gender_female, heart_rate=110, body_temp=39):
    # 모델 파일 경로 구성
    file_path = settings.BASE_DIR / 'exercise' / 'moduls' / 'calories_model.pkl'
    
    # 모델 로드
    loaded_model = joblib.load(file_path)
    
    # 입력 데이터 준비
    input_data = {
        'Age': age,
        'Height': height,
        'Weight': weight,
        'Duration': exercise_amount,
        'Heart_Rate': heart_rate,  # 고정치
        'Body_Temp': body_temp,    # 고정치
        'Gender_female': gender_female,    
        'Gender_male': gender_male,
    }
    
    # 입력 데이터를 DataFrame으로 변환
    input_df = pd.DataFrame([input_data])
    
    # 모델을 사용하여 칼로리 예측
    predicted_calories = loaded_model.predict(input_df)
    
    return predicted_calories[0]
