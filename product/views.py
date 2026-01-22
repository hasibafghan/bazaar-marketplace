from django.shortcuts import render , get_object_or_404 , redirect 
from .models import Product , ProductGallery
from category.models import Category
from carts.models import CartItem 
from carts.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import ReviewRating
from .forms import ReviewForm
from orders.models import OrderProduct
from django.db.models import Min, Max



def product_list(request):
    # Get all available products
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    
    # Get min and max prices - force min to 0
    price_range = products.aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )
    min_price = 0  # Always start from 0
    max_price = int(price_range['max_price'] or 1000)
    
    # Handle price filtering
    min_filter = request.GET.get('min_price')
    max_filter = request.GET.get('max_price')
    
    if min_filter:
        products = products.filter(price__gte=min_filter)
    if max_filter:
        products = products.filter(price__lte=max_filter)
    
    # Generate price options starting from 0
    price_options = []
    current = 0
    while current <= max_price:
        price_options.append(current)
        if current < 50:
            current += 10
        elif current < 200:
            current += 50
        else:
            current += 100
    
    # Pagination
    products_counter = products.count()
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)

    context = {
        'products': page_products,
        'products_counter': products_counter,
        'min_price': min_price,
        'max_price': max_price,
        'price_options': price_options,
        'selected_min': min_filter,
        'selected_max': max_filter,
    }
    
    return render(request, 'product/product_list.html', context)



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


from accounts.models import UserProfile

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
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user = request.user , product = product).exists()
        except orderproduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # show reviews
    reviews = ReviewRating.objects.filter(product_id = product.id  , status = True)

    # # get user profile image
    # userprofile = None
    # userprofile = UserProfile.objects.get_or_create(user_id = request.user.id) 

    # get product gallery images
    product_gallery = ProductGallery.objects.filter(product_id = product.id)

    context = {
        'product' : product,
        'in_cart' : in_cart,
        'orderproduct' : orderproduct,
        'reviews' : reviews,
        'product_gallery' : product_gallery,
        # 'userprofile': userprofile,
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