from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, Message, Friends, BotPersonality
from .forms import BotPersonalityForm, UserProfileForm


class BotPersonalityAdmin(admin.ModelAdmin):
    form = BotPersonalityForm
    list_display = ('display_avatar_small', 'name', 'personality_type')
    readonly_fields = ('display_avatar_large', 'display_portrait_large')

    def display_avatar_small(self, obj):
        return self.display_image(obj.avatar, small=True)
    display_avatar_small.short_description = "Bot Avatar"

    def display_avatar_large(self, obj):
        return self.display_image(obj.avatar)
    display_avatar_large.short_description = "Avatar"

    def display_portrait_large(self, obj):
        return self.display_image(obj.portrait)
    display_portrait_large.short_description = "Portrait"

    def display_image(self, image_field, small=False):
        if image_field:
            size = '50px' if small else '150px'
            return format_html('<img src="{}" style="width: {}; height: auto;"/>', image_field.url, size)
        return "No Image"

    fieldsets = (
        (None, {
            'fields': ('name', 'personality_type', 'avatar', 'display_avatar_large', 'portrait', 'display_portrait_large', 'predict_prefix')
        }),
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'username', 'display_avatar_small')
    readonly_fields = ('display_avatar_large',)
    form = UserProfileForm

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
            'name', 'email', 'username', 'avatar', 'is_bot', 'personalities', 'grounding_source', 'stock_answer',
            'display_avatar_large')
        }),
    )


admin.site.register(Message)
admin.site.register(Friends)
admin.site.register(BotPersonality, BotPersonalityAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
