from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView  # 장고에서 제공하는 비밀번호 찾기 기능
from django.contrib.auth.hashers import check_password
from django.views.generic import FormView, CreateView
from django.http import HttpResponseNotFound

from .models import User
from .forms import LoginForm, UserCreationForm, FindIdForm, PWChangeForm, checkPwForm, PWResetForm, SetPWForm

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
        return reverse('loginPage') # reverse()  urls.py에서 선언한 name에 따라 url을 받아와 쓸 수 있게 해줌.
    
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

# 탈퇴
def delete_user(request):
    if request.method == 'POST':
        pw = request.POST['password']
        user = request.user
        if check_password(pw, user.password):
            user.delete()
            return redirect('/')
    else:
        form = checkPwForm()
        return render(request, 'delete_user.html', {'form':form})

# 비밀번호 찾기
# 비밀번호 변경을 위한 링크를 받을 이메일 입력
class PWResetView(PasswordResetView):
    template_name = 'pw_reset.html' # 장고가 제공하는 것 말고 다른 템플릿 사용하기
    form_class = PWResetForm # html 상에 보여 줄 폼
    success_url = reverse_lazy("password_reset_done") # 성공 시 이동할 url

    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST["email"]).exists(): # 사용자 이메일 중, 입력한 이메일과 동일한 게 있는지 확인
            return super().form_valid(form)
        else:
            return render(self.request, 'pw_reset_done_fail.html') # 없으면 이메일 전송에 실패했음을 알려주고, 회원가입 또는 다시 입력하도록 함.

# 회원가입 시 입력한 이메일을 올바르게 입력하면, 이메일이 성공적으로 전송되었음을 알려 줌.
class PWResetDoneView(PasswordResetDoneView):
    template_name = 'pw_reset_done.html'

# 이메일로 전송된 링크를 입력하면, 새 비밀번호를 입력할 수 있는 창이 나옴.
class PWResetConfirmView(PasswordResetConfirmView):
    template_name = 'pw_reset_confirm.html'
    form_class = SetPWForm
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):  # form에 입력한 내용이 유효한지 검사
        return super().form_valid(form)

# 새 비밀번호 입력이 성공적으로 이루어지면, 성공했다는 것을 알려주고, login 페이지로 이동.
class PWResetCompleteView(PasswordResetCompleteView):
    template_name = 'pw_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = reverse('loginPage')
        return context