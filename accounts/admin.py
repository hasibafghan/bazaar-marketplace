from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account , UserProfile



# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'is_admin', 'is_staff', 'is_active', 'is_super_admin', 'date_joined')
#     link_display_links = ('id', 'first_name', 'last_name', 'username', 'email')
#     search_fields = ('email', 'username')
#     list_filter = ('is_admin', 'is_staff', 'is_active', 'is_super_admin')
#     ordering = ('-date_joined',)
#     list_per_page = 15
#     readonly_fields = ('id', 'date_joined','last_login')


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'username')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile)


    # def has_add_permission(self, request):
    #     return request.user.is_superuser
        
    # def has_change_permission(self, request, obj=None):
    #     return request.user.is_superuser
        
    # def has_delete_permission(self, request, obj=None):
    #     return request.user.is_superuser
        
    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser
        
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.none()