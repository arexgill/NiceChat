from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.html import format_html, mark_safe
from .models import BotPersonality, UserProfile

# class BotPersonalityForm(forms.ModelForm):
#     class Meta:
#         model = BotPersonality
#         fields = '__all__'
#         widgets = {
#             'predict_prefix': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Adjust rows and cols as needed
#         }



class AvatarCheckboxSelectMultiple(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        # Assuming 'avatar' is the field in BotPersonality model that contains the image URL
        bot_personalities = BotPersonality.objects.all()
        replacements = {
            str(bot_personality.id): format_html(
                '<img src="{}" alt="{}" style="height: 20px; width: 20px; margin-right: 5px; border-radius: 50%;" />{}',
                bot_personality.avatar.url,
                bot_personality.name,
                bot_personality.name
            )
            for bot_personality in bot_personalities
        }
        for bot_id, replacement in replacements.items():
            output = output.replace(f'>{bot_id}<', f'>{replacement}<')
        return mark_safe(output)


class UserProfileForm(forms.ModelForm):
    personalities = forms.ModelMultipleChoiceField(
        queryset=BotPersonality.objects.all(),
        widget=AvatarCheckboxSelectMultiple,  # Use the custom widget
        required=False
    )

    class Meta:
        model = UserProfile
        fields = '__all__'
