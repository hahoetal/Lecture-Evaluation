# forms.py에서 만든 폼 관리자 페이지에 적용하기

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User 
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    # 관리자 페이지에서 사용자 변경 폼, 추가 폼을 forms.py에서 생성한 폼으로 변경
    form = UserChangeForm
    add_form = UserCreationForm

    # 커스텀 유저 모델이 관리자 화면에서 어떻게 표시될지에 대한 설정
    list_display = ('user_id', 'major', 'student_id', 'email')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('user_id', 'password')}),
        ('Personal info', {'fields': ('major', 'student_id', 'email')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'major', 'student_id', 'email')
        }),
    )
    search_fields = ('user_id',)
    ordering = ('user_id',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin) # 커스텀한 유저 모델과 관리자 폼을 사용하겠다!
admin.site.unregister(Group) # 장고에서 기본적으로 제공하는 Group은 사용하지 않음.

# settings.py 수정