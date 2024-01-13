from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import UsersAppUser, User

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일", required=True)
    user_age = forms.DateField(label="연령", widget=forms.widgets.DateInput(attrs={'type':'date'}), required=True)
    user_gender = forms.ChoiceField(label="성별", choices=(("0", "남자"), ("1", "여자")))
    user_height = forms.IntegerField(label="키", max_value=300)
    user_weight = forms.IntegerField(label="몸무게", max_value=300)
    user_activity = forms.ChoiceField(label="활동수준", choices=(("active", "활동적"), ("deactive","비활동적")))

    class Meta:
        model = User

        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'user_age',
            'user_gender',
            'user_height',
            'user_weight',
            'user_activity',
        )