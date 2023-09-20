
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from users.models import SocialProfile


User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (("User", {"fields": ("full_name", 'avatar')}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["full_name", "email", "is_superuser", "is_active", "is_staff"]
    search_fields = ["name", "email",]


admin.site.register(SocialProfile)