from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UsersAppUser, User, Daily

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일", required=True)
    user_birth = forms.DateField(label="생년월일", widget=forms.widgets.DateInput(attrs={'type':'date'}), required=True)
    user_gender = forms.ChoiceField(label="성별", choices=(("0", "남자"), ("1", "여자")), widget=forms.RadioSelect)
    user_height = forms.IntegerField(label="키", max_value=300)
    user_weight = forms.IntegerField(label="몸무게", max_value=300)
    user_activity = forms.ChoiceField(label="활동수준", choices=(("5", "매우 활발한 활동"),("4","활발한 활동"),("3","보통 활동"),("2","약간의 활동"), ("1","거의 활동이 없음")))
    user_target_weight = forms.IntegerField(label="목표몸무게", max_value=300)
    user_exercise_purpose = forms.ChoiceField(label="운동목적", choices=(("health", "건강"), ("bulkup", "벌크업"), ("diet", "다이어트")), widget=forms.RadioSelect)

    class Meta:
        model = User

        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'user_birth',
            'user_gender',
            'user_height',
            'user_weight',
            'user_activity',
            'user_target_weight',
            'user_exercise_purpose'
        )

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=commit)

        # Daily 레코드 생성
        if commit:
            Daily.objects.create(
                user=user,
                current_weight=user.user_weight,
                date=timezone.now().date()
            )

        return user
    

class MypageUserForm(forms.ModelForm):
    user_activity = forms.ChoiceField(
        label="활동수준",
        choices=(("5", "매우 활발한 활동"),("4","활발한 활동"),("3","보통 활동"),("2","약간의 활동"), ("1","거의 활동이 없음")),
        widget=forms.RadioSelect  # 라디오 버튼 형태로 선택하도록 설정
    )

    class Meta:
        model = User
        fields = (
            'user_height',
            'user_weight',
            'user_activity',
            'user_target_weight',
        )
        labels = {
            'user_height': '키',
            'user_weight': '몸무게',
            'user_activity': '활동수준',
            'user_target_weight': '목표몸무게',        
        }

    def save(self, commit=True):
        user = super(MypageUserForm, self).save(commit=commit)

        # Daily 레코드 생성
        if commit:
            Daily.objects.create(
                user=user,
                current_weight=user.user_weight,
                date=timezone.now().date()
            )

        return user