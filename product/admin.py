from django.contrib import admin
from .models import Product , Variation , ReviewRating , ProductGallery
import admin_thumbnails
@admin_thumbnails.thumbnail('image',)
class ProductGalleryinline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'slug', 'price', 'stock', 'is_available', 'created_date', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ('is_available', 'category')
    search_fields = ('product_name', 'description')
    list_editable = ('price', 'stock', 'is_available')
    list_per_page = 20
    inlines = [ProductGalleryinline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product' , 'variation_category' , 'variation_value' , 'is_active', 'created_date' )
    list_editable = ( 'is_active', )
    list_filter = ('product' , 'variation_category' , 'variation_value' ,)
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery )