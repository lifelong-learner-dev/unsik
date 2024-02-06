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
