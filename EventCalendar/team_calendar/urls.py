from django.urls import path
from . import views 

app_name = "team_calendar"

urlpatterns = [
    path('team_list/', views.team_list, name='team_list'),
    path('create_team/', views.create_team, name='create_team'),
    path('<str:team_name>/', views.calendar_view, name='calendar_view'),
]


