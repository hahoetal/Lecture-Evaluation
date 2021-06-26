from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator # 페이지네이션
from django.contrib import messages
from django.contrib.auth.decorators import login_required # 데코레이터 사용
from django.db import connection # djanog ORM 대신 SQL문 사용하기

# 강의 목록 페이지 띄우기
def LectureListPage(request):
    try:
        cursor = connection.cursor()
        strSQL = "SELECT * FROM Lectures"
        cursor.execute(strSQL)
        lects = cursor.fetchall()
        connection.close()

        lectures = []
        for lect in lects:
            row = {'num': lect[0], 'lecture_name': lect[1], 'lecture_id': lect[2], 'professor': lect[3], 'department': lect[4], 'lecture_type': lect[5], 'hit': lect[6]}
            lectures.append(row)
        return render(request, 'LectureList.html', {'lectures':lectures}) # lectures의 정보를 LectureList.html로 전달
    except:
        messages.error(request, "강의 목록을 가져오는데 실패했습니다.")
        return redirect('/')

# 강의 검색
def searchLecture(request):
    # 검색어 가져오기
    search_lecture = request.POST.get('search_lecture') # 입력한 강의명(LectureList의 search_lecture) 가져오기
    search_major = request.POST.get('search_major') # 입력한 학과(LectureList의 search_major) 가져오기
    search_professor = request.POST.get('search_professor') # 입력한 교수명(LectureList의 search_professor) 가져오기
    search_type = request.POST.get('search_type')   # 입력한 과목구분(LectureList의 search_type) 가져오기

    # 4가지 중 하나라도 입력이 안됐다면 메세지 띄우기
    allNone = search_lecture == "" and search_major == "None" and search_professor == "" and search_type == "None"
    if(allNone):
        messages.warning(request, "강의명, 개설학과, 교수명, 과목구분 중 한 가지 항목은 필수입력 항목입니다.")
        return render(request, 'search_fail.html')

    # 조건 개수
    q = [0, 0, 0, 0]

    if(search_lecture != ""):
        q[0] = 1
    if(search_major != "None"):
        q[1] = 1
    if(search_professor != ""):
        q[2] = 1
    if(search_type != "None"):
        q[3] = 1

    # DB에서 데이터 가져오기
    cursor = connection.cursor()
    lecture = f"lecture_name  LIKE '%{search_lecture}%'"
    department = f"department = '{search_major}'"
    professor = f"professor LIKE '%{search_professor}%'"
    type = f"lecture_type = '{search_type}'"

    strSQL = ""

    if sum(q) == 1:
        if q[0] == 1:
            strSQL = f"SELECT * FROM Lectures WHERE {lecture} ORDER BY lecture_id"
        elif q[1] == 1:
            strSQL = f"SELECT * FROM Lectures WHERE {department} ORDER BY lecture_id"
        elif q[2] == 1:
            strSQL = f"SELECT * FROM Lectures WHERE {professor} ORDER BY lecture_id"
        else:
            strSQL = f"SELECT * FROM Lectures WHERE {type} ORDER BY lecture_id"
    elif sum(q) == 2:
        q1 = ""
        q2 = ""

        while(q2 == ""):
            if q[0] == 1:
                q1 = lecture
            if q[1] == 1:
                if q[0] != 1:
                    q1 = department
                else:
                    q2 = department
            if q[2] == 1:
                if q[0] == 1 or q[1] == 1:
                    q1 = professor
                else:
                    q2 = professor
            if q[3] == 1:
                q2 = type
        strSQL = f"SELECT * FROM Lectures WHERE {q1}  AND {q2} ORDER BY lecture_id" 
    elif sum(q) == 3:
        if q[0] != 1:
            strSQL = f"SELECT * FROM Lectures WHERE {department} AND {professor} AND {type} ORDER BY lecture_id"
        elif q [1] != 1:
            strSQL = f"SELECT * FROM Lectures WHERE {lecture} AND {professor} AND {type} ORDER BY lecture_id"
        elif q [2] != 1:
            strSQL = f"SELECT * FROM Lectures WHERE {lecture} AND {department} AND {type} ORDER BY lecture_id"
        else:
            strSQL = f"SELECT * FROM Lectures WHERE {lecture} AND {department} AND {professor} ORDER BY lecture_id"
    else:
        strSQL = f"SELECT * FROM Lectures WHERE lecture_name  LIKE '%{search_lecture}%' AND department = '{search_major}' AND professor LIKE '%{search_professor}%' AND lecture_type = '{search_type}' ORDER BY lecture_id"
        
    cursor.execute(strSQL)
    datas = cursor.fetchall()
    connection.close()

    lectures = []
    for lect in datas:
        row = {'num': lect[0], 'lecture_name': lect[1], 'lecture_id': lect[2], 'professor': lect[3], 'department': lect[4], 'lecture_type': lect[5], 'hit': lect[6]}
        lectures.append(row)

    return render(request, 'search.html', {'lectures' : lectures})

