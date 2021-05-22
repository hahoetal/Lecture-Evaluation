from django.shortcuts import render
from django.db.models import Q
from .models import Lectures

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