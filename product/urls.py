from django.urls import path
from . import views

urlpatterns = [
    path('product_list/' , views.product_list , name = 'product_list'),
    path('<slug:category_slug>' , views.products_by_category , name = 'products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/' , views.product_detail , name = 'product_detail'),
    path('search/' , views.search_product , name = 'search_product'),

]
