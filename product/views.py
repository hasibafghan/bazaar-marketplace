from django.shortcuts import render , get_object_or_404 
from .models import Product
from category.models import Category
from carts.models import Cart , CartItem 
from carts.views import _cart_id
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger


def product_list(request):
    products = Product.objects.all().filter(is_available = True).order_by('created_date')
    products_counter = products.count()
    # pagination section
    paginator = Paginator(products , 3)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)

    context = {
        'products' : page_products,
        'products_counter' : products_counter
    }

    return render (request , 'product/product_list.html' , context) 



def products_by_category(request , category_slug):
    category = get_object_or_404(Category , slug = category_slug)
    products = Product.objects.filter(category = category , is_available = True).order_by('created_date')
    
    paginator = Paginator(products , 3)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)

    products_counter = products.count()
    

    context = { 
        'category' : category,
        'products' : page_products,
        'products_counter' : products_counter
    }

    return render (request , 'product/product_list.html' , context) 



def product_detail(request, category_slug, product_slug):
    try:
        category = get_object_or_404(Category, slug=category_slug)
        product = get_object_or_404(Product, category=category, slug=product_slug, is_available=True)
        
        in_cart = CartItem.objects.filter(
          # cart is field in model! and double ( __ ) go filter by cart_id
            cart__cart_id=_cart_id(request),
            product=product
        ).exists()
        
    except Exception as e:
        raise e

    context = {
        'product' : product,
        'in_cart' : in_cart
    }

    return render(request, 'product/product_detail.html', context )


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



