
# views.py
from django.shortcuts import render, redirect
import calendar
from datetime import datetime
from .models import Team, CalenderData
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def calendar_view(request):
    print("called view")
    today = datetime.today()
    year = int(request.POST.get('year', today.year))
    month = int(request.POST.get('month', today.month))
    
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)
    
    years = list(range(2020, 2031))  # 연도 리스트 (2020년부터 2030년까지)
    months = list(range(1, 13))  # 월 리스트 (1월부터 12월까지)
    team = request.user.team
    schedule_list = CalenderData.objects.get(team=team, schedule_year=year, schedule_month=month)

    context = {
        'year': year,
        'month': month,
        'month_days': month_days,
        'month_name': calendar.month_name[month],
        'years': years,
        'months': months,
        'schedule_list':schedule_list
    }
    
    return render(request, 'calendar.html', context)

def team_list(request):
    team_list = Team.objects.all()
    user_team = request.user.team
    return render(request, "list.html", {"team_list":team_list, "user_team":user_team})

def create_team(request):
    print(request.method)
    if request.method == "GET":
        return render(request, "create_team.html")
    elif request.method == "POST":
        print(request.POST.get("user"))
        if not request.user.is_join_request:
            team_name = request.POST.get("team_name")
            # 등록 처리.
            ## 1. 요청파라미터 조회 (질문, 보기들)
            ### GET방식: request.GET, POST방식: request.POST
            #질문
            ## 2. 요청파라미터 검증 (글자수, 값이 넘어왔는지 ....)
            ## 3. 검증 통과 -> DB에 insert
            team = Team(team_name=team_name, team_manager=request.POST.get("user_name"))
            user = request.user
            user.is_team_manager = True
            user.is_join_request = True
            user.request_to = team_name
            user.team = team_name
            team.save()
            user.save()
        else:
            errorMessage = '이미 가입한 팀이 있습니다.' 
            # alert 구현 
        url = reverse("team_calendar:team_list")
        return redirect(url)      

