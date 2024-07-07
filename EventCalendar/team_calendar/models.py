from django.db import models
from account.models import User

# Create your models here.

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50, unique=True)
    team_manager = models.CharField(max_length=50)
    member1 = models.CharField(max_length=50, default=None, null=True)
    member2 = models.CharField(max_length=50, default=None, null=True)
    member3 = models.CharField(max_length=50, default=None, null=True)

class CalendarData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()