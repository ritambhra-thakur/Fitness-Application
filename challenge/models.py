from contextlib import nullcontext
from email.policy import default
from hashlib import blake2b
from re import T
import uuid
from django.db import models
from common.models import BaseModels, Category, NameWiseModels, Timeline, Type, Units
from todo.models import Todo
from pomodoro.models import Pomodoro
from users.models import User
from common.models import MessageEmoji

class FriendChallenge(NameWiseModels):
    owner = models.ForeignKey( # created by
        User,
        on_delete=models.CASCADE,
        related_name="friend_challenge"
    )
    challenger = models.ForeignKey( # who made challenge
        User,
        on_delete=models.SET_DEFAULT,
        related_name="friend_challenger",
        null=True,
        blank=True,
        default=None
    )
    start_date = models.DateField()
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete = models.CASCADE
        
    )
    type = models.ForeignKey(
        Type,
        blank=True,
        null=True,
        on_delete = models.CASCADE
        
    )
    time = models.TimeField(null=True, blank=True)
    timeline = models.ForeignKey(
        Timeline,
        related_name="friend_challenge",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    goal_value = models.CharField(null=True, blank=True, max_length=255)
    goal_unit = models.ForeignKey(Units, null=True, blank=True, on_delete = models.CASCADE, related_name = 'unit_challenge')
    parent_challenge = models.ForeignKey('self', null=True, blank=True, default=None, on_delete = models.CASCADE, related_name = 'parent_friend_challenge')
    is_active = models.BooleanField(default=True)
    is_reminder = models.BooleanField(default=True)

class GoalDetail(BaseModels):

    challenge = models.ForeignKey(FriendChallenge, null=True, blank=True, on_delete=models.CASCADE, related_name = 'goal_details')
    date = models.DateField(null=True, blank=True)
    goal_value = models.CharField(max_length=10, null=True, blank=True)
    target_goal_value = models.CharField(max_length=10, null=True, blank=True)
    points = models.CharField(max_length=20, null=True, blank=True)
    is_skipped = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_reminder = models.BooleanField(default=True)

class ChallengeUser(BaseModels):
    challenge = models.ForeignKey(
        FriendChallenge,
        on_delete=models.CASCADE,
        related_name="challenge_user",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="challenge_user"
    )

class  FriendInvitationChallange(BaseModels):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    owner = models.ForeignKey( # who sent the invitation
        User,
        on_delete=models.CASCADE,
    )
    challenge = models.ForeignKey(
        FriendChallenge,
        on_delete=models.CASCADE,
        related_name="friend_invitation_challange"
    )
    invitee = models.ForeignKey( # to whom invitation is sent
        User,
        on_delete=models.CASCADE,
        related_name="friend_invitation_challange",
        null=True,
        blank=True
    )
    # email = models.EmailField(unique=False, null=True, blank=True)
    # invited_via = models.CharField(null=True, blank=True, max_length=255)
    # facebook_response = models.JSONField(default=dict, null=True, blank=True)
    is_accepted = models.BooleanField(default=None, null=True, blank=True)
    
    # class Meta:
    #     unique_together = ("challenge", "email",)

class CompletionDetails(models.Model):
    task_type = models.IntegerField(null=True, blank=True, help_text="1 - Todo, 2 - Pomodoro, 3- Self Challenge, 4 - Friend Challenge")
    todo = models.ForeignKey(Todo, null=True, blank=True, on_delete=models.CASCADE)
    pomodoro = models.ForeignKey(Pomodoro, null=True, blank=True, on_delete=models.CASCADE)
    self_challenge = models.ForeignKey(FriendChallenge, null=True, blank=True, on_delete=models.CASCADE, related_name="self_challenge_completion_details")
    friend_challenge = models.ForeignKey(FriendChallenge, null=True, blank=True, on_delete=models.CASCADE, related_name="friend_challenge_completion_details")
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class ChallengeCompletionMessage(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    body = models.CharField(max_length=100, null=True, blank=True)
    message_type = models.IntegerField(unique=True, help_text='1. Self Challenge , 2. Friend Challenge')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class ChallengeMessages(models.Model):
    sender = models.ForeignKey(User, null=True, blank=True, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, null=True, blank=True, related_name='receiver_messages', on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    media = models.ForeignKey(MessageEmoji, null=True, blank=True, related_name='media_messages', on_delete=models.CASCADE)
    friend_challenge = models.ForeignKey(FriendChallenge, null=True, blank=True, related_name='challenge_messages', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)