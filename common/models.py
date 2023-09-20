from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.stretch_enum import CategoryType
from users.models import User

class BaseModels(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class NameWiseModels(BaseModels):
    name = models.CharField(_("Name"), max_length=255)
    class Meta:
        abstract = True


class NameDescriptionWiseModels(NameWiseModels):
    description = models.TextField(_("Description"), max_length=1000)
    class Meta:
        abstract = True



class MoneyMixingModel(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=6, default=0.00)

    class Meta:
        abstract = True

class TypeEmoji(BaseModels):
    code = models.CharField(_("name"), max_length=30, unique=True)
    file = models.ImageField(upload_to="type_emoji")
    is_active = models.BooleanField(default=True)

class CategoryEmoji(BaseModels):
    code = models.CharField(_("name"), max_length=30, unique=True)
    file = models.ImageField(upload_to="categories_emoji")
    is_active = models.BooleanField(default=True)

class Tags(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags", null=True, blank=True)
    code = models.CharField(_("code"), max_length=15)
    name = models.CharField(_("Name"), max_length=15) # Translable level

    # class Meta:
        # unique_together = ('owner', 'code',)

    def __str__(self):
        return self.name

class Units(models.Model):
    name = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=15)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_category",
        null=True,
        blank=True
    )
    category_image = models.ForeignKey(
        CategoryEmoji,
        on_delete=models.CASCADE,
        related_name="category_emoji",
        null=True,
        blank=True
    )
    default = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name



class Type(models.Model):
    name = models.CharField(max_length=30, help_text="Enter the name", null=True, blank=True,) 
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_type",
        null=True,
        blank=True
    )
    type_image = models.ForeignKey(
        TypeEmoji,
        on_delete=models.CASCADE,
        related_name="type_emoji",
        null=True,
        blank=True
    )
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, related_name = 'type_category')
    default = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False, help_text="to delete the Type")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False,help_text="active")

    def __str__(self):
        return self.name


class Timeline(models.Model):
    number_of_days = models.IntegerField(_("Number of Days"))
    is_deleted = models.BooleanField(default=False, help_text="to delete the pomodoro")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False,help_text="active")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_timeline")
    code = models.CharField(max_length=100, help_text="Enter the Code")

class Files(NameWiseModels):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    file = models.FileField()


class Images(NameWiseModels):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    file = models.FileField()


class Emoji(BaseModels):
    code = models.CharField(_("name"), max_length=30, unique=True)
    file = models.ImageField(upload_to="emoji")

class MessageEmoji(BaseModels):
    code = models.CharField(_("code"), max_length=15)
    name = models.CharField(_("Name"), max_length=15)
    file = models.ImageField(upload_to="emoji")
    is_active = models.BooleanField(default=True)

