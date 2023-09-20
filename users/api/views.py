
from rest_framework import generics
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from users.api.serializers import CustomSocialLoginSerializer, SocialProfileSerializer, CreateSocialUserSerializer
from users.models import User

from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.views import APIView
from django.conf import settings

from users.permission import IsOwnerOrReadOnly
from users.models import SocialProfile
import jwt
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    serializer_class = CustomSocialLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)



class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    serializer_class = CustomSocialLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class InitialConfigView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        config = {
            'social': {
                'FACEBOOK_CLIENT_ID': getattr(settings, 'FACEBOOK_CLIENT_ID', ''),
                'GOOGLE_CLIENT_ID': getattr(settings, 'GOOGLE_CLIENT_ID', ''),

                'FACEBOOK_CLIENT_ID': getattr(settings, 'FACEBOOK_INTEGRATION_CLIENT_ID', ''),
                'GOOGLE_CLIENT_ID': getattr(settings, 'FACEBOOK_INTEGRATION_SECRET_KEY', ''),
            }
        }
        return Response(config)

class SocialProfileViews(generics.ListCreateAPIView):
    
    serializer_class = SocialProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    
    def get_queryset(self):
        return SocialProfile.objects.filter(owner=self.request.user)

class SocialLoginUserView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        operation_description="Social Login API",
        operation_summary="Social Login API",
        request_body=CreateSocialUserSerializer,
    )

    def post(self, request, format=None):

        if 'social_login_id' in request.data and 'social_login_type' in request.data:
            request.data['username'] = request.data['social_login_id']
            try:
                user_obj = User.objects.get(social_login_id = request.data['social_login_id'], social_login_type = request.data['social_login_type'])
                serializer = CreateSocialUserSerializer(user_obj)
            except Exception as e:
                serializer = CreateSocialUserSerializer(data = request.data)
                if serializer.is_valid():
                    serializer.save()
                    user_obj = User.objects.get(id = serializer.data['id'])
                else:
                    return Response({"data":serializer.errors, "message":"Some Error Occured"}, status = 400)

            payload = jwt_payload_handler(user_obj)
            token = jwt.encode(payload, settings.SECRET_KEY)
            user_details = serializer.data
            user_details['token'] = token
            return Response({"data":user_details, "message":"OK"}, status = 200)
            