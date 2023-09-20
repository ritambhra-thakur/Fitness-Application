from django.db import models
from django.utils.translation import ugettext_lazy as _


class CategoryType(models.TextChoices):
    SPORTS = 'SPORTS', _('Sports')
    THOUGHT = 'THOUGHT', _("Thoughts")
    EXCERCISE = 'EXCERCISE', _('Exercises')