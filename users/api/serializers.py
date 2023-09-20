from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from users.models import User

from rest_framework import serializers

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists, generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from rest_auth.serializers import PasswordResetSerializer

from rest_auth.registration.serializers import SocialLoginSerializer



#from django.contrib.auth.forms import PasswordResetForm # It's customizable for both UID/TOKEN and URL
from allauth.account.forms import ResetPasswordForm
from users.models import SocialProfile # Allauth's which provide only alluth urls to reset password

User = get_user_model()


class RESTSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            },
            'full_name': {
                'required': True,
                'allow_blank': False,
            }
        }

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def validate_email(self, email):
        # DRF convention to validate fields
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("This e-mail address already asigned for another users."))
        return email

    def validated_full_name(self, full_name):
        # write here validation for full_name that solve your case
        return full_name

    def create(self, validated_data):
        # Create record in User table
        user = User(
            email=validated_data.get('email'),
            full_name=validated_data.get('full_name'),
            username=generate_unique_username(
                [
                    validated_data.get('full_name'),
                    validated_data.get('email'),
                    'stretch'
                ]
            ),
            #user_type = 'author' # Place more built-in or custom fields there: is_staff=True etc
        )
        user.set_password(validated_data.get('password'))
        user.save()
        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def save(self, request=None):
        # Must override it to save the request data by rest_auth
        return super().save()

class RESTPasswordSerializer(PasswordResetSerializer):
    # solved reset password error
    password_reset_form_class = ResetPasswordForm # Only URL to reset password
    #password_reset_form_class = PasswordResetForm # counter part of django which provide UID/TOKEN even URL, which is customizeable



class CustomSocialLoginSerializer(SocialLoginSerializer):
    pass

    # this is how we send custom fields value below
    """
    is_someone = serializers.BooleanField(required=False, default=False)
    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = attrs['user']
        if attrs.get('is_someone'):
            user.is_someone = True
            user.save()
        return attrs
    """

class SocialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialProfile
        fields = '__all__'
        read_only_fields = ("owner",)
    

    def create(self, validated_data):

        instance = SocialProfile.objects.filter(owner=self.context['request'].user)
        if instance.exists():
            instance.update(**validated_data)
            return SocialProfile.objects.get(owner=self.context['request'].user)
        else:
            instance = SocialProfile.objects.create(
                **validated_data,
                **{'owner': self.context['request'].user}
            )
            return instance

class CreateSocialUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id','full_name','email','social_login_id','social_login_type','username')