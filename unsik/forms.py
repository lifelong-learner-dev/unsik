from django import forms
from .models import UsersAppUser

class UserForm(forms.ModelForm):
    class Meta:
        model = UsersAppUser

        fields = (
            'username',
            'email',
            'password',
            'user_age',
            'user_gender',
            'user_height',
            'user_weight',
            'user_activity',
        )

        labels = {
            'username': '아이디',
            'email': '이메일',
            'password': '비밀번호',
            'user_age': '나이',
            'user_gender': '성별',
            'user_height': '키',
            'user_weight': '몸무게',
            'user_activity': '활동량',
        }