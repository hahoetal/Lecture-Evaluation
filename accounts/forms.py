# 커스텀한 유저 모델에 맞는 폼(form) 생성하기

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, SetPasswordForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.hashers import check_password
from .models import User

# 유저 생성 폼
class UserCreationForm(forms.ModelForm):
    # 비밀번호 입력
    password1 = forms.CharField(
        label= '비밀번호 ',
        widget= forms.PasswordInput(
            attrs={
                'class ': 'pw',
                'placeholder': '비밀번호',
                'style':'border:none; border-bottom: 2px solid #5C65BB; width:85%; margin-bottom: 5px;'
            }
        ),
    )
    password2 = forms.CharField(
        label= '비밀번호 ',
        widget= forms.PasswordInput(
            attrs={
                'class' : 'pw',
                'placeholder': '비밀번호 확인',
                'style':'border:none; border-bottom: 2px solid #5C65BB; width:85%; margin-bottom: 5px;'
            }
        ),
    )

     # User 모델에 이미 만들어져 있는 field 가져오기
    class Meta:
        model = User
        fields= ('userId', 'major', 'studentId', 'email')

    # 초기화.
    # <form>을 이용해 form을 직접 만들지 않고, 미리 만들어진 form(djanog form)을 사용하기 때문에 css를 적용하려면 아래와 같이 작성하기 
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['userId'].label= '아이디 ' # <label>와 관련. 
        self.fields['userId'].widget.attrs.update({ # css와 관련
            'class': 'create_user', # css 클래스
            'placeholder': '아이디',
        })

        self.fields['major'].label= '전공 '
        self.fields['major'].widget.attrs.update({
            'class': 'create_user',
        })

        self.fields['studentId'].label= '학번 '
        self.fields['studentId'].widget.attrs.update({
            'class': 'create_user',
            'placeholder': '학번',
        })

        self.fields['email'].label= '이메일 '
        self.fields['email'].widget.attrs.update({
            'class': 'create_user',
            'placeholder': 'EMAIL',
        })

    # 입력 받은 password1과 password2가 일치하는지 확인
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    # password1과 password2가 일치하면 저장
    def save(self, commit=True):
        user= super().save(commit=False) # 입력한 내용을 아직 DB에 저장하지 말고,
        user.set_password(self.cleaned_data["password1"]) # 

        if commit:
            user.save() # 비밀번호를 제대로 입력한 경우만 DB에 저장
        return user

# 유저 정보 수정 폼
class UserChangeForm(forms.ModelForm):
    password= ReadOnlyPasswordHashField() # 비밀번호를 이렇게 가져오면 수정이 불가

    class Meta:
        model = User
        fields= (
            'userId',
            'password',
            'major',
            'studentId',
            'email',
        )

    def clean_password(self):
        return self.initial["password"] # 비밀번호는 그대로 다시 저장

# 관리자 페이지에 적용하기 위해 admin.py 수정.

# 로그인 폼
class LoginForm(forms.Form):
    userId= forms.CharField(
        label= '',
        widget=forms.TextInput(
            attrs={
                'class' : 'login',
                'placeholder':'ID'
            }),
        error_messages= {'required': '아이디를 입력해주세요'}
    )
    password= forms.CharField(
        label= '',
        widget= forms.PasswordInput(
            attrs= {
                'class': 'login',
                'placeholder': 'Password'
            }),
        error_messages= {'required': '비밀번호를 입력해주세요'}
    )

    def clean(self):
        cleaned_data= super().clean()
        userId= cleaned_data.get('userId')
        password= cleaned_data.get('password')

        if userId and password:
            try:
                user= User.objects.get(userId=userId)
            except User.DoesNotExist:
                self.add_error('userId', '아이디가 존재하지 않습니다.')
                return

            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')

# 아이디 찾기
class FindIdForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('studentId','major','email',) # 학과는 입력하지 않고 선택할 수 있도록 만들기

# 비밀번호 변경하기
class PWChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PWChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = "기존 비밀번호"
        self.fields['old_password'].widget.attrs.update({
            'class': '',
        })
        self.fields['new_password1'].label = "새 비밀번호"
        self.fields['new_password1'].widget.attrs.update({
            'class':'',
        })
        self.fields['new_password2'].label = "새 비밀번호 확인"
        self.fields['new_password2'].widget.attrs.update({
            'class': '',
        })

# 탈퇴하기_탈퇴하려는 사용자 비밀번호 확인
class checkPwForm(forms.Form):
    password = forms.CharField(
        label='비밀번호',
        widget= forms.PasswordInput(
            attrs={
                'class': '',
            }
        )
    )

# 비밀번호 찾기_ 비밀번호 변경을 위한 링크를 받을 이메일 입력.
class PWResetForm(PasswordResetForm):
    # 이미 만들어진 form에 css를 적용하려면, 초기화가 필요.
    def __init__(self, *args, **kwargs):
        super(PWResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "이메일 "
        self.fields['email'].widget.attrs.update({
            'class': 'findPw_input',
        })

# 비밀번호 찾기_ 비밀번호 초기화
class SetPWForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPWForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = "새 비밀번호"
        self.fields['new_password1'].widget.attrs.update({
            'class':'',
        })
        self.fields['new_password2'].label = "새 비밀번호 확인"
        self.fields['new_password2'].widget.attrs.update({
            'class': '',
        })