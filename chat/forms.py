from django import forms
from .models import BotPersonality, UserProfile


class BotPersonalityForm(forms.ModelForm):
    class Meta:
        model = BotPersonality
        fields = '__all__'
        widgets = {
            'predict_prefix': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Adjust rows and cols as needed
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'