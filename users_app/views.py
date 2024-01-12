from django.shortcuts import render, redirect
from .models import User, UsersAppUser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
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
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_age = request.POST['user_age']
        user_gender = request.POST['user_gender']
        user_height = request.POST['user_height']
        user_weight = request.POST['user_weight']
        user_activity = request.POST['user_activity']

        user = User.objects.create_user(username, email, password, user_age=user_age, user_gender=user_gender)
        user.user_height = user_height
        user.user_weight = user_weight
        user.user_activity = user_activity
        
        user.save()
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