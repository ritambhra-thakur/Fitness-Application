from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from users.models import Music
from .models import Pomodoro
from users.serializers import GetMusicSerializer

from pomodoro import models

class PomodoroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pomodoro
        fields = '__all__'

class GetPomodoroSerializer(serializers.ModelSerializer):

    # selected_music = GetMusicSerializer()
    chime_music_url = serializers.SerializerMethodField()
    selected_music = serializers.SerializerMethodField()
    class Meta:
        model = Pomodoro
        fields = '__all__'

    def get_chime_music_url(self, obj):
        try:
            music_obj = Music.objects.get(name = 'Chime')
            return music_obj.id
        except:
            return None

    def get_selected_music(self, obj):
        try:
            if obj.selected_music is None:
                music_obj = Music.objects.get(name = 'White Noise')
                return music_obj.id
            else:
                return obj.selected_music.id
        except:
            return None
        