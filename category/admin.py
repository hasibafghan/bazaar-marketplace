from django.contrib import admin
from .models import Category
from parler.admin import TranslatableAdmin


# @admin.register(Category)
# class CategoryAdmin(TranslatableAdmin):
#     list_display = ('category_name', 'slug', 'description')
#     search_fields = ('translations__category_name',)
#     ordering = ('translations__category_name',)
#     list_per_page = 20

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('category_name', 'slug', 'description')
    search_fields = ('translations__category_name',)
    ordering = ('translations__category_name',)
    list_per_page = 20
    ordering = ('slug',)
    list_per_page = 20

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.distinct()