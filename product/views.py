from django.shortcuts import render , get_object_or_404 , redirect 
from .models import Product
from category.models import Category
from carts.models import Cart , CartItem 
from carts.views import _cart_id
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from .models import ReviewRating
from .forms import ReviewForm
from orders.models import OrderProduct



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



def search_product(request):
    query = request.GET.get('search', '').strip()
    # categories = Category.objects.all()

    if query:
        products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-id')
    else:
        products = Product.objects.all().order_by('-id')

    # Pagination for search results too
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)

    return render(request, 'product/product_list.html', {
        'products': products_page,
        'products_counter': products.count(),
        # 'categories': categories,
    })




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

    # check if the user has purchased the product for leaving a review
    try:
        orderproduct = OrderProduct.objects.filter(user = request.user , product = product).exists()
    except orderproduct.DoesNotExist:
        orderproduct = None

    context = {
        'product' : product,
        'in_cart' : in_cart,
        'orderproduct' : orderproduct,
    }

    return render(request, 'product/product_detail.html', context )


def submit_review(request , product_id):
    if request.method == 'POST':
        url = request.META.get('HTTP_REFERER')
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id , product__id = product_id)
            forms = ReviewForm(request.POST , instance = reviews)
            forms.save()
            messages.success(request , 'Thank you! Your review has been updated.')
            return redirect(url)
        
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request , 'Thank you! Your review has been submitted.')
                return redirect(url)