# account/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from . import views

app_name = "account"
urlpatterns = [
    path("join", views.create, name="join"),
    # path("login", views.user_login, name="login"),
    path("login", 
        LoginView.as_view(
            template_name="account/login.html", # login form template
            form_class=AuthenticationForm       # Form class
        ),
        name="login"),
    path("logout", views.user_logout, name="logout"),
    path("detail", views.user_detail, name="detail"), 
    path("password_change", views.change_password, name="password_change"),
    path("update", views.user_update, name="update"),
    path("approve/<int:user_id>", views.approve_request, name="approve_request"),
    path("reject/<int:user_id>", views.reject_request, name="reject_request"),
    path("user_expel/", views.user_expel, name="user_expel"),
    path("delete", views.user_delete, name="delete"),
    path("team_delete/", views.user_team_delete, name="team_delete"),
]