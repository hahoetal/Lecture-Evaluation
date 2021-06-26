from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required # 데코레이터 사용
from django.contrib import messages
from django.db import connection # djanog ORM 대신 SQL문 사용하기

from .forms import EvalForm

# 글 작성하기
@login_required(login_url= '/accounts/login')
def create(request, num):
    if request.method == "POST":
        form = EvalForm(request.POST)
        if form.is_valid():
            user = request.user.get_username()
            date = timezone.datetime.now()
            content = request.POST['content']
            hw_lv = request.POST['hw_level']
            test_lv = request.POST['test_level']
            lect_power = request.POST['lect_power']

            try:
                cursor = connection.cursor()
                strSQL = f"INSERT INTO Evals VALUES(NULL, '{num}', '{user}', '{date}', '{content}', '{hw_lv}', '{test_lv}', '{lect_power}', default)"
                # 강의평 정보 입력
                cursor.execute(strSQL)
                connection.close()
            except:
                messages.error("저장에 실패했습니다.")
            
            return redirect('detail', num) # 강의 자세히 보기 페이지로 이동
    else:
        user = request.user.get_username()
            
        cursor = connection.cursor()
        strSQL = f"SELECT num FROM Evals WHERE author = '{user}' and lect_id = '{num}'"
        # 강의평 작성을 요청한 사용자와 강의 번호가 일치하는 강의평 조회
        cursor.execute(strSQL)
        result = cursor.fetchone()
        connection.close()

        if result != None: # 이미 강의평을 작성한 경우, 오류 메시지 띄우기
            messages.warning(request, '강의평을 이미 작성했습니다.')
            return redirect('detail', num)
        else: # 강의평을 작성한 적이 없으면 강의평 작성 폼 띄우기
            form = EvalForm()
            return render(request, 'create.html', {'form': form})

# 평가글 삭제하기
@login_required(login_url= '/accounts/login')
def delete(request, eval_id):
    try:
        cursor = connection.cursor()
        strSQL1 = f"SELECT author FROM Evals WHERE num = '{eval_id}'" # 요청한 강의평 번호와 일치하는 강의평 조회
        strSQL2 = f"DELETE FROM Evals WHERE num = '{eval_id}'" # 요청한 강의평 번호와 일치하는 강의평 삭제
        cursor.execute(strSQL1)
        result = cursor.fetchone()

        if result[0] == request.user.get_username():
            cursor.execute(strSQL2)
            connection.close()
            return redirect('mypage')
        else:
            messages.warning(request, "본인이 작성한 글만 삭제할 수 있습니다.")
            connection.close()
            return redirect('/')
    except:
        messages.error(request, '삭제에 실패했습니다.')
        return redirect('/')

# 강의평 추천하기
@login_required(login_url= '/accounts/login')
def recommand(request, eval_num, lect_num):
    try:
        cursor = connection.cursor()
        strSQL1 = f"SELECT author FROM Evals WHERE num = '{eval_num}'" # 추천을 누른 강의평의 작성자 조회
        strSQL2 = f"UPDATE Evals SET counts = counts + 1 WHERE num = '{eval_num}'" # 추천 수 증가
        strSQL3 = f"UPDATE Lectures SET hit = hit - 1 WHERE num = '{lect_num}'" # 조회수 감소, 추천에 성공하면 detail 페이지로 이동하고, 그와 동시에 조회수가 증가하기 때문..
        cursor.execute(strSQL1)
        result = cursor.fetchone()

        if request.user.get_username() != result[0]:
            cursor.execute(strSQL2)
        else:
            messages.warning(request, "본인이 작성한 글은 추천할 수 없습니다.")

        cursor.execute(strSQL3)
        connection.close()
    except:
        messages.error(request, "강의평 추천에 실패했습니다.")
    
    return redirect('detail', lect_num)
    # 추천은 한 번만 할 수 있게 코드 고민하기