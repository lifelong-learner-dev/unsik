from django import forms
from .models import Exercise

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        exclude = ('user',)
        fields = (
            'exercise_date', 
            'exercise_type', 
            'exercise_name', 
            'exercise_amount', 
            'calories_burned',
            'weight', 
            'reps', 
            'sets'
        )

        labels = {
            'exercise_date': '운동시각',
            'exercise_type': '유산소 or 웨이트',
            'exercise_name': '운동명',
            'exercise_amount': '운동 지속 시간',
            'calories_burned': '칼로리 소모량',
            'weight': '무게',
            'reps': '횟수',
            'sets': '세트 수',
        }

        widgets = {
            'exercise_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        # 필요하다면 widgets 를 사용하여 HTML 입력 요소에 추가 속성을 지정할 수 있다.
        # 예: 
        # widgets = {
        #     'exercise_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['exercise_type'].widget = forms.RadioSelect(choices=[('유산소', '유산소'), ('웨이트', '웨이트')])

    #     # JavaScript에서 사용할 클래스 이름을 추가
    #     self.fields['exercise_type'].widget.attrs['class'] = 'exercise-type-field'

    # def clean(self):
    #     cleaned_data = super().clean()
    #     exercise_date = cleaned_data.get('exercise_date')
    #     exercise_type = cleaned_data.get('exercise_type')
    #     exercise_name = cleaned_data.get('exercise_name')
    #     exercise_amount = cleaned_data.get('exercise_amount')

    #     if not exercise_date or not exercise_type or not exercise_name or not exercise_amount:
    #         raise forms.ValidationError('빈칸을 입력해 주세요')
