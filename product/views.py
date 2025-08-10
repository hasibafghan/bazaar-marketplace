from django.shortcuts import render
from .models import Product


def product_list(request):
    products = Product.objects.all().filter(is_available = True)
    products_counter = products.count()

    context = {
        'products' : products,
        'products_counter' : products_counter
    }

    return render (request , 'product_list.html' , context) 
