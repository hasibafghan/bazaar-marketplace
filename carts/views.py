from django.shortcuts import render , redirect, get_object_or_404
from product.models import Product , Variation
from .models import Cart , CartItem


def _cart_id(request):
    cart = request.session.session_key 
    if not cart :
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variations = []
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variations.append(variation)
            except Variation.DoesNotExist:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    # CartItem Section: try to find an existing cart item with the same variations
    cart_items = CartItem.objects.filter(product=product, cart=cart)
    if cart_items.exists():
        new_variation_ids = sorted([v.id for v in product_variations])
        for item in cart_items:
            existing_variation_ids = sorted(list(item.variations.values_list('id', flat=True)))
            if existing_variation_ids == new_variation_ids:
                item.quantity += 1
                item.save()
                break
        else:
            # no matching item found -> create new row
            cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            if product_variations:
                cart_item.variations.add(*product_variations)
            cart_item.save()
    else:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        if product_variations:
            cart_item.variations.add(*product_variations)
        cart_item.save()
    return redirect('cart')



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except Cart.DoesNotExist:
        cart_items = []
        tax = 0
        grand_total = 0

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'carts/cart.html', context)



def remove_cart_quantity(request, product_id , cart_item_id ):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart , id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')



def remove_cart_item(request, product_id , cart_item_id): 
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart  , id=cart_item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  

    # check if cart has no items left
    if not CartItem.objects.filter(cart=cart).exists():
        cart.delete()   # delete the whole cart if empty

    return redirect('cart')
