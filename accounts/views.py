from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import FormView

from .models import User
from .forms import LoginForm

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