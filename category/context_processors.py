from django.shortcuts import render
from .models import Category



def category_list(request):
    return {
        'categories': Category.objects.all()
    }