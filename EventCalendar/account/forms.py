# account/forms.py
### Form/ModelForm들은 forms 모듈에 작성.
# class MyForm(forms.Form):
#     pass
# class MyForm2(forms.ModelForm):
#     pass

from django import forms
# User(사용자)를 관리하는 ModelForm은 django 에서 제공하는 Form을 상속받아서 구현.
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from .models import User

## User 가입시 사용할 ModelForm을 정의
### ModelForm <-상속- UserCreateForm(username, password) <-상속- MyForm

## ModelForm은 Form Field들을 Model 클래스를 이용해서 정의
class CustomUserCreateForm(UserCreationForm):
    # Form Field 들 class변수 정의
    ## UserCreationForm의 비밀번호 입력 Form을 재정의
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput()) # 문자열 입력 폼.
    password2 = forms.CharField(label="Password확인", 
                                widget=forms.PasswordInput(), 
                                help_text="비밀번호 확인을 위해 이전과 동일한 비밀번호를 입력하시오.")
   # widget: 입력양식의 태그를 설정. 
   #(각Field들은 기본 태그(widget)가 있는데 다른 것을 사용경우 widget설정을 한다.)
   #(ex: CharField의 기본 widget은 TextInput (input type=text). 문자열 입력 태그로 password, textarea를 사용할 경우 widget 지정.

    class Meta:
        # ModelForm과 연결된 Model 클래스 지정. 
        #                 (Model의 Field들을 이용해서 Form Field들을 생성)
        model = User 
        # Model Field 중 Form Field로 포함시킬 것들을 선언
        # fields = "__all__"  # 모든 Model Field들을 포함.
        fields = ["username", "password1", "password2", "name"]
        # 지정한 field들을 제외한 나머지 field들을 form field로 정의
        # exclude = ["field명"] 
        
## 패스워드변경 Form - PasswordChangeForm 상속해서 구현.
from django.contrib.auth.forms import PasswordChangeForm
class CustomPasswordChangeForm(PasswordChangeForm):
    # 필드 재정의
    old_password = forms.CharField(
        label="기존 패스워드", 
        widget=forms.PasswordInput() # 태그의 attribute 설정: attr={"attr":value}
    )
    new_password1 = forms.CharField(
        label="새 패스워드", 
        widget=forms.PasswordInput() # 태그의 attribute 설정: attr={"attr":value}
    )
    new_password2 = forms.CharField(
        label="새 패스워드 확인", 
        widget=forms.PasswordInput() # 태그의 attribute 설정: attr={"attr":value}
    )

## User 정보 수정 Form (UserChangeForm 상속-username, password관련변경)
class CustomUserChangeForm(UserChangeForm):
    # password 항목은 안나오도록 변경
    password = None

    class Meta:
        model = User
        fields = ["name"]
    