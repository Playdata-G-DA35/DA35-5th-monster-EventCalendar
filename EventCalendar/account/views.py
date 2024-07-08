# account/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User 
from team_calendar.models import Team, CalendarData
from django.contrib import messages
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
from .forms import CustomUserChangeForm
@login_required # 로그인한 사용자만 요청가능.
def user_update(request):
    if request.method == "GET":
        form = CustomUserChangeForm(instance=request.user)
        return render(request, "account/update.html", {"form":form})
    elif request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # 저장, User 로그인 정보 갱신
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse('account:detail'))
        else:
            return render(request, "account/update.html", {"form":form})


# 회원탈퇴
from django.contrib import messages
@login_required
def user_delete(request):
    user = request.user
    members = User.objects.filter(team=user.team)
    
    if user.is_team_manager: # 매니저일 때 
        team = Team.objects.get(team_name= user.team)
        if len(members) <= 1: # 매니저 자신만 팀멤버이면 
            user.delete()
            team.delete() # 팀도 삭제
            logout(request)
        else: # 남은 멤버 있으면 탈퇴 불가 
            messages.error(request, '남아있는 팀원이 있어 회원 탈퇴할 수 없습니다.')
            return redirect(reverse('account:detail'))
    else: # 매니저 아니면 탈퇴 가능
        user.delete()
        logout(request)
            
    return redirect(reverse('home'))


# 팀 탈퇴
@login_required
def user_team_delete(request):
    user = request.user
    if user.team is not None:
        team = Team.objects.get(team_name = user.team)
        applicants = User.objects.filter(request_to= team.team_name)

        # 팀매니저인 경우
        if user.is_team_manager: 
            if (team.member1 is None) & (team.member2 is None) &(team.member3 is None): # 남은 멤버가 없으면 
                user.team = None # 탈퇴  
                user.request_to = None
                user.is_team_manager= False
                team.delete() # 팀도 삭제

                # 매니저가 팀탈퇴하며 해당 팀 삭제될 경우 : user의 신청 요청 기록 에서도 지워야 함.
                for app in applicants:
                    app.request_to = None 
                    app.is_team_manager=None
                    app.save()

            else: # 남은 멤버 있으면 탈퇴 못함
                messages.error(request, '남아있는 팀원이 있어 회원 탈퇴할 수 없습니다.')
                return redirect(reverse('account:detail'))

        # 팀매니저아니면 탈퇴
        else: 
            user.team = None 
            user.request_to = None
            user.is_team_manager= False
            # Team 객체에서 멤버 이름 삭제
            if user.name == team.member1:
                team.member1=None
            elif user.name == team.member2:
                team.member2=None
            elif user.name == team.member3:
                team.member3=None
            team.save()

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
        messages.error(request, '팀이 가득찼습니다.')
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

def user_expel (request):
    member_id = request.POST['member_id']
    team_name = request.user.team
    team = Team.objects.get(team_name=team_name)
    if int(member_id) == 1:  
        delete_user_name = team.member1
        delete_user = User.objects.get(name=delete_user_name, team=team_name)
        team.member1 = None
    elif int(member_id) == 2:  
        delete_user_name = team.member2
        delete_user = User.objects.get(team=team_name, name=delete_user_name)
        team.member2 = None
    elif int(member_id) == 3:  
        delete_user_name = team.member3
        delete_user = User.objects.get(team=team_name, name=delete_user_name)
        team.member3 = None
    else:
        messages.error(request, '')
        return redirect(reverse(url)) #에러메세지 띄워야함 꽉찼다고
    
    delete_user_schedule = CalendarData.objects.filter(user=delete_user)
    delete_user_schedule.delete()
    delete_user.request_to = None
    delete_user.team = None
    delete_user.save()
    team.save()
    url = 'account:detail'
    return redirect(reverse(url))