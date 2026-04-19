from django.contrib import admin
from .models import Product , Variation , ReviewRating , ProductGallery
from parler.admin import TranslatableAdmin
import admin_thumbnails

@admin_thumbnails.thumbnail('image',)
class ProductGalleryinline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(TranslatableAdmin):
    list_display = ('product_name', 'slug', 'price', 'stock', 'is_available', 'created_date', 'modified_date')
    list_filter = ('is_available', 'category')
    search_fields = ('translations__product_name', 'translations__description')
    list_editable = ('price', 'stock', 'is_available')
    list_per_page = 20
    inlines = [ProductGalleryinline]

class VariationAdmin(TranslatableAdmin):
    list_display = ('product', 'variation_category', 'is_active', 'created_date')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'is_active')
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery )