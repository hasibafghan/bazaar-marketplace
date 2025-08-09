from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'slug', 'price', 'stock', 'is_available', 'created_date', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ('is_available', 'category')
    search_fields = ('product_name', 'description')
    list_editable = ('price', 'stock', 'is_available')
    list_per_page = 20

    
admin.site.register(Product, ProductAdmin)