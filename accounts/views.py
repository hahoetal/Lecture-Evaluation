from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.views.generic import FormView, CreateView
from django.http import HttpResponseNotFound

from .models import User
from .forms import LoginForm, UserCreationForm, FindIdForm, PWChangeForm

# 임시 홈
def home(request):
    return render(request, 'home.html')

# 로그인 페이지 띄우기
def loginPage(request):
    form = LoginForm()
    return render(request, 'login.html', {'form':form})

# 로그인
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        userId = form.cleaned_data.get("userId")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=userId, password=password)

        if user is not None:
            self.request.session['userId'] = userId
            login(self.request, user)
        return super().form_valid(form)

# 로그아웃
def userLogout(request):
    logout(request)
    return redirect('/')

# 회원 가입
class CreateUser(CreateView):
    model = User
    template_name = 'create_user.html'
    form_class = UserCreationForm

    def get_success_url(self):
        messages.success(self.request, "회원가입이 완료되었습니다.")
        return reverse('loginPage')
    
    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())

# 아이디 찾기
def find_id(request):
    if request.method == 'POST':
        s_id = request.POST.get('studentId')
        major = request.POST.get('major') # 학과 입력은 select box를 활용하는 방식으로 고치기
        email = request.POST.get('email')
        
        try:
            target = User.objects.get(studentId=s_id, major = major, email=email)
        except:
            response = HttpResponseNotFound()
            response.write('<p>입력하신 정보와 일치하는 사용자가 없습니다.</p> <p><a href="/">home</a></p>')
            return response
    else:
        form = FindIdForm()
        return render(request, 'find_id.html', {'form':form})

# 비밀번호 변경
def change_pw(request):
    if request.method == 'POST':
        form = PWChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('/')
    else:
            form = PWChangeForm(request.user)
    return render(request, 'change_pw.html', {'form':form})