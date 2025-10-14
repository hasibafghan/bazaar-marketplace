from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account , UserProfile
from django.utils.html import format_html

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'username')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    # show profile picture in admin panel
    # def thumbnail(self, object):
    #     return format_html('<img src="{}" width="30" height="30" style="border-radius: 50px;" />'.format(object.profile_picture.url))
    # thumbnail.short_description = 'Profile Picture'

    list_display = ( 'user', 'city', 'state', 'country')
    list_display_links = ( 'user',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'city', 'state', 'country')




admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile , UserProfileAdmin)