from django.urls import path , include
from . import views

urlpatterns = [
    path('place_order/', views.place_order , name = 'place_order'),
    # path('payments/', views.payments , name = 'payments'),
    # Paypal URL
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('order-complete/', views.order_complete, name='order_complete'), 
    path('checkout-cancel/', views.checkout_cancel, name='checkout_cancel'),
    
    ]