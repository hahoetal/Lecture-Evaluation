from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator # 페이지네이션
from django.contrib import messages
from django.contrib.auth.decorators import login_required # 데코레이터 사용

from .models import Lectures
from evaluation.models import Evals


# 강의 목록 페이지 띄우기
def LectureListPage(request):
    lectures = Lectures.objects.all()
    return render(request, 'LectureList.html', {'lectures':lectures}) # lectures의 정보를 LectureList.html로 전달

# 강의 검색
def searchLecture(request):
    lectures = Lectures.objects.all().order_by('lecture_id') # Lectures의 모든 객체 가져오기(학수번호로 오름차순)
    
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

    # 조건 하나씩 검사하기
    if(search_lecture != ""):
        lectures = lectures.filter(Q(lecture_name__contains=search_lecture))
    if(search_major != "None"):
        lectures = lectures.filter(Q(department=search_major))
    if(search_professor != ""):
        lectures = lectures.filter(Q(professor__contains=search_professor))
    if(search_type != "None"): 
        lectures = lectures.filter(Q(lecture_type=search_type))

    return render(request, 'search.html', {'lectures' : lectures})

# 별점 평균
def avg(evals, target):
    count = len(evals)
    sum = 0

    if target == 'hw_level':
        for e in evals:
            sum += e.hw_level
    elif target == 'test_level':
        for e in evals:
            sum += e.test_level
    else:
        for e in evals:
            sum += e.lect_power
    
    if count != 0:
        return round(sum/count, 2)

    return 0

# 강의 자세히 보기(강의 정보와 강의평을 볼 수 있음)
@login_required(login_url= '/accounts/login')
def detail(request, lect_id):
    # 강의 정보
    lect = get_object_or_404(Lectures, pk=lect_id)
    lect.hit += 1 # detail 함수가 실행될 때마다 count 증가 => 조회수 증가
    lect.save() # db에 저장
    
    # 강의평
    evals = Evals.objects.filter(lect_id=lect_id).order_by('-eval_date')
    paginator = Paginator(evals, 6) # 강의평 객체 6개를 한 페이지로 자르기
    page = request.GET.get('page') # 사용자가 요청한 페이지 알아내고
    evaluations = paginator.get_page(page) # request된 페이지 return

    # 강의평 하나당 별점 평균
    avg_score =[]
    for e in evals:
        score = e.hw_level + e.test_level + e.lect_power
        avg_score.append(round(score/3, 2))

    # 전체 별점 평균
    hw_avg = avg(evals, 'hw_level')
    test_avg = avg(evals, 'test_level')
    lect_power_avg = avg(evals, 'lect_power')

    return render(request, 'detail.html', {'lect':lect, 'evaluations':evaluations, 'hw_avg':hw_avg, 'test_avg':test_avg, 'lect_power_avg':lect_power_avg})

# 강의평 정렬하기
def ordering(request, lect_id):
    lect = get_object_or_404(Lectures, pk=lect_id)

    # 정렬하기 
    sort = request.GET.get('sort')

    if sort == 'recommand':
        evals = Evals.objects.filter(lect_id=lect_id).order_by('-counts', '-eval_date') # 사용자가 요청한 강의와 강의 번호가 일치하는 강의평만 가져오기
    else:
        evals = Evals.objects.filter(lect_id=lect_id).order_by('-eval_date')

    paginator = Paginator(evals, 6) # 강의평 객체 6개를 한 페이지로 자르기
    page = request.GET.get('page') # 사용자가 요청한 페이지 알아내고
    evaluations = paginator.get_page(page) # request된 페이지 return

    hw_avg = avg(evals, 'hw_level')
    test_avg = avg(evals, 'test_level')
    lect_power_avg = avg(evals, 'lect_power')
    return render(request, 'detail.html', {'lect':lect, 'evaluations':evaluations, 'hw_avg':hw_avg, 'test_avg':test_avg, 'lect_power_avg':lect_power_avg})