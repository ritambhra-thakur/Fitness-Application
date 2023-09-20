from rest_framework import serializers
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import get_object_or_404

import facebook
from django.core.mail import send_mail
from django.conf import settings




from users.models import User
from challenge.models import FriendChallenge, FriendInvitationChallange, GoalDetail, CompletionDetails, ChallengeMessages
from todo.serializers import ToDoGetSerializer
from pomodoro.serializers import GetPomodoroSerializer
from common.serializers import TimelineSerializer, GetTypeSerializer, GetCategorySerializer, GetUnitsSerializer
from users.serializers import GetUserDetailSerializer
from common.serializers import CreateCompletionDetailsSerializer, GetMessageEmojiSerializer
# from utils.saveTaskCompletionDetails import save_completion_details
class FriendChallengeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendChallenge
        fields = '__all__'
        # exclude = ('owner', )
    
    def create(self, validated_data):
        # category = validated_data.pop('category', '')
        instance = self.Meta.model.objects.create(
            **validated_data
        )

        # if category:
        #     instance.category.set(category)
        #     instance.save()
        return instance

class CreateupdateGoalsDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoalDetail
        fields = ('__all__')


class GetFriendChallengeSerializer(serializers.ModelSerializer):

    category = GetCategorySerializer()
    timeline = TimelineSerializer()
    type = GetTypeSerializer()
    goal_completed = serializers.SerializerMethodField()
    is_challenge_completed = serializers.SerializerMethodField()
    goal_details = serializers.SerializerMethodField()
    goal_unit = GetUnitsSerializer()
    own_friend_challenge = serializers.SerializerMethodField()
    friend_challenges = serializers.SerializerMethodField()
    owner = GetUserDetailSerializer()
    total_points = serializers.SerializerMethodField()

    class Meta:
        model = FriendChallenge
        fields = '__all__'
        # exclude = ('owner', )

    def get_goal_completed(self, obj):
        count = GoalDetail.objects.filter(is_completed=True, challenge = obj.id).count()
        return count
    
    def get_is_challenge_completed(self, obj):
        completed_count = GoalDetail.objects.filter(is_completed=True, challenge = obj.id).count()
        try:
            target_count = obj.timeline.number_of_days
            if int(target_count) == int(completed_count):
                if obj.challenger is None:
                    save_completion_details(task_type = 4, task_id = obj.id, user_id = obj.owner.id)
                if obj.owner.id == obj.challenger.id:
                    save_completion_details(task_type = 3, task_id = obj.id, user_id = obj.owner.id)
                else:
                    save_completion_details(task_type = 4, task_id = obj.id, user_id = obj.owner.id)
                return True
            else:
                return False 
        except:
            return None

    def get_goal_details(self, obj):
        # try:
        date = self.context.get('date')
        try:
            goal_obj = GoalDetail.objects.get(challenge = obj.id, date = date)
            goal_data = CreateupdateGoalsDetailsSerializer(goal_obj).data
            return goal_data
        except:
            return None
        # except:
        #     return None
        # final_result = {}
        # for goal  in goal_data:
        #     final_result[goal['date']] = goal
        # return final_result

    def get_own_friend_challenge(self, obj):
        request = self.context.get('request')
        if request:
            if int(request.user.id) == int(obj.owner.id) and obj.challenger is None:
                return True
            else:
                return False
        else:
            return None
    
    def get_friend_challenges(self, obj):
        child_challenge = FriendChallenge.objects.filter(parent_challenge = obj.id)
        return GetFriendChallengeSerializer(child_challenge, many=True).data

    def get_total_points(self, obj):
        goal_details_obj = GoalDetail.objects.filter(challenge = obj.id)
        res = 0
        for goal_detail in goal_details_obj:
            if goal_detail.points is not None:
                res += int(goal_detail.points)
        return res


