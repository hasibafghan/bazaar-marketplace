from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0
    if 'admin' in request.path:  # Skip admin pages
        return {}
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        cart_count = sum(item.quantity for item in cart_items)  # Total quantity, not just rows
    except Cart.DoesNotExist:
        cart_count = 0
    return dict(cart_count=cart_count)
