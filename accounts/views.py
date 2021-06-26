from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView  # 장고에서 제공하는 비밀번호 찾기 기능
from django.contrib.auth.hashers import check_password # 입력한 비밀번호가 맞는지 확인
from django.contrib.auth.decorators import login_required # 데코레이터 사용
from django.views.generic import FormView, CreateView
from django.core.paginator import Paginator # 페이지네이션
from django.db import connection # djanog ORM 대신 SQL문 사용하기

from .models import User
from .forms import LoginForm, UserCreationForm, FindIdForm, PWChangeForm, checkPwForm, PWResetForm, SetPWForm

# 홈
def home(request):
    try:
        cursor = connection.cursor()
        strSQL = "SELECT E.lect_id, E.eval_date, E.content, L.lecture_name FROM Evals E JOIN Lectures L ON E.lect_id = L.num ORDER BY eval_date DESC LIMIT 8"
        cursor.execute(strSQL)
        eval_datas = cursor.fetchall()
        connection.close()

        eval = []
        for data in eval_datas: # DB에서 데이터를 가져와 튜플 형식으로 반환. 딕셔너리 형태로 만들어 주기!
            row = {'lect_id': data[0], 'eval_date': data[1], 'summary': data[2][:40], 'lect_name': data[3]}
            eval.append(row)
        
    except:
        messages.error(request, "강의평을 가져오는데 실패하였습니다.")
    
    return render(request, 'home.html', {'evals':eval})

# 로그인
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        userId = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        # 입력한 아이디와 비밀번호가 DB에 있는 유저 정보와 일치하는지 확인, 일치하면 해당 유저 데이터 반환.
        user = authenticate(self.request, username=userId, password=password)

        # 일치하는 유저가 있는 경우. authenticate()는 username과 password가 일치하지 않으면 None을 반환.
        if user is not None:
            self.request.session['user_id'] = userId # request 객체의 session 부분에 로그인한 사용자 정보 입력.
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

    def form_valid(self, form):
        self.object = form.save() # form에 입력한 값이 유효하면 DB에 저장.
        return redirect(self.get_success_url())

# 아이디 찾기
def find_id(request):
    form = FindIdForm()

    if request.method == 'POST': # 전달 방식이 POST, 즉 아이디를 찾기 위해 요구된 정보를 입력한 경우 
        s_id = request.POST.get('student_id')
        major = request.POST.get('major')
        email = request.POST.get('email')
        
        try:
            cursor = connection.cursor()
            strSQL = f"SELECT user_id FROM User WHERE student_id = '{s_id}' and major = '{major}' and email = '{email}'"
            # 문자열 포매팅을 이용해 파이썬 변수를 SQL문에 담아서 DB에 전달!!
            cursor.execute(strSQL)
            data = cursor.fetchone()
            connection.close()

            target = {'user_id':data[0]} # DB에서 가져온 값이 무엇인지 알려주기 위해 key: value 형식(딕셔너리)로 만들기
            return render(request, 'find_id.html',{'target': target})
        except:
            # 404 에러 예외 처리
            messages.info(request, "입력하신 정보와 일치하는 사용자가 없습니다.")
            return render(request, 'find_id.html', {'form':form})
           
    else: # 전달 방식이 POST가 아님.. 여기서는 GET으로 들어왔다고 생각.
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
    form = checkPwForm()

    if request.method == 'POST':
        pw = request.POST['password']
        user = request.user
        if check_password(pw, user.password): # 비밀번호를 제대로 입력한 경우!
            user.delete() # DB에서 유저 삭제
            messages.info(request, "탈퇴가 완료되었습니다. 강의 평가 서비스를 이용해주셔서 감사합니다.")
            return redirect('/')
        else: # 비밀번호를 잘못 입력한 경우.
            messages.warning(request, "비밀번호를 제대로 입력해주세요.")
            return render(request, 'delete_user.html', {'form':form})
    else:
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

    if user:
        cursor = connection.cursor()
        strSQL1 = f"SELECT user_id, student_id, major, email FROM User WHERE user_id = '{user}'"
        cursor.execute(strSQL1)
        info = cursor.fetchone() # 요청한 유저의 아이디와 일치하는 유저 정보 가져오기

        if(info != None):   
            myInfo = {'user_id': info[0], 'student_id': info[1], 'major': info[2], 'email': info[3]}

            strSQL2 = f"SELECT L.lecture_name, E.num, E.lect_id, E.eval_date, E.content FROM Evals E JOIN Lectures L ON E.lect_id = L.num WHERE author='{user}'"
            cursor.execute(strSQL2)
            eval_datas = cursor.fetchall() # 요청한 유저가 작성한 강의평 정보와 강의명 가져오기
            connection.close()
                
            evals = []
            for data in eval_datas:
                row = {'lect_name': data[0], 'num': data[1], 'lect_id': data[2], 'eval_date': data[3], 'summary': data[4][:40]}
                evals.append(row)

            paginator = Paginator(evals, 6) # 강의평 객체 6개를 한 페이지로 자르기
            page = request.GET.get('page') # 사용자가 요청한 페이지를 알아내고
            myEval = paginator.get_page(page) # request된 페이지 return
            return render(request, 'mypage.html', {'myInfo':myInfo, 'myEval':myEval})
        else:
            messages.error("나의 정보를 가져오는데 실패했습니다.")
    else:
        messages.error("사용자 정보가 없습니다.")
    redirect('/')