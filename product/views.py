from django.shortcuts import render , get_object_or_404
from .models import Product
from category.models import Category


def product_list(request):
    products = Product.objects.all().filter(is_available = True)
    products_counter = products.count()

    context = {
        'products' : products,
        'products_counter' : products_counter
    }

    return render (request , 'product/product_list.html' , context) 




def products_by_category(request , category_slug):

    category = get_object_or_404(Category , slug = category_slug)
    products = Product.objects.filter(category = category , is_available = True)
    products_counter = products.count()
    
    context = {
        'category' : category,
        'products' : products,
        'products_counter' : products_counter
    }

    return render (request , 'product/product_list.html' , context) 


def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug, is_available=True)
    
    return render(request, 'product/product_detail.html', {'product': product})


# def products_by_category(request , category_slug):
#     category = None
#     products = None

#     if category_slug != None:
#         category = get_object_or_404(Category , slug = category_slug)
#         products = Product.objects.filter(category = category , is_available = True)
#         products_counter = products.count()
#     else: 
#         products = Product.objects.all().filter(is_available = True)
#         products_counter = products.count()

#     context = {
#         'category' : category,
#         'products' : products,
#         'products_counter' : products_counter
#     }

#     return render (request , 'product/product_list.html' , context) 



