from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import IntegrityError
from .models import UsersAppUser

def show_main(request):
    return render(request, "main.html")

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
    return render(request, "sign_up.html")

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