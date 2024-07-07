# account/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User 
from team_calendar.models import Team

from django.contrib.auth.decorators import login_required

# 가입 처리 - ModelForm을 이용
## GET  방식요청 - 입력폼을 응답
## POST 방식요청 - 가입 처리
from .forms import CustomUserCreateForm
def create(request):
    if request.method == 'GET':
        # context data 로 빈 Form(ModelForm) 객체를 template 전달.
        return render(
            request, 
            "account/create.html", 
            {"form":CustomUserCreateForm()}
        )
    elif request.method == "POST":
        # 요청파라미터 조회 -> 검증
        ### ModelForm/Form 에 요청파라미터를 넣어서 객체 생성.
        form = CustomUserCreateForm(request.POST)
        ## 검증 결과 이상이 없으면
        if form.is_valid():
            #정상처리 -> DB 저장 (ModelForm.save(): Model)
            user = form.save() # insert하고 insert한 값들을 가진 User(Model)객체를 반환
            ## 가입과 동시에 로그인
            login(request, user)            
            # 응답 : 등록->redirect방식
            return redirect(reverse('home'))
        else:
            # 요청파라미터 검증 실패. => 등록폼으로 이동.
            return render(request, "account/create.html",
                        {"form":form})  # form: 요청파라미터를 가진 Form

from django.contrib.auth import login, logout, authenticate       
# login(), logout(): 로그인/로그아웃 처리하는 함수
# authenticate(): username/password를 확인함수.
from django.contrib.auth.forms import AuthenticationForm 
#로그인 모델폼 - username, password 입력폼

### 로그인 처리: GET-로그인 폼반환, POST-로그인 처리
def user_login(request):
    if request.method == "GET":
        return render(request, 
                    'account/login.html', 
                    {"form":AuthenticationForm()})
    elif request.method == "POST":
        # 요청파라미터 조회
        username = request.POST['username']
        password = request.POST['password']
        ## AUTH_USER_MODEL를 기반으로 사용자 인증 처리
        ### 받은 username/password가 유효한 사용자 계정이라면 User객체를 반환.
        ###      유효하지 않은 사용자 계정이라면 None 반환.
        user = authenticate(request, username=username, password=password)
        if user is not None: # 유효한 사용자 계정.
            login(request, user) # 로그인 처리 -> 로그아웃할 때까지 request에 로그인한 사용자 정보를 사용할 수있도록 처리.
            return redirect(reverse("home"))
        else: # 유효한 사용자 계정이 아님
            return render(
                request,
                'account/login.html', 
                {"form":AuthenticationForm(), 
                "errorMessage":"ID나 Password를 다시 확인하세요."})

### 로그아웃 처리

# View를 실행할 때 로그인 되었는지를 먼저 체크.
## 로그인이 안되있으면 settings.LOGIN_URL  여기로 이동.
@login_required   
def user_logout(request):
    # login() 시 처리한 것들을 다 무효화시킴
    logout(request)
    return redirect(reverse('home'))

##### 로그인한 사용자 정보 조회
def user_detail(request):
    ## 로그인한 사용자 정보 -> request.user
    user = User.objects.get(pk=request.user.pk)
    if user.team:
        team = Team.objects.get(team_name=request.user.team)
        req_user = User.objects.filter(request_to=team.team_name)
    else:
        team = None
        req_user = None
        
    return render(request, "account/detail.html", {"object":user, "team":team, "req_user":req_user})

##############
# 변경
##############

# 패스워드 변경 - GET: 폼제공, POST: 변경처리
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required 
def change_password(request):
    if request.method == "GET":
        # form = PasswordChangeForm(request.user)# 로그인한 User정보(old password 비교)
        form = CustomPasswordChangeForm(request.user)
        return render(
            request, "account/password_change.html", 
            {'form': form})
    elif request.method == "POST": # 패스워드 변경
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid(): #요청파라미터 검증이 잘 되었으면
            user = form.save()  # user의 password  update
            # 사용자의 정보(패스워드)가 변경된것을 session에 업데이트. 안하면 로그아웃이 된다.
            update_session_auth_hash(request, user) 
            return redirect(reverse("account:detail"))
        else: # 요청파라미터의 검증 실패
            return render(
                request, 'account/password_change.html',
                {'form':form, 'errorMessage':'패스워드를 다시 입력하세요.'}
            )

# 사용자 정보를 수정
## GET - 수정 폼 전달 (원래 입력값이 폼필드에 나와야 함)
## POST - 수정 업데이트 (세션정보 업데이트)
@login_required #로그인한 사용자만 요청 가능.
def user_update(request):
    if request.method == "GET":
        pass
        return render(request, "account/unpdate.html", {})
    elif request.method == "POST":
        pass

# 탈퇴
@login_required
def user_delete(request):
    request.user.delete()
    # 삭제 후 로그아웃
    logout(request)
    return redirect(reverse('home'))

# 팀 탈퇴
@login_required
def user_team_delete(request , user_id):
    user = User.objects.get(pk = user_id)
    if user.team is not None :
        if user.is_team_manager:
            user_team = Team.objects.get(team_name=user.team)
            if (user_team.member1 == None) & (user_team.member2 == None) & (user_team.member3 == None):
                user.is_team_manager = False 
                user.request_to = None          
                user.team=None
                user_team.delete()
        
        else:
            user.team = None
            user.request_to = None 

    user.save()
    return redirect(reverse('account:detail'))

def approve_request(request, user_id):
    manager = request.user #현재 사용자(매니저)의 팀
    team=Team.objects.get(team_name =manager.team) # 매니저 팀 객체 
    applicant = User.objects.get(pk=user_id)# 매니저팀 지원자

    url = 'account:detail'

    if team.member1 is None:  # 멤버 1이 비어 있는 경우
        team.member1 = applicant.name
    elif team.member2 is None:  # 멤버 2가 비어 있는 경우
        team.member2 = applicant.name
    elif team.member3 is None:  # 멤버 3이 비어 있는 경우
        team.member3 = applicant.name
    else:
        return redirect(reverse(url)) #에러메세지 띄워야함 꽉찼다고

    applicant.team = team.team_name
    applicant.request_to = None
    applicant.save()
    team.save()
    return redirect(reverse(url))


def reject_request (request, user_id):
    applicant = User.objects.get(pk=user_id)# 매니저팀 지원자
    url = 'account:detail'
    applicant.request_to = None
    applicant.save()
    return redirect(reverse(url))

