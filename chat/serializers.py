from rest_framework import serializers
from .models import Messages, UserProfile


class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=UserProfile.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=UserProfile.objects.all())

    class Meta:
        model = Messages
        fields = ['sender', 'receiver', 'content', 'time']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
