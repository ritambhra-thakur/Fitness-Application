"""stretch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView
from django.conf.urls.static import static

from users.api.views import FacebookLogin, GoogleLogin, InitialConfigView, SocialProfileViews, SocialLoginUserView
from django.conf.urls import url

# Admin placeholder change
admin.site.site_header = "stretch"
admin.site.site_title = "stretch Admin Panel"
admin.site.index_title = "stretch Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    # path('', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', TemplateView.as_view(template_name='account/profile.html'), name='account_profiles'),
    path('todo/api/v1/', include('todo.urls', namespace='todo')),
    path('challenge/api/v1/', include('challenge.urls', namespace='challenge')),
    path('common/api/v1/', include('common.urls', namespace='common')),
    path('pomodoro/api/v1/', include('pomodoro.urls', namespace='pomodoro')),

    path('initial-config/', InitialConfigView.as_view(), name='initial_config'),
    path('social-profile/', SocialProfileViews.as_view(), name='social_profile'),
    path('social-login/', SocialLoginUserView.as_view(), name='social_profile'),

    url('rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url('rest-auth/google/$', GoogleLogin.as_view(), name='google_login'),

] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


API_INFO = openapi.Info(
    title="stretch API",
    default_version="v1",
    description="API documentation for stretch App",
)

API_DOCS_SCHEMA_VIEWS = get_schema_view(
    API_INFO,
    public=True,
    permission_classes=(AllowAny,),
)

if settings.USE_API_DOCS:
    urlpatterns += [
        path("api-documentation/", API_DOCS_SCHEMA_VIEWS.with_ui("swagger", cache_timeout=0), name="api_playground")
    ]
