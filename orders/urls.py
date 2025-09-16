from django.urls import path , include
from . import views

urlpatterns = [
    path('payment_process/', views.payment_process , name = 'payment_process'),
    # path('payments/', views.payments , name = 'payments'),
    # Paypal URL
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('order-complete/', views.order_complete, name='order_complete'), 
    path('checkout-cancel/', views.checkout_cancel, name='checkout_cancel'),
    
    ]