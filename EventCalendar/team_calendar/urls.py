from django.urls import path
from . import views 

app_name = "team_calendar"

urlpatterns = [
    path('team_list/', views.team_list, name='team_list'),
    path('create_team/', views.create_team, name='create_team'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('delete_schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('join_team/<str:team_name>/', views.join_team, name='join_team'),
    path('cancel_request/', views.cancel_request, name='cancel_request'),
]


