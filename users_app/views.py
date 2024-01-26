from django.shortcuts import render, redirect, get_object_or_404
from .models import User, UsersAppUser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserForm, MypageUserForm

# Create your views here.
# 로그인, 회원가입 전용 함수
def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')
    
    return render(request, 'main.html')

def sign_out(request):
    logout(request)
    return redirect('main')

def sign_up(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main')
    else:
        form = UserForm()

    return render(request, "users_app/sign_up.html", {'form': form})

def id_check(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username', None)
            if username:
                if UsersAppUser.objects.filter(username=username).exists():
                    return JsonResponse({'is_taken':True})
                else:
                    return JsonResponse({'is_taken':False})
        except IntegrityError:
            return redirect('sign_up')

    else:
        return JsonResponse({'error':'올바르지 않은 형식입니다.'})

# def password_check(request):
#     if request.method == 'POST':
#         form = PasswordCheckForm(request.POST)

#         if form.is_valid():
#             password = form.cleaned_data['password']
#             password_check = form.cleaned_data['confirm']
    

def my_page(request, username):

    my_page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    return render(request, "users_app/my_page.html", {"my_page_user":my_page_user,})

def my_page_update(request, username):
    # (1) 전달받은 username에 해당되는 상품 정보 가져와서
    user = get_object_or_404(User, username=username)
        # 유효성 검사 is_valid
    if request.method == "POST":
        # (3) 폼변수의 가져온 값(=user 데이터 내용)을 form 변수에 저장
        form = MypageUserForm(request.POST, instance=user)
        # (4) Django의 기본 기능은 is_valid()라는 메소드를 사용해서 데이터 유효성 확인
        # 마치 수학 공식과 같은 것
        if form.is_valid():
            # (5) form에 저장된 데이터를 아직 완전 저장안하고 
            # (참고로 현재는 이부분 없어도 됨)
            # user = form.save()
            
            user = form.save(commit=True)
            # commit = False 수행할 작업이 있다면 여기서 수행 (우리는 현대 자른 작업 없음)
            # user...() 작업
            # (6) 여기에서 DB에 저장할 것임.
            user.save()
            # (7) DB에 저장 후 결과 확인하기 위해 상품 조회 화면으로 이동 (포워딩)
            # redirect() 사용
            return redirect('my_page', username=user.username)
    else:
        form = MypageUserForm(instance=user) #처음 form 화면 출력
        # form의 user에 해당되는 데이터 출력

    # (8) else : POST 요청이 아니라면 입력 폼 그대로 출력
    return render(request, 'users_app/my_page_update.html', {'form':form})

