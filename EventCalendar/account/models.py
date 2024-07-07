from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(verbose_name="사용자이름", max_length=50)
    team = models.CharField(verbose_name="팀", max_length=50, null=True, default=None)
    is_team_manager = models.BooleanField(verbose_name="팀장", null=True, default=False) 
    request_to = models.CharField(verbose_name="신청팀", max_length=50, null=True, default=None)
    
    def __str__(self):
        return self.name