from django.shortcuts import render, redirect, get_object_or_404
from .models import UsersAppUser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserForm

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