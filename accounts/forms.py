# 커스텀한 유저 모델에 맞는 폼(form) 생성하기

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, SetPasswordForm
from .models import User

# 유저 생성 폼
class UserCreationForm(forms.ModelForm):
    # 비밀번혼 입력
    password1 = forms.CharField(
        label= '',
        widget= forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호',
            }
        ),
    )
    password2 = forms.CharField(
        label= '',
        widget= forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호 확인',
            }
        ),
    )

     # User 모델에 이미 만들어져 있는 field 가져오기
    class Meta:
        model = User
        fields= ('userId', 'major', 'studentId', 'email')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['userId'].label= '',
        self.fields['userId'].widget.attrs.update({
            #'class': '',
            'placeholder': '아이디',
        })

        self.fields['major'].label= '',
        self.fields['major'].widget.attrs.update({
            #'class': '',
            'placeholder': '전공',
        })

        self.fields['studentId'].label= '',
        self.fields['studentId'].widget.attrs.update({
            #'class': '',
            'placeholder': '학번',
        })

        self.fields['email'].label= ''
        self.fields['email'].widget.attrs.update({
            'class': '',
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
        user= super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
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
                #'class: '',
                'placeholder':'ID'
            }),
        error_messages= {'required': '아이디를 입력해주세요'}
    )
    password= forms.CharField(
        label= '',
        widget= forms.PasswordInput(
            attrs= {
                #'class': '',
                'placeholder': 'Password'
            }),
        error_messages= {'required': '비밀번호를 입력해주세요'}
    )

    def clean(self):
        cleaned_data= super().clean()
        teacherId= cleaned_data.get('userId')
        password= cleaned_data.get('password')

        if teacherId and password:
            try:
                user= User.objects.get(userId=userId)
            except User.DoesNotExist:
                self.add_error('teacherId', '아이디가 존재하지 않습니다.')
                return

            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')