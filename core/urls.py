from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('category/', include('category.urls')),
    path('accounts/', include('accounts.urls')),
    path('products/', include('product.urls')),
    path('carts/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    
    path('test_paypal/', include('test_paypal.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
