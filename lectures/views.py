from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator # 페이지네이션

from .models import Lectures
from evaluation.models import Evals

# 강의 목록 페이지 띄우기
def LectureListPage(request):
    lectures = Lectures.objects.all()
    return render(request, 'LectureList.html', {'lectures':lectures}) # lectures의 정보를 LectureList.html로 전달

# 강의 검색
def serachLecture(request):
    lectures = Lectures.objects.all().order_by('lecture_id') # Lectures의 모든 객체 가져오기(학수번호로 오름차순)
    
    search_key = request.POST.get('search_key') # 입력한 강의명(LectureList의 search_key) 가져오기
    if search_key:  # 만약 검색어가 존재하면
        lectures = lectures.filter(Q(lecture_name__contains=search_key)) # 강의명이 search_key를 포함하는 경우 lecutres에 저장
        return render(request, 'search.html', {'lectures':lectures, 'search_key':search_key})
    else: 
        return render(request, 'search.html')

# 강의 자세히 보기(강의 정보와 강의평을 볼 수 있음)
def detail(request, lect_id):
    lect = get_object_or_404(Lectures, pk=lect_id)
    evals = Evals.objects.filter(lect_id=lect_id) # 사용자가 요청한 강의와 강의 번호가 일치하는 강의평만 가져오기
    paginator = Paginator(evals, 6) # 강의평 객체 6개를 한 페이지로 자르기
    page = request.GET.get('page') # 사용자가 요청한 페이지 알아내고
    evaluations = paginator.get_page(page) # request된 페이지 return
    return render(request, 'detail.html', {'lect':lect, 'evaluations':evaluations})