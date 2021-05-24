from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView  # 장고에서 제공하는 비밀번호 찾기 기능
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required # 데코레이터 사용
from django.views.generic import FormView, CreateView
from django.http import HttpResponseNotFound

from .models import User
from evaluation.models import Evals
from .forms import LoginForm, UserCreationForm, FindIdForm, PWChangeForm, checkPwForm, PWResetForm, SetPWForm

# 임시 홈
def home(request): # django는 request와 response 객체를 이용하여 서버와 클라이언트가 상태를 주고 받음.
    return render(request, 'home.html')
    # render(): HttpResponse 객체를 반환하는 함수.
    # template를 context와 엮어 HttpResponse로 쉽게 반환하게 해주는 함수.
    
    # HttpResponse: HttpRequest와 짝을 이루면, reponse를 반환하는 기본적인 함수.
    # context는 템플릿에서 쓰이는 변수명과 python 객체를 연결하는 사전형 값.

# 로그인
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    # form에 입력한 내용이 유효한지 검사
    # 값이 유효하다면 True가 리턴되고, cleaned_data에 값이 저장 됨.
    def form_valid(self, form):
        userId = form.cleaned_data.get("userId")
        password = form.cleaned_data.get("password")
        # 입력한 아이디와 비밀번호가 DB에 있는 유저 정보와 일치하는지 확인, 일치하면 해당 유저 데이터 반환.
        user = authenticate(self.request, username=userId, password=password)

        # 일치하는 유저가 있는 경우. authenticate()는 username과 password가 일치하지 않으면 None을 반환.
        if user is not None:
            self.request.session['userId'] = userId # request 객체의 session 부분에 로그인한 사용자 정보 입력.
            login(self.request, user) # django가 제공하는 로그인 함수.
        return super().form_valid(form)

# 로그아웃
def userLogout(request):
    logout(request) # django가 제공하는 로그아웃 함수.
    return redirect('/')

# 회원 가입
class CreateUser(CreateView): # 장고가 제공하는 유저 생성 기능을 사용하되 약간 수정.
    model = User # 어떤 모델을 가지고 사용자를 생성할지
    template_name = 'create_user.html' # 장고가 제공하는 것 대신 사용할 템플릿(html)
    form_class = UserCreationForm # html에 띄울 form

    def get_success_url(self):
        messages.success(self.request, "회원가입이 완료되었습니다.")
        return reverse('login')
        # reverse(): 전달받은 인수(name)와 매칭되는 url 반환하고 매칭되는 url이 없으면 NoReverseMatch 예외 발생.
        # resolve_url(): 내부적으로 reverse()를 사용하고, 매칭되는 url이 없으면 예외없이 문자열을 그대로 반환.

    def form_valid(self, form):
        self.object = form.save() # form에 입력한 값이 유효하면 DB에 저장.
        return redirect(self.get_success_url())
        # redirect(): 전달받은 URL로 HttpResponseRedirect를 반환하고, 내부적으로 resolve_url() 사용.

# 아이디 찾기
def find_id(request):
    if request.method == 'POST': # 전달 방식이 POST, 즉 아이디를 찾기 위해 요구된 정보를 입력한 경우 
        s_id = request.POST.get('studentId')
        major = request.POST.get('major') # 학과 입력은 select box를 활용하는 방식으로 고치기
        email = request.POST.get('email')
        
        try:
            target = User.objects.get(studentId=s_id, major = major, email=email)
            return render(request, 'find_id.html',{'target': target})
        except:
            # 404 에러 예외 처리
            response = HttpResponseNotFound()
            response.write('<p>입력하신 정보와 일치하는 사용자가 없습니다.</p> <p><a href="/">home</a></p>')
            return response
    else: # 전달 방식이 POST가 아님.. 여기서는 GET으로 들어왔다고 생각.
        form = FindIdForm()
        return render(request, 'find_id.html', {'form':form}) # form을 띄워주기. {'템플릿에서 쓰이는 변수': python 객체}

# 비밀번호 변경
@login_required(login_url= '/accounts/login')
def change_pw(request):
    if request.method == 'POST':
        form = PWChangeForm(request.user, request.POST) # 비밀번호 변경을 요청한 사용자와 데이터 전달 방식이 담긴 form 제공
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # session update
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('/')
    else:
        form = PWChangeForm(request.user)
    return render(request, 'change_pw.html', {'form':form})

# 탈퇴
@login_required(login_url= '/accounts/login')
def delete_user(request):
    if request.method == 'POST':
        pw = request.POST['password']
        user = request.user
        if check_password(pw, user.password):
            user.delete() # DB에서 유저 삭제
            return redirect('/')
    else:
        form = checkPwForm()
        return render(request, 'delete_user.html', {'form':form})

# 비밀번호 찾기
# 비밀번호 변경을 위한 링크를 받을 이메일 입력
class PWResetView(PasswordResetView):
    template_name = 'pw_reset.html'
    form_class = PWResetForm
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
        context['login_url'] = reverse('login')
        return context

# 마이페이지
@login_required(login_url= '/accounts/login')
def mypage(request):
    user = request.user.get_username() # 요청한 유저의 아이디 가져오기
    myInfo = User.objects.get(userId=user) # 요청한 유저의 아이디와 일치하는 유저 객체 가져오기
    myEval = Evals.objects.filter(author=user) # 요청한 유저가 작성한 평가글 정보 가져오기
    return render(request, 'mypage.html', {'myInfo':myInfo, 'myEval':myEval})

# 용어 정리
# django는 request와 response 객체를 이용하여 서버와 클라이언트가 상태를 주고 받음.
# 이를 위해 django.http 모듈에서 HttpRequest와 HttpResponse API를 제공.
# 1) 특정 페이지가 요청(request)되면, django는 메타데이터를 포함하는 HttpRequest 객체를 생성.
# 2) urls.py에서 정의한 특정 view 클래스/함수의 첫 번째 인자로 해당 객체(reuqest)를 전달.
# 3) view(함수 또는 클래스)는 결과 값을 HttpResponse로 전달.

# URL Reverse: view 함수를 이용해 url을 역으로 계산.
# 개발자가 URL을 일일이 외워서 코딩하지 않아도 됨.
# urls.py에서 정의한 url pattern의 name만 알고 있으면, view 함수와 매칭되는 url을 찾아 전달받을 수 있음.
# reverse(), resolve_url(), redirect()

# session: 클라이언트의 정보를 브라우저가 아닌 웹 서버에 저장하는 것. 사이트와 특정 브라우저 사이의 'state(상태)'를 유지시키는 것.
# cookie: 클라이언트의 정보를 웹브라우저에 저장하는 것.
# sessino의 원리
# 1) 유저가 웹사이트에 접속
# 2) 웹사이트의 서버가 유저에게 sessionId를 부여
# 3) 유저의 브라우저가 sessionId를 cookie에 보존
# 4) 통신할 때마다 sessionId를 웹 서버에 전송(django는 request 객체에 sessionId가 들어있고, session 정보는 django DB의 django_session 테이블에 저장)
# 5) sessionId를 통해서 웹사이트에 접속한 많은 유저 중 특정 유저를 인식할 수 있게 됨.