from rest_framework import serializers
from .models import Message, UserProfile


class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=UserProfile.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=UserProfile.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content', 'time']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
