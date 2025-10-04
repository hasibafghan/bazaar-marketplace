from django.urls import path , include
from . import views

urlpatterns = [
    path('payment_process/', views.payment_process , name = 'payment_process'),
    # Paypal URL
    path('payment_success/', views.payment_success, name='payment_success'), 
    path('payment_failed/', views.payment_failed, name='payment_failed'),
    
    ]