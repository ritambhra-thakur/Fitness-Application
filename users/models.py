from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings



class Music(models.Model):
    name = models.CharField(max_length=30, unique=True, help_text="Enter the tittle name", null=True, blank=True)
    file = models.FileField(upload_to="sounds/",blank=True, null=True, help_text="Select file")
    sequence_id = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, help_text="to delete the music")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False,help_text="active")
class User(AbstractUser):
    full_name = models.CharField(_("Full Name"), blank=True, null=True, max_length=255)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    social_login_id = models.CharField(max_length = 500, null=True, blank=True)
    social_login_type = models.IntegerField(null=True, blank=True, help_text = '1. Facebook, 2. Google')
    name = models.CharField(max_length = 500, null=True, blank=True)
    default_sound = models.ForeignKey(Music, null=True, blank=True, related_name = 'user_default_sounds', on_delete = models.CASCADE)
    otp = models.IntegerField(null=True, blank=True)
    otp_verification = models.BooleanField(default=True)
    otp_send_time = models.DateTimeField(blank=True, null=True)


class SocialProfile(models.Model):
    """
        Store user sensitive social info to get user friend list, sending invitation etc.
    """
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    facebook_access_token = models.CharField(_("Facebook token"), max_length=1000, null=True, blank=True)
    facebook_response = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    facebook_email = models.EmailField(_("Facebook email"), blank=True, null=True, unique=True)

    def __str__(self):
        return self.owner.username
    
    class Meta:
        verbose_name = _("Social Permission")
        verbose_name_plural  = _("Social Permissions")


class UserSubscriptionDetails(models.Model):

    user = models.ForeignKey(User, null=True, blank=True, related_name='user_subscriptions', on_delete=models.CASCADE)
    webhook_response = models.JSONField(null=True, blank=True)
    starts_on = models.BigIntegerField(null=True, blank=True)
    ends_on = models.BigIntegerField(null=True, blank=True)
    event_type = models.CharField(max_length=100, null=True, blank=True, default='RENEWAL')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserRevenueCatMapper(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    revenue_cat_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

