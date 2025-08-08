from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'description', 'category_image')
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ('category_name',)
    list_filter = ('category_name',)
    ordering = ('category_name',)
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('category_name', 'slug', 'description', 'category_image')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('category_name', 'slug', 'description', 'category_image')
        }),
    )
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