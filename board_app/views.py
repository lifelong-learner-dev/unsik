import json
from django.shortcuts import get_object_or_404, render, redirect
from .models import Community, UsersAppUser
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BoardForm, BoardCommentForm

# Create your views here.
def board_list(request):
    boards = Community.objects.all()
    return render(request, 'board_app/board_list.html', {'boards':boards, 'user': request.user})

# def book_detail(request,postnum):
#     # bookno 조건에 맞는 행 select
#     # get_object_or_404() 사용
#     board = get_object_or_404(Community, pk=postnum)
#     return render(request, 'board_app/board_detail.html', {'board':board})

def board_detail(request, postnum):
    board = get_object_or_404(Community, pk=postnum)
    comments = board.fk_reply_community.all()
    
    if request.method == "POST":
        form = BoardCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.board = board
            comment.user = request.user
            comment.save()
            return redirect('board_detail', postnum=postnum)
    else:
        form = BoardCommentForm()
    
    return render(request, 'board_app/board_detail.html', {'board': board, 'comments': comments, 'form': form})

@login_required
def board_insert(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            user_instance = UsersAppUser.objects.get(id=request.user.id)
            board = form.save(commit=False)
            board.user = user_instance  # 현재 로그인한 사용자의 인스턴스를 할당
            board.save()
            return redirect('board_list')
    else:
        form = BoardForm()
    return render(request, 'board_app/board_form.html', {'form': form})

    
@login_required
def board_update(request, postnum):
    # (1) 전달받은 bookno에 해당되는 상품 정보 가져와서
    book = get_object_or_404(Community, pk=postnum)
        # 유효성 검사 is_valid
    if request.method == "POST":
        # (3) 폼변수의 가져온 값(=book 데이터 내용)을 form 변수에 저장
        form = BoardForm(request.POST, instance=board)
        # (4) Django의 기본 기능은 is_valid()라는 메소드를 사용해서 데이터 유효성 확인
        # 마치 수학 공식과 같은 것
        if form.is_valid():
            # (5) form에 저장된 데이터를 아직 완전 저장안하고 
            # (참고로 현재는 이부분 없어도 됨)
            # book = form.save()
            
            board = form.save(commit=False)
            # commit = False 수행할 작업이 있다면 여기서 수행 (우리는 현대 자른 작업 없음)
            # book...() 작업
            # (6) 여기에서 DB에 저장할 것임.
            board.save()
            # (7) DB에 저장 후 결과 확인하기 위해 상품 조회 화면으로 이동 (포워딩)
            # redirect() 사용
            return redirect('book_list')
    else:
        form = BoardForm(instance=book) #처음 form 화면 출력
        # form의 bookno에 해당되는 상품 데이터 출력

    # (8) else : POST 요청이 아니라면 입력 폼 그대로 출력
    return render(request, 'board_app/board_update.html', {'form':form})

@login_required    
def board_delete(request, postnum):
    board = Community.objects.get(postnum=postnum)
    board.delete()
    return redirect('board_list')
    

def board_search_form(request):
    return render(request, 'board_app/board_search_form.html')


def board_search(request):
    if request.method == "POST":
        type = request.POST['type']
        keyword = request.POST['keyword']
        if type == "title":
            bd_list = Community.objects.filter(title__contains=keyword)
        elif type == "content":
            bd_list = Community.objects.filter(content__contains=keyword)
        else:
            return JsonResponse({'reload_all':False, 'bd_list_json':[]})
        
        bd_list_json = json.loads(serializers.serialize('json', bd_list, ensure_ascii=False))

        return JsonResponse({'reload_all':False, 'bd_list_json':bd_list_json})
    else:
        return render(request, 'board_app/board_search_form.html')
    
