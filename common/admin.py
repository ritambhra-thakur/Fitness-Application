from django.contrib import admin

from common.models import Emoji, Tags, Timeline, Type, Units, CategoryEmoji, TypeEmoji, MessageEmoji

admin.site.register(Emoji)
admin.site.register(Tags)
admin.site.register(Timeline)
admin.site.register(Type)
admin.site.register(Units)
admin.site.register(TypeEmoji)
admin.site.register(CategoryEmoji)
admin.site.register(MessageEmoji)