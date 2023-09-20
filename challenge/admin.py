from django.contrib import admin

from challenge.models import FriendChallenge, FriendInvitationChallange, Category, ChallengeCompletionMessage

admin.site.register(FriendInvitationChallange)
admin.site.register(FriendChallenge)
admin.site.register(Category)
admin.site.register(ChallengeCompletionMessage)
