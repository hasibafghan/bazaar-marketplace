from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'is_admin', 'is_staff', 'is_active', 'is_super_admin')
    search_fields = ('email', 'username')
    list_filter = ('is_admin', 'is_staff', 'is_active', 'is_super_admin')
    ordering = ('-date_joined',)
    list_per_page = 15

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