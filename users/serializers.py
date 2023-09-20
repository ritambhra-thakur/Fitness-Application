from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .models import Music, User, UserRevenueCatMapper, UserSubscriptionDetails

class GetMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'


class GetUserDetailSerializer(serializers.ModelSerializer):

    default_sound = GetMusicSerializer()
    class Meta:
        model = User
        exclude = ['password','social_login_id','social_login_type','otp_verification','otp','otp_send_time','groups','user_permissions']

class CreateUserRevenueCatMapperSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRevenueCatMapper
        fields = '__all__'
        

class SaveUserSubscriptionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSubscriptionDetails
        fields = '__all__'