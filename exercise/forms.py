from django import forms
from .models import Exercise

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['exercise_date', 'exercise_type', 'exercise_name', 'exercise_amount', 'weight', 'reps', 'sets']
        # 필요하다면 widgets 를 사용하여 HTML 입력 요소에 추가 속성을 지정할 수 있다.
        # 예: 
        # widgets = {
        #     'exercise_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        # }
