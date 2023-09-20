from rest_framework import serializers
from django.db import transaction
from django.utils.translation import ugettext_lazy as _


from common.models import Tags, Emoji, Timeline, Category, Type, Units, CategoryEmoji, TypeEmoji, MessageEmoji
from challenge.models import CompletionDetails
from todo.models import Todo

class TagSerializer(serializers.ModelSerializer):


    class Meta:
        model = Tags
        fields = '__all__'
        read_only_fields = ("owner",)


    def create(self, validated_data):
        if validated_data['name'].lower() in ['home', 'office', 'work', 'urgent']:
            raise serializers.ValidationError({"message":"Duplicate Tag Name for this user."})
        existing_obj = Tags.objects.filter(owner = self.context['request'].user, name = validated_data['name']).count()
        if existing_obj > 0:
            raise serializers.ValidationError({"message":"Duplicate Tag Name for this user."})
        instance = Tags.objects.create( 
            **validated_data,
            **{'owner': self.context['request'].user}
        )
        return instance

class GetTagSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tags
        fields = '__all__'
        read_only_fields = ("owner",)

    def get_name(self, obj):
        return obj.name.upper()

    def create(self, validated_data):
        if validated_data['name'].lower() in ['home', 'office', 'work', 'urgent']:
            raise serializers.ValidationError({"message":"Duplicate Tag Name for this user."})
        existing_obj = Tags.objects.filter(owner = self.context['request'].user, name = validated_data['name']).count()
        if existing_obj > 0:
            raise serializers.ValidationError({"message":"Duplicate Tag Name for this user."})
        instance = Tags.objects.create( 
            **validated_data,
            **{'owner': self.context['request'].user}
        )
        return instance


class EmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoji
        fields = '__all__'


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class GetTypeEmojiSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeEmoji
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class GetTypeSerializer(serializers.ModelSerializer):

    type_image = GetTypeEmojiSerializer()

    
    class Meta:
        model = Type
        fields = '__all__'

class GetUnitsSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Units
        fields = '__all__'


class GetCategoryEmojiSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = CategoryEmoji
        fields = '__all__'

class GetMessageEmojiSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageEmoji
        fields = '__all__'


class GetCategorySerializer(serializers.ModelSerializer):

    type_category = GetTypeSerializer(many=True)
    category_image = GetCategoryEmojiSerializer()
    class Meta:
        model = Category
        fields = '__all__'

class CreateCompletionDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompletionDetails
        fields = '__all__'

