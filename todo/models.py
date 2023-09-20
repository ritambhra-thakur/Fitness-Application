from django.db import models
from django.conf import settings
from common.models import NameDescriptionWiseModels, Tags, Emoji
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Todo(NameDescriptionWiseModels):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="todo_created_by",
        on_delete=models.CASCADE,
    )
    due_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    priority = models.PositiveIntegerField(blank=True, null=True)
    reminder_time = models.TimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tags, blank=True)
    emoji = models.ForeignKey(
        Emoji,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    time = models.TimeField(null=True, blank=True)
    reminder_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name