# views.py
from django.shortcuts import render, redirect, get_object_or_404
import calendar
from datetime import datetime
from .models import Team, CalendarData
from account.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import TimeForm


@login_required
def calendar_view(request):
    if not request.user.team:
        return render(request, 'list.html')
        #return render(request, 'error.html', {'message': 'You are not assigned to any team.'})

    user_team = get_object_or_404(Team, team_name=request.user.team)

    if request.method == 'POST':
        form = TimeForm(request.POST)
        if form.is_valid():
            year = int(request.POST.get('year'))
            month = int(request.POST.get('month'))
            selected_day = int(form.cleaned_data['selected_day'])
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            start_time = datetime.strptime(start_time, '%H:%M').time()
            end_time = datetime.strptime(end_time, '%H:%M').time()
            CalendarData.objects.create(user=request.user, team=user_team, year=year, month=month, day=selected_day, start_time=start_time, end_time=end_time)
            return redirect(f'{request.path}?year={year}&month={month}')
    else:
        current_year = datetime.now().year
        current_month = datetime.now().month
        form = TimeForm(initial={'year': current_year, 'month': current_month})

    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))

    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)

    schedules = {}
    for schedule in CalendarData.objects.filter(team=user_team, year=year, month=month):
        if schedule.day not in schedules:
            schedules[schedule.day] = []
        schedules[schedule.day].append({
            'user_name' : schedule.user.name,
            'start_time': schedule.start_time.strftime('%H:%M'),
            'end_time': schedule.end_time.strftime('%H:%M'),
            'is_user_schedule': schedule.user == request.user,
            'id': schedule.id
        })

    # ## 개당 스케쥴 6개 이하 정의본
    # for overday in schedules:
    #     if len(schedules[overday])>6:
    #         # 에러메세지
    #         # calenderview로 redirect
    #         return render(request, 'list.html')

    context = {
        'calendar': month_days,
        'form': form,
        'minutes': [f'{h:02d}:{m:02d}' for h in range(24) for m in range(0, 60, 15)],
        'schedules': schedules.items(),
        'current_year': year,
        'current_month': month,
        'years': range(datetime.now().year - 10, datetime.now().year + 10),
        'months': range(1, 13),
    }
    return render(request, 'calendar.html', context)

@login_required
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(CalendarData, id=schedule_id)
    if schedule.user == request.user and schedule.team.team_name == request.user.team:
        schedule.delete()
    year = request.POST.get('year')
    month = request.POST.get('month')
    redirect_url = reverse("team_calendar:calendar_view")+f'?year={year}&month={month}'
    return HttpResponseRedirect(redirect_url)

def team_list(request):
    team_list = Team.objects.all()
    if request.user.is_authenticated:
        user_team = request.user.team
        user_request_to = request.user.request_to
    else:
        user_team = None
        user_request_to = None
    return render(request, "list.html", {"team_list":team_list, "user_team":user_team, "user_request_to":user_request_to, "login":request.user.is_authenticated})

@login_required
def create_team(request):
    print(request.method)
    if request.method == "GET":
        return render(request, "create_team.html")
    elif request.method == "POST":

        if not request.user.team: # user의 팀이 없으면
            team_name = request.POST.get("team_name")
            team = Team(team_name=team_name, team_manager=request.POST.get("user_name"))
            user = request.user
            user.is_team_manager = True
            user.request_to = None
            user.team = team_name
            team.save()
            user.save()
        else:
            errorMessage = '이미 가입한 팀이 있습니다.' 
            # alert 구현 
        url = reverse("team_calendar:team_list")
        return redirect(url)
    
# 팀 참여 요청
@login_required
def join_team(request, team_name):
    user = request.user
    user.request_to = team_name
    user.save()
    url = reverse("team_calendar:team_list")
    return redirect(url)

# 팀 참여 요청 취소 
@login_required
def cancel_request(request):
    user = request.user
    user.request_to = None
    user.save()
    url = reverse("team_calendar:team_list")
    return redirect(url)

