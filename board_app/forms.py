from django import forms
from .models import Community, Reply
from django.contrib.auth import get_user_model

# ModelForm 클래스 상속 받음
class BoardForm(forms.ModelForm):
    category = forms.ChoiceField(
        label="카테고리",
        choices=(("exercise", "운동"),("health","건강"),("meal","식단"),("disease","질병")),
        widget=forms.RadioSelect  # 라디오 버튼 형태로 선택하도록 설정
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BoardForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Community
        fields = (
            'title',
            'content',
            'category',
        )
        labels = {
            'title':'제목',
            'content':'내용',
            'category':'카테고리',
        }


    def save(self, commit=True):
        instance = super(BoardForm, self).save(commit=False)
        instance.user = self.user 
        if commit:
            instance.save()
        return instance    
    
class BoardCommentForm(forms.ModelForm):
    class Meta:
        model = Reply
        exclude = ('postnum', 'user')
        fields = ('reply',)  
        labels = {
            'reply': '댓글 내용',
        }