# 별점 평균
def avg(evals, target):
    count = len(evals)
    sum = 0

    if target == 'hw_level':
        for e in evals:
            sum += e[4]
    elif target == 'test_level':
        for e in evals:
            sum += e[5]
    else:
        for e in evals:
            sum += e[6]
    
    if count != 0:
        return round(sum/count, 2)

    return 0

# 강의 자세히 보기(강의 정보와 강의평을 볼 수 있음)
@login_required(login_url= '/accounts/login')
def detail(request, lect_id):
    try:
        cursor = connection.cursor()

        # 강의 정보
        strSQL1 = f"SELECT * FROM Lectures WHERE num = '{lect_id}'" # 요청한 강의 번호와 일치하는 강의 정보 조회
        strSQL2 = f"UPDATE Lectures SET hit = hit + 1 WHERE num = '{lect_id}'" # detail 함수가 실행될 때마다 count 증가 => 조회수 증가
        cursor.execute(strSQL1)
        lect = cursor.fetchone()
        cursor.execute(strSQL2) 

        lecture = {'num': lect[0], 'lecture_name': lect[1], 'lecture_id': lect[2], 'professor': lect[3], 'department': lect[4], 'lecture_type': lect[5], 'hit': lect[6], 'lecture_plan': lect[7]}
        
        # 강의평
        strSQL3 = f"SELECT num, author, eval_date, content, hw_level, test_level, lect_power, counts FROM Evals WHERE lect_id = '{lect_id}' ORDER BY eval_date DESC"
        # 강의평 정보 조회
        cursor.execute(strSQL3)
        eval_datas = cursor.fetchall()
        connection.close()

        evals = []
        for eval in eval_datas:
            row = {'lect_id': lect_id, 'num': eval[0], 'author': eval[1], 'eval_date': eval[2], 'content': eval[3], 'hw_level': eval[4], 'test_level': eval[5], 'lect_power': eval[6], 'counts': eval[7]}
            evals.append(row)

        paginator = Paginator(evals, 6) # 강의평 객체 6개를 한 페이지로 자르기
        page = request.GET.get('page') # 사용자가 요청한 페이지 알아내고
        evaluations = paginator.get_page(page) # request된 페이지 return

        # 전체 별점 평균
        hw_avg = avg(eval_datas, 'hw_level')
        test_avg = avg(eval_datas, 'test_level')
        lect_power_avg = avg(eval_datas, 'lect_power')

        return render(request, 'detail.html', {'lect':lecture, 'evaluations':evaluations, 'hw_avg':hw_avg, 'test_avg':test_avg, 'lect_power_avg':lect_power_avg})

    except:
        messages.error(request, '강의 정보를 불러오는데 실패했습니다.')
        return redirect('lectureList')

# 강의평 정렬하기
def ordering(request, lect_id):
    cursor = connection.cursor()
    strSQL1 = f"SELECT * FROM Lectures WHERE num = '{lect_id}'" # 요청한 강의 번호와 일치하는 강의 정보 조회
    strSQL2 = f"SELECT num, author, eval_date, content, hw_level, test_level, lect_power, counts FROM Evals WHERE lect_id = '{lect_id}' ORDER BY counts DESC, eval_date DESC"
    strSQL3 = f"SELECT num, author, eval_date, content, hw_level, test_level, lect_power, counts FROM Evals WHERE lect_id = '{lect_id}' ORDER BY eval_date DESC"

    cursor.execute(strSQL1)
    lect= cursor.fetchone()
    lecture = {'num': lect[0], 'lecture_name': lect[1], 'lecture_id': lect[2], 'professor': lect[3], 'department': lect[4], 'lecture_type': lect[5], 'hit': lect[6], 'lecture_plan': lect[7]}
        
    # 정렬하기 
    sort = request.GET.get('sort')

    if sort == 'recommand':
        cursor.execute(strSQL2)
    else:
        cursor.execute(strSQL3)
    
    eval_datas = cursor.fetchall()
    connection.close()

    evals = []
    for eval in eval_datas:
        row = {'lect_id': lect_id, 'num': eval[0], 'author': eval[1], 'eval_date': eval[2], 'content': eval[3], 'hw_level': eval[4], 'test_level': eval[5], 'lect_power': eval[6], 'counts': eval[7]}
        evals.append(row)

    paginator = Paginator(evals, 6) # 강의평 객체 6개를 한 페이지로 자르기
    page = request.GET.get('page') # 사용자가 요청한 페이지 알아내고
    evaluations = paginator.get_page(page) # request된 페이지 return

    hw_avg = avg(eval_datas, 'hw_level')
    test_avg = avg(eval_datas, 'test_level')
    lect_power_avg = avg(eval_datas, 'lect_power')
    return render(request, 'detail.html', {'lect':lecture, 'evaluations':evaluations, 'hw_avg':hw_avg, 'test_avg':test_avg, 'lect_power_avg':lect_power_avg})