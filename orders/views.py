from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import Order , Payment, OrderProduct
from .forms import OrderForm
from carts.models import CartItem

import datetime, uuid
from core import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt




def payment_process(request, total=0, quantity=0):
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
            # Create order
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

            # Generate unique order number
            current_date = datetime.date.today().strftime("%Y%m%d")
            order_number = current_date + str(order.id)
            order.order_number = order_number
            order.save()

            messages.success(request, "Order placed successfully ✅")


            # # 🔹 PayPal form dictionary
            # # host = request.get_host()

            # paypal_dict = {
            #     "business": settings.PAYPAL_RECEIVER_EMAIL,
            #     "amount": str(order.order_total),   # must be string
            #     "item_name": f"Order {order.order_number}",
            #     "invoice": str(uuid.uuid4()),      # unique ID
            #     "currency_code": "USD",
                
            #     "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            #     "return_url": request.build_absolute_uri(reverse('payment_success')),
            #     "cancel_return": request.build_absolute_uri(reverse('payment_failed')),

                

            #     # 'notify_url': 'https://{}{}'.format(host, reverse("paypal-ipn")),
            #     # 'return_url': 'https://{}{}'.format(host, reverse("payment_success")),
            #     # 'cancel_return' : 'https://{}{}'.format(host, reverse("payment_failed"))
            # }

            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": str(order.order_total),
                "item_name": f"Order {order.order_number}",
                "invoice": str(order.order_number),   # ✅ use order_number
                "currency_code": "USD",
                "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
                "return_url": request.build_absolute_uri(reverse("payment_success")),
                "cancel_return": request.build_absolute_uri(reverse("payment_failed")),
            }
                
            form = PayPalPaymentsForm(initial=paypal_dict)

            return render(request, 'orders/payment_process.html', {
                'form': form,
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            })

        else:
            messages.error(request, "Form is not valid!")
            return redirect('checkout')

    else:
        return HttpResponse("Invalid request method.", status=400)

from paypal.standard.forms import PayPalPaymentsForm




@csrf_exempt
def payment_success(request):

    import json
    try:
        if request.method == "POST" and request.content_type == "application/json":
            data = json.loads(request.body.decode())
            transaction_id = data.get("paymentID")
            payer_id = data.get("payerID")
            order_id = data.get("orderID")
            order_number = data.get("order_number")
            status = "Completed"
            amount = None
        else:
            transaction_id = (
                request.GET.get("tx")
                or request.POST.get("tx")
                or request.GET.get("txn_id")
                or request.POST.get("txn_id")
                or request.GET.get("PayerID")
                or request.POST.get("PayerID")
            )
            status = (
                request.GET.get("st")
                or request.POST.get("payment_status")
                or "Completed"
            )
            amount = (
                request.GET.get("amt")
                or request.POST.get("mc_gross")
            )
            order_number = request.GET.get("order_number") or request.POST.get("order_number")

        # Find the order
        order = None
        if order_number:
            order = Order.objects.filter(order_number=order_number, is_ordered=False).last()
        elif request.user.is_authenticated:
            order = Order.objects.filter(user=request.user, is_ordered=False).last()

        if order:
            payment = Payment.objects.create(
                user=order.user,
                payment_id=transaction_id if transaction_id else f"ORDER-{order.order_number}",
                payment_method="PayPal",
                amount_paid=amount or str(order.order_total),
                status=status,
            )
            order.payment = payment
            order.is_ordered = True
            order.save()
            CartItem.objects.filter(user=order.user).delete()

            # If AJAX, return JSON
            if request.method == "POST" and request.content_type == "application/json":
                return HttpResponse(json.dumps({"status": "success", "transaction_id": payment.payment_id}), content_type="application/json")

            messages.success(request, "Payment successful and order completed 🎉")
            return render(request, "orders/payment_success.html", {
                "order": order,
                "payment": payment
            })
        else:
            if request.method == "POST" and request.content_type == "application/json":
                return HttpResponse(json.dumps({"status": "error", "message": "Order not found"}), content_type="application/json")
            return redirect("home")
    except Exception as e:
        if request.method == "POST" and request.content_type == "application/json":
            return HttpResponse(json.dumps({"status": "error", "message": str(e)}), content_type="application/json")
        messages.error(request, f"Something went wrong: {str(e)}")
        return redirect("home")



def payment_failed(request):
    return render(request, 'orders/payment_cancelled.html')
