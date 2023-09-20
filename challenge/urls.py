from django.urls import path
from rest_framework.routers import DefaultRouter

from challenge import views

app_name = "challenge"

urlpatterns = [
    path("friend-invitation/", views.FriendInvitationChallangeAPIView.as_view(), name="friend-invitation"),
    path("accept-invitation/<uuid:pk>/", views.AcceptInvitationChallangeAPIView.as_view(), name="accept-invitation"),
    path("get-facebook-friend-list/", views.GetMyFacebookFriendList.as_view(), name="get_facebook_friend_list"),
    
    # API's with diffrent pattern
    # Challenge
    # path("sendchallenge/get/<int:id>/", views.GetFriendChallenge.as_view()),
    # path("sendchallenge/list/", views.GetAllFriendChallenge.as_view()),
    # path("sendchallenge/create/", views.CreateFriendChallenge.as_view()),
    # path("sendchallenge/update/<int:id>/", views.UpdateFriendChallenge.as_view()),
    # path("sendchallenge/delete/<int:id>/", views.DeleteFriendChallenge.as_view()),


    # # Self Challenge
    path("selfchallenge/get/<int:id>/", views.GetSelfChallenge.as_view()),
    path("selfchallenge/list/", views.GetAllSelfChallenge.as_view()),
    path("selfchallenge/update/<int:pk>/", views.UpdateSelfChallenge.as_view()),
    path("selfchallenge/create/", views.CreateSelfChallenge.as_view()),
    path("selfchallenge/delete/<int:pk>/", views.DeleteSelfChallenge.as_view()),
    path("selfchallenge/delete-by-owner-id/", views.DeleteSelfChallengeByOnwer.as_view()),

    # Friend Challenge
    path("friend-challenge/get/<int:id>/", views.GetFriendChallenge.as_view()),
    path("friend-challenge/list/", views.GetAllFriendChallenge.as_view()),
    path("friend-challenge/update/<int:pk>/", views.UpdateSelfChallenge.as_view()),
    path("friend-challenge/create/", views.CreateSelfChallenge.as_view()),   # owner = request.user.id and #challenger - Null
    path("friend-challenge/delete/<int:pk>/", views.DeleteSelfChallenge.as_view()),
    path("friend-challenge/delete-by-owner-id/", views.DeleteSelfChallengeByOnwer.as_view()),

    path("accept-challenge-invite/", views.AcceptChallengeInviteView.as_view()),

    path("create-invitation/", views.CreateInvitaitonView.as_view()),
    path("get-invitation/", views.GetInvitaitonsView.as_view()),


    # Goal Details
    path("goal-details/create-update/", views.CreateUpdateGoalDetails.as_view()),


    path("delete-all-self-challenges-by-token/", views.DeleteAllSelfChallenges.as_view()),

    #messaging
    path("send-challenge-completion-message/", views.SendChallengeCompletionMessageView.as_view()),
    path("get-challenge-completion-messages/", views.GetChallengeCompletionMessageView.as_view()),
    path("get-unread-message-count/", views.GetUnReadMessageCount.as_view()),
]
router = DefaultRouter()

router.register(r'friend-challenge', views.FriendChallengeViewSets, basename='challenge')



urlpatterns += router.urls