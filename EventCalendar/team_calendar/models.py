from django.db import models

# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=50)
    team_manager = models.CharField(max_length=50)
    member1 = models.CharField(max_length=50, default=None, null=True)
    member2 = models.CharField(max_length=50, default=None, null=True)
    member3 = models.CharField(max_length=50, default=None, null=True)

class CalenderData(models.Model):
    team_name = models.ForeignKey(
        Team, # 참조 모델클래스 
        on_delete=models.CASCADE  # 참조 값이 삭제될때 처리방법.
        # , related_name = "Teams_Schedules"  
    )
    scheduled_year = models.DateField(null=True)
    scheduled_month = models.DateField(null=True)
    scheduled_date = models.DateField(null=True)
    scheduled_member = models.CharField(max_length=50, null=True)
    scheduled_start_time = models.TimeField(null=True)
    scheduled_end_time = models.TimeField(null=True)