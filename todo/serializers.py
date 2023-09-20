from datetime import datetime
from re import L
from rest_framework import serializers
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from utils.checkUserSubscription import check_user_subscription


from users.models import User
from todo.models import Todo

from common.serializers import TagSerializer, EmojiSerializer
class ToDoCreateSerializer(serializers.ModelSerializer):

    todo_status = serializers.SerializerMethodField()
    # emoji = serializers.SerializerMethodField()
    class Meta:
        model = Todo
        exclude = ('owner',)

    # def get_emoji(self, obj):
    #     if obj.emoji is not None:
    #         serializer = EmojiSerializer(obj.emoji)
    #         return serializer.data
    #     else:
    #         return None


    def get_todo_status(self, obj):
        current_time = self.context.get('current_time')
        if current_time:
            if obj.is_completed is True:
                return 'Completed'
            elif obj.due_date > datetime.now().date():
                return 'Active'
            elif obj.due_date == datetime.now().date():
                current_time = datetime.strptime(current_time, '%H:%M:%S')
                if obj.time < current_time.time():
                    return 'PassedOut'
                else:
                    return 'Active'
            else:
                return 'PassedOut'
        else:
            return None
    
    def create(self, validated_data):
        check_resp = check_user_subscription(self.context['request'], 1)
        if check_resp['result'] is True:
            tags = validated_data.pop('tags', '')
            instance = self.Meta.model.objects.create(
                **validated_data,
                **{
                    'owner': self.context['request'].user,
                }
            )
            if tags:
                instance.tags.set(tags)
                instance.save()
            return instance
        else:
            raise serializers.ValidationError({"data":None, "message":check_resp['detail'], "status":400})

class ToDoGetSerializer(serializers.ModelSerializer):

    todo_status = serializers.SerializerMethodField()
    emoji = serializers.SerializerMethodField()
    tags_name = serializers.SerializerMethodField()
    class Meta:
        model = Todo
        exclude = ('owner',)

    def get_emoji(self, obj):
        if obj.emoji is not None:
            serializer = EmojiSerializer(obj.emoji)
            return serializer.data
        else:
            return None
    
    def get_tags_name(self, obj):
        tag_obj = obj.tags.values_list('name', flat=True)
        return tag_obj


    def get_todo_status(self, obj):
        current_time = self.context.get('current_time')
        if current_time:
            if obj.is_completed is True:
                return 'Completed'
            elif obj.due_date > datetime.now().date():
                return 'Active'
            elif obj.due_date == datetime.now().date():
                current_time = datetime.strptime(current_time, '%H:%M:%S')
                if obj.time < current_time.time():
                    return 'PassedOut'
                else:
                    return 'Active'
            else:
                return 'PassedOut'
        else:
            return None