from django.contrib import admin
from .models import UserProfile, Message, Friends

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Friends)
