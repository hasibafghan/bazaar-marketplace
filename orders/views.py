from django.shortcuts import render , HttpResponse , redirect
from carts.models import CartItem , Cart
from .models import Order
from .forms import OrderForm
from django.contrib import messages
import datetime


from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings


def paypal_payment(request, order_id):
    if request.method != 'GET':
        return HttpResponse("Invalid request method.", status=400)
    
    order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": str(order.order_total),   # must be string
        "item_name": f"Order {order.id}",
        "invoice": str(order.id),           # unique ID
        "currency_code": "USD",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('order_complete')),
        "cancel_return": request.build_absolute_uri(reverse('checkout')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, "orders/payments.html", {"form": form, "order": order})



# def payments(request):
#     return render(request , 'orders/payments.html')



def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('home')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create a new Order instance
            order = Order()
            order.user = current_user
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address_line_1 = form.cleaned_data['address_line_1']
            order.address_line_2 = form.cleaned_data['address_line_2']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.order_note = form.cleaned_data['order_note']
            order.order_total = grand_total
            order.tax = tax
            order.ip = request.META.get('REMOTE_ADDR')
            order.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # e.g., 20250318
            order_number = current_date + str(order.id)
            order.order_number = order_number
            order.save()

            messages.success(request, "Order placed successfully ✅")

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }

            return render(request, 'orders/payments.html', context)


        else:
            messages.error(request, "Form is not valid ❌")
            return redirect('checkout')
