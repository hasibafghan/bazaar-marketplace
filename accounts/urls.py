from django.urls import path
from . import views

urlpatterns = [
    # authentication
    path('register_user/', views.register_user, name='register_user'), 
    path('login_user/', views.login_user, name='login_user'), 
    path('logout_user/', views.logout_user, name='logout_user'),
    
    # activation link
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
    
    # Forgot Password
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'), 
    path('reset_password/', views.reset_password, name='reset_password'),

    # dashboard
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('', views.dashboard, name='dashboard'), 
    path('my_orders/', views.my_orders, name = 'my_orders'),
    path('edit_profile/' , views.edit_profile , name = 'edit_profile')

    

]