class FriendInvitationChallangeSerializer(serializers.ModelSerializer):
    emails = serializers.ListField(
        child = serializers.EmailField(),
        write_only=True
    )
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = FriendInvitationChallange
        exclude = ('owner',)
        read_only_fields = ("facebook_response", "invited_via", 'id', 'email', 'is_accepted', 'invitee',)

    
    def validate_emails(self, emails):
        if FriendInvitationChallange.objects.filter(email__in=emails).exists():
            raise serializers.ValidationError('You already invited to the challenge with one of the email, You cant double invite')
        return emails
    
    def create(self, validated_data):
        get_object_or_404(FriendChallenge, owner=self.context['request'].user, id=validated_data.get('challenge').id)

        emails = validated_data.pop('emails', [])

        if emails:
            for email in emails:
                instance = self.Meta.model.objects.create(
                    **{
                        'email': email,
                        'owner': self.context['request'].user,
                        'challenge': validated_data.get('challenge'),
                    }
                )

                send_mail(
                    'Invitation to accept a challenge',
                    'Here you go for the challenge link: https://stretchyo.page.link/LdvY2EV7SN5Vaq4FA?pk={} or you can use this code to accept {}'.format(instance.id, instance.id),
                    str(getattr(settings, 'DEFAULT_FROM_EMAIL')),
                    [instance.email],
                    fail_silently=False,
                )
        return emails






class AcceptInvitationChallangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendInvitationChallange
        fields = ('id',)
    

class SaveInvitationResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendInvitationChallange
        fields = ('__all__')


class GetInvitationResponseSerializer(serializers.ModelSerializer):

    owner = serializers.SerializerMethodField()
    challenge = GetFriendChallengeSerializer()
    # invitee = GetUserDetailSerializer()

    class Meta:
        model = FriendInvitationChallange
        fields = ('__all__')
    
    def get_owner(self, obj):
        res = {
            "email":obj.owner.email,
            "username":obj.owner.username,
            "full_name":obj.owner.full_name
        }

        return res
        
class GetCompletionDetailsSerializer(serializers.ModelSerializer):
    todo = ToDoGetSerializer()
    pomodoro = GetPomodoroSerializer()
    self_challenge = GetFriendChallengeSerializer()
    friend_challenge = GetFriendChallengeSerializer()

    class Meta:
        model = CompletionDetails
        fields = '__all__'

def save_completion_details(task_type, task_id, user_id):
    data = {"task_type":task_type,"owner":user_id}
    if int(task_type) == 1:
        try:
            comp_obj = CompletionDetails.objects.get(todo = task_id)
            return False
        except:
            data['todo'] = task_id
    elif int(task_type) == 2:
        try:
            comp_obj = CompletionDetails.objects.get(pomodoro = task_id)
            return False
        except:
            data['pomodoro'] = task_id
    elif int(task_type) == 3:
        try:
            comp_obj = CompletionDetails.objects.get(self_challenge = task_id)
            return False
        except:
            data['self_challenge'] = task_id
    elif int(task_type) == 4:
        try:
            comp_obj = CompletionDetails.objects.get(friend_challenge = task_id)
            return False
        except:
            data['friend_challenge'] = task_id
    else:
        return "Incorrect Task Type"


    serializer = CreateCompletionDetailsSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return True
    else:
        return str(serializer.errors)


class CreateChallengeMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChallengeMessages
        fields = '__all__'

class GetChallengeMessageSerializer(serializers.ModelSerializer):
    sender = GetUserDetailSerializer()
    receiver = GetUserDetailSerializer()
    media = GetMessageEmojiSerializer()
    friend_challenge = GetFriendChallengeSerializer()
    show_type = serializers.SerializerMethodField()
    class Meta:
        model = ChallengeMessages
        fields = '__all__'

    def get_show_type(self, obj):
        user_id = self.context.get('request').user.id
        try:
            if int(obj.sender.id) == int(user_id):
                return 2
            else:
                return 1
        except:
            return 0