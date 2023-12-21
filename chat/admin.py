from django.contrib import admin
from .models import UserProfile, Message, Friends, BotPersonality

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Friends)
admin.site.register(BotPersonality)
