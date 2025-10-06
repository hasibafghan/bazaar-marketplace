from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import Order, Payment , OrderProduct
from .forms import OrderForm
from carts.models import CartItem
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json, traceback



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

            # Only pass order/cart context, no PayPal form
            return render(request, 'orders/payment_process.html', {
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
    


@csrf_exempt
def payment_success(request):
    try:
        # POST (AJAX from the client after capture)
        if request.method == "POST":
            # Robustly detect JSON content
            content_type = request.META.get('CONTENT_TYPE', '')
            body = request.body.decode() if request.body else ''
            data = {}

            if 'application/json' in content_type or body.startswith('{'):
                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                    return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
            else:
                # support form-encoded fallback
                data = request.POST.dict()

            transaction_id = data.get("paymentID") or data.get("payment_id") or data.get("txn_id")
            payer_id = data.get("payerID") or data.get("payer_id")
            order_id = data.get("orderID") or data.get("order_id")
            order_number = data.get("order_number") or request.GET.get('order')
            status = "Completed"

            # find the order (best effort)
            order = None
            if order_number:
                order = Order.objects.filter(order_number=order_number, is_ordered=False).last()
            elif request.user.is_authenticated:
                order = Order.objects.filter(user=request.user, is_ordered=False).last()

            if not order:
                return JsonResponse({"status": "error", "message": "Order not found"}, status=404)

            # create Payment and attach
            payment = Payment.objects.create(
                user = order.user,
                payment_id = transaction_id or f"ORDER-{order.order_number}",
                payment_method = "PayPal",
                amount_paid = data.get('amount') or str(order.order_total),
                status = status
            )
            order.payment = payment
            order.is_ordered = True
            order.save()

            # clear cart
            CartItem.objects.filter(user=order.user).delete()

            return JsonResponse({"status": "success", "transaction_id": payment.payment_id})

        # GET => show success page
        order_number = request.GET.get("order")
        order = None
        payment = None
        if order_number:
            order = Order.objects.filter(order_number=order_number).select_related('payment').last()
            if order and order.payment:
                payment = order.payment
        context = {"order": order, "payment": payment}
        return render(request, "orders/payment_success.html", context)

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    

def payment_failed(request):
    return render(request, 'orders/payment_cancelled.html')

