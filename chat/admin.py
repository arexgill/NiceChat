from django.utils.html import format_html
from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import UserProfile, Message, Friends, BotPersonality
from .forms import UserProfileForm


@admin.register(BotPersonality)
class BotPersonalityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},  # Makes text areas larger
    }

    list_display = ('name', 'personality_type', 'display_portrait', 'display_avatar')  # Customize as needed
    list_filter = ('personality_type',)

    def portrait_image(self, obj):
        return format_html('<img src="{}" style="width: 150px; height: auto;"/>',
                           obj.portrait.url) if obj.portrait else "No Image"

    def avatar_image(self, obj):
        return format_html('<img src="{}" style="width: 150px; height: auto;"/>',
                           obj.avatar.url) if obj.avatar else "No Image"

    def display_portrait(self, obj):
        if obj.portrait:
            return format_html('<img src="{}" style="width: 50px; height: auto;"/>', obj.portrait.url)
        return "No Portrait"

    display_portrait.short_description = 'Portrait'

    def display_avatar(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width: 50px; height: auto;"/>', obj.avatar.url)
        return "No Avatar"

    display_avatar.short_description = 'Avatar'

    readonly_fields = ['portrait_image', 'avatar_image']
    fieldsets = (
        (None, {
            'fields': (('name', 'personality_type'),
                       ('portrait', 'portrait_image'),
                       ('avatar', 'avatar_image')),
        }),
        ('Personality Profile', {
            'fields': ('predict_prefix', 'prompt_instruction', 'prompt_examples', 'prompt_output_details'),
            'description': "Detailed settings for how this personality should construct and interpret prompts."
        }),
        ('Advanced Settings', {
            'fields': ('context_length', 'tone', 'keywords'),
            'description': "Fine-tune how this personality behaves in conversation."
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('display_avatar_small', 'name', 'email', 'username')
    readonly_fields = ('display_avatar_large',)
    form = UserProfileForm
    filter_horizontal = ('personalities',)  # This adds the filter interface for personalities

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj and not obj.is_bot:
            # If it's not a bot, make bot-specific fields read-only
            for field in ['grounding_source', 'stock_answer', 'personalities']:
                if field in form.base_fields:
                    form.base_fields[field].disabled = True
        return form

    def display_avatar_small(self, obj):
        return self.display_image(obj.avatar, small=True)

    display_avatar_small.short_description = "Avatar"

    def display_avatar_large(self, obj):
        return self.display_image(obj.avatar)

    display_avatar_large.short_description = "Avatar"

    def display_image(self, image_field, small=False):
        if image_field:
            size = '50px' if small else '150px'
            return format_html('<img src="{}" style="width: {}; height: auto;"/>', image_field.url, size)
        return "No Image"

    fieldsets = (
        (None, {
            'fields': (
                'name', 'email', 'username', 'avatar', 'display_avatar_large',
                'is_bot', 'personalities', 'grounding_source', 'stock_answer',
            )
        }),
    )


# Sets the text that appears at the top of each admin page.
admin.site.site_header = 'Nice Chat Administration'

# Sets the text that appears at the top of the admin index page.
admin.site.index_title = 'Site Administration'

# Sets the text that appears in the browser title bar.
admin.site.site_title = 'Nice Chat'

admin.site.register(Message)
admin.site.register(Friends)
