from email.policy import default
from itertools import count
from django.db import models
from users.models import Music, User
# Create your models here.

class Pomodoro(models.Model):
    name = models.CharField(max_length=30, help_text="Enter the tittle name", null=True, blank=True,)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_pomodoro",
        null=True,
        blank=True
    )
    total_time = models.BigIntegerField(default=1500)
    elapsed_time = models.BigIntegerField(default=0)
    count = models.IntegerField(default=0, help_text="pomodoro count")
    completed_cycle_count = models.IntegerField(default=0, help_text="completed pomodoro count")
    completed = models.BooleanField(default=True, help_text="pomodoro status")
    is_break = models.BooleanField(default=False, help_text="Boolean Check for Break")
    
    is_chime_selected = models.BooleanField(default=True)
    chime_music_url = models.CharField(max_length=30, null=True, blank=True)
    selected_music = models.ForeignKey(Music, related_name = 'pomodoro_music', null=True, blank=True, on_delete = models.CASCADE)

    create_date = models.DateField(auto_now_add=True, null=True, blank=True) 
    is_deleted = models.BooleanField(default=False, help_text="to delete the pomodoro")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False,help_text="active")


