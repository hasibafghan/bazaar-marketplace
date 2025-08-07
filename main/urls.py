from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # or whatever view you have
]