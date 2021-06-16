from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required # 데코레이터 사용
from django.contrib import messages

from .forms import EvalForm
from accounts.models import User
from lectures.models import Lectures
from .models import Evals

# 글 작성하기
@login_required(login_url= '/accounts/login')
def create(request, num):
    if request.method == "POST":
        form = EvalForm(request.POST)
        if form.is_valid():
            eval = form.save(commit=False) # 일단 DB에 저장하지 않고
            eval.lect_id = get_object_or_404(Lectures, pk=num) # 강의 정보를 가져와 넣어주고
            eval.author = User.objects.get(user_id=request.user.get_username()) # 글 작성을 요청한 사용자 넣어주고
            eval.eval_date = timezone.datetime.now() # 현재 시간 넣어주고
            eval.hw_level = request.POST['hw_level'] # 과제 난이도 넣어주고
            eval.test_level = request.POST['test_level'] # 시험 난이도 넣어주고
            eval.lect_power = request.POST['lect_power'] # 강의력까지 넣어주고
            eval.save() # db에 저장
        return redirect('detail', num) # 저장되면 강의 자세히 보기 페이지로 이동
    else:
        try: # 강의평을 작성하면 일단 요청한 사용자와 강의가 일치하는 강의평 가져오기
            user = request.user.get_username()
            lect = Lectures.objects.get(pk=num)
            Evals.objects.get(author=user, lect_id=lect)
            messages.warning(request, '강의평을 이미 작성했습니다.')
            return redirect('detail', num)
        except: # 강의평 가져오기가 실패하면.. 요청한 사용자는 강의평을 작성하지 않은 것. 강의평 작성 폼 띄우기
            form = EvalForm()
            return render(request, 'create.html', {'form': form})

# 글 삭제하기
@login_required(login_url= '/accounts/login')
def delete(request, eval_id):
    eval = get_object_or_404(Evals, pk=eval_id) # 삭제하려는 글이 없으면 404 오류를 내고, 있으면 가져오기

    if eval.author == request.user: # 본인이 작성한 글만 삭제 가능
        eval.delete()
        return redirect('mypage')
    else:
        messages.warning(request, "본인이 작성한 글만 삭제할 수 있습니다.")
        return redirect('/')

# 강의평 추천하기
@login_required(login_url= '/accounts/login')
def recommand(request, eval_num, lect_num):
    eval = get_object_or_404(Evals, pk=eval_num)
    lect = Lectures.objects.get(pk=lect_num)

    if request.user != eval.author: # 자기가 쓴 글은 추천할 수 없음.
        eval.counts += 1 # 해당 함수가 실행되면 count가 1 증가
        eval.save() # 저장을 해주어야만 DB에 반영!!
    else:
        messages.warning(request, "본인이 작성한 글은 추천할 수 없습니다.")
        
    lect.hit -= 1 # 강의평 추천이 성공적으로 이루어지면, 다시 detail 페이지를 띄우는데 이때 조회수가 증가하지 않도록 1을 빼주기
    lect.save()  
    return redirect('detail', lect_num)
    # 추천은 한 번만 할 수 있게 코드 고민하기