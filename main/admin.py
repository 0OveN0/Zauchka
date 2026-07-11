from django.contrib import admin
from .models import Olympiad, Profile, Comment, BannedWord, SiteSetting, CustomTheme, SupportThread, SupportMessage, ThemePreset, FavoriteItem


@admin.register(Olympiad)
class OlympiadAdmin(admin.ModelAdmin):
    list_display = ('public_number', 'title', 'listing_type', 'organizer', 'target_audience', 'stage', 'format', 'region', 'start_date', 'end_date', 'is_approved')
    list_filter = ('is_approved', 'listing_type', 'target_audience', 'stage', 'format', 'region')
    search_fields = ('title', 'organizer', 'region', 'description', '=public_number')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'region', 'is_banned', 'last_login', 'last_activity', 'can_upload_photo', 'can_change_username', 'can_comment', 'pd_agreement', 'cookies_agreement')
    list_filter = ('is_banned', 'pd_agreement', 'cookies_agreement', 'show_region', 'show_online_status')
    search_fields = ('user__username', 'region', 'bio')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'olympiad', 'created_at', 'is_approved', 'is_deleted', 'deleted_by')
    list_filter = ('is_approved', 'is_deleted', 'created_at')
    search_fields = ('text', 'user__username', 'olympiad__title')


@admin.register(BannedWord)
class BannedWordAdmin(admin.ModelAdmin):
    search_fields = ('word',)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key',)


@admin.register(ThemePreset)
class ThemePresetAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'card_style', 'is_builtin', 'sort_order', 'updated_at')
    list_filter = ('card_style', 'is_builtin')
    search_fields = ('name', 'key')


@admin.register(CustomTheme)
class CustomThemeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Брендинг и звуки', {
            'fields': ('site_name', 'site_logo', 'send_sound', 'send_sound_volume', 'notification_sound', 'notification_sound_volume', 'report_sound', 'report_sound_volume', 'support_open_sound', 'support_open_sound_volume', 'support_close_sound', 'support_close_sound_volume', 'sound_enabled_default')
        }),
        ('Виджет обращения к админу', {
            'fields': ('support_widget_title', 'support_widget_gif', 'support_widget_text')
        }),
        ('Старый CSS оригинальной темы', {
            'fields': ('custom_css',),
            'classes': ('collapse',),
        }),
    )



class SupportMessageInline(admin.TabularInline):
    model = SupportMessage
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(SupportThread)
class SupportThreadAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'kind', 'status', 'updated_at')
    list_filter = ('kind', 'status', 'updated_at')
    search_fields = ('subject', 'user__username')
    inlines = [SupportMessageInline]


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('thread', 'sender', 'is_admin', 'read_by_admin', 'read_by_user', 'created_at')
    list_filter = ('is_admin', 'read_by_admin', 'read_by_user', 'created_at')
    search_fields = ('text', 'sender__username', 'thread__subject')


@admin.register(FavoriteItem)
class FavoriteItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'olympiad', 'created_at')
    search_fields = ('user__username', 'olympiad__title', '=olympiad__public_number')
