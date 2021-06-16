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
                'class ': 'create_userP',
                'id': 'pw1',
                'placeholder': '비밀번호',
            }
        ),
    )
    password2 = forms.CharField(
        label= '비밀번호 ',
        widget= forms.PasswordInput(
            attrs={
                'class' : 'create_userP',
                'id':'pw2',
                'placeholder': '비밀번호 확인',
            }
        ),
    )

     # User 모델에 이미 만들어져 있는 field 가져오기
    class Meta:
        model = User
        fields= ('user_id', 'major', 'student_id', 'email')

    # 초기화.
    # <form>을 이용해 form을 직접 만들지 않고, 미리 만들어진 form(djanog form)을 사용하기 때문에 css를 적용하려면 아래와 같이 작성하기 
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['user_id'].label= '아이디 ' # <label>와 관련. 
        self.fields['user_id'].widget.attrs.update({ # css와 관련
            'class': 'create_user', # css 클래스
            'id':'cu1',
            'placeholder': '아이디',
        })

        self.fields['major'].label= '전공 '
        self.fields['major'].widget.attrs.update({
            'class': 'create_user',
            'id': 'cu2',
        })

        self.fields['student_id'].label= '학번 '
        self.fields['student_id'].widget.attrs.update({
            'class': 'create_user',
            'id':'cu3',
            'placeholder': '학번',
        })

        self.fields['email'].label= '이메일 '
        self.fields['email'].widget.attrs.update({
            'class': 'create_user',
            'id':'cu4',
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
            'user_id',
            'password',
            'major',
            'student_id',
            'email',
        )

    def clean_password(self):
        return self.initial["password"] # 비밀번호는 그대로 다시 저장

# 관리자 페이지에 적용하기 위해 admin.py 수정.

# 로그인 폼
class LoginForm(forms.Form):
    user_id= forms.CharField(
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
        user_id= cleaned_data.get('user_id')
        password= cleaned_data.get('password')

        if user_id and password:
            try:
                user= User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                self.add_error('user_id', '❗ 아이디가 존재하지 않습니다.')
                return

            if not check_password(password, user.password):
                self.add_error('password', '❗ 비밀번호가 틀렸습니다.')

# 아이디 찾기
class FindIdForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('student_id','major','email',) # 학과는 입력하지 않고 선택할 수 있도록 만들기
    def __init__(self, *args, **kwargs):
        super(FindIdForm, self).__init__(*args, **kwargs)

        self.fields['major'].label= '전공 '
        self.fields['major'].widget.attrs.update({
            'class': 'find_id',
            'id': 'fi1'
        })

        self.fields['student_id'].label= '학번 '
        self.fields['student_id'].widget.attrs.update({
            'class': 'find_id',
            'id':'fi2',
            'placeholder': '학번',
        })

        self.fields['email'].label= '이메일 '
        self.fields['email'].widget.attrs.update({
            'class': 'find_id',
            'id':'fi3',
            'placeholder': 'EMAIL',
        })

# 비밀번호 변경하기
class PWChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PWChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = "기존 비밀번호 "
        self.fields['old_password'].widget.attrs.update({
            'class': 'org_pw',
        })
        self.fields['new_password1'].label = "새 비밀번호 "
        self.fields['new_password1'].widget.attrs.update({
            'class':'new_pw',
        })
        self.fields['new_password2'].label = "새 비밀번호 확인 "
        self.fields['new_password2'].widget.attrs.update({
            'class': 'new_pwr',
        })

# 탈퇴하기_탈퇴하려는 사용자 비밀번호 확인
class checkPwForm(forms.Form):
    password = forms.CharField(
        label='비밀번호',
        widget= forms.PasswordInput(
            attrs={
                'class': 'pw',
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
            'class':'pw_input',
        })
        self.fields['new_password2'].label = "새 비밀번호 확인"
        self.fields['new_password2'].widget.attrs.update({
            'class': 'pw_input',
        })