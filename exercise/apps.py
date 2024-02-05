from django.apps import AppConfig
import joblib

class ExerciseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exercise"
    model = None  # 모델 인스턴스를 저장할 변수 초기화

    def ready(self):
        # 모델 파일의 경로 지정
        model_path = 'exercise/moduls/calories_model.pkl'
        # Django 앱이 준비되면 모델을 로드
        if not self.model:
            self.model = joblib.load(model_path)
