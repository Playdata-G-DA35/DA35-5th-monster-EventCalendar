from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from team_calendar.models import Team, CalenderData

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "name"]
    add_fieldsets = (
        (
            "인증정보",
            {
                "fields":("username", "password1", "password2"),
            }
        ),
        (
            "개인정보",
            {
                "fields":("name",)
            }
        )
    )
    fieldsets = (
        (
            "인증정보",
            {
                "fields":("username", "password"),
            }
        ),
        (
            "개인정보",
            {
                "fields":("name",)
            }
        ),
        (
            "권한", 
            {
                "fields":("is_active", "is_superuser")
            }
        )
    )

admin.site.register(User, CustomUserAdmin)
