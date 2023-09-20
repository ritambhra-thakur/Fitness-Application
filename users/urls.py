from django.urls import path
from .views import *
urlpatterns = [
    path('api/forgot-password/',ForgotPasswordView.as_view(), name="forgot-password"),
    path('api/resend-otp/',ForgotPasswordView.as_view(), name="resend-otp"),
    path('api/forgot-verify-otp/',ForgotVerifyOtpView.as_view(), name="forgot-password-verify-otp"),
    path('api/reset-password/',ChangePasswordView.as_view(), name="reset-password"),

    path('api/music/list',GetMusicListView.as_view(), name="reset-password"),
    path('api/music/create',CreateMusicListView.as_view(), name="reset-password"),
    path('api/music/set-default/<int:pk>/',UpdateDefaultSound.as_view(), name="reset-password"),
    path('api/user/get-profile-by-token/',GetProfileByTokenView.as_view(), name="reset-password"),


    path("get-profile-details/", GetProfileDetailView.as_view()),
    path("update-username-by-token/", UpdateUsernameView.as_view()),

    path("delete-user/", DeleteUserView.as_view()),
    path("policies/", fetch_privacy_policies),

    path('revenue-cat/webhook/get-info/', RevenueCatWebhookView.as_view()),

    path('revenue-cat/webhook-test/', TestRevenueCatWebhookView.as_view()),
    # path('revenue-cat/save-id/', SaveRevenueCatIDView.as_view()),
]