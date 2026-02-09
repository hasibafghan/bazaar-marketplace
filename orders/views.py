from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, Payment, OrderProduct
from .forms import OrderForm
from carts.models import CartItem
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json, traceback
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@login_required
def payment_process(request):
    """
    Show checkout form and calculate totals
    But DON'T create order until payment is successful
    """
    current_user = request.user

    # Get cart items
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        messages.error(request, "Your cart is empty!")
        return redirect('cart')

    # Calculate totals
    total = 0
    quantity = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store form data in session instead of creating order
            order_data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'address_line_1': form.cleaned_data['address_line_1'],
                'address_line_2': form.cleaned_data['address_line_2'],
                'country': form.cleaned_data['country'],
                'state': form.cleaned_data['state'],
                'city': form.cleaned_data['city'],
                'order_note': form.cleaned_data['order_note'],
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'cart_items_count': cart_count,
            }
            
            # Save to session
            request.session['pending_order'] = order_data
            request.session['cart_items'] = [
                {
                    'product_id': item.product.id,
                    'quantity': item.quantity,
                    'price': float(item.product.price),
                    'variations': list(item.variations.values_list('id', flat=True)) if hasattr(item, 'variations') else []
                }
                for item in cart_items
            ]
            
            # Generate a temporary order number for reference (not saved to DB yet)
            temp_order_number = datetime.date.today().strftime("%Y%m%d") + "TEMP"
            
            messages.info(request, "Please complete your payment")
            
            # Render payment page with form data (but no order in DB yet)
            return render(request, 'orders/payment_process.html', {
                'form_data': order_data,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'temp_order_number': temp_order_number,
            })
        else:
            messages.error(request, "Form is not valid!")
            return redirect('checkout')
    else:
        # GET request - show empty form
        return HttpResponse("Invalid request method.", status=400)


@csrf_exempt
@login_required
def payment_success(request):
    """
    Handle successful payment and ONLY NOW create the order
    """
    try:
        # POST (AJAX from the client after capture)
        if request.method == "POST":
            # Parse payment data
            try:
                data = json.loads(request.body)
            except:
                data = request.POST.dict()

            # Get payment details from PayPal
            transaction_id = data.get("paymentID") or data.get("payment_id") or data.get("txn_id")
            payer_id = data.get("payerID") or data.get("payer_id")
            status = data.get("status", "Completed")
            
            # Check if we have pending order data in session
            if 'pending_order' not in request.session:
                return JsonResponse({
                    "status": "error", 
                    "message": "No pending order found. Please start checkout again."
                }, status=400)
            
            order_data = request.session['pending_order']
            cart_items_data = request.session.get('cart_items', [])
            
            # Verify cart still has items
            current_cart_items = CartItem.objects.filter(user=request.user)
            if current_cart_items.count() == 0:
                return JsonResponse({
                    "status": "error", 
                    "message": "Your cart is empty. Please add items and try again."
                }, status=400)
            
            # 1. CREATE THE ORDER (only now, after payment)
            order = Order()
            order.user = request.user
            order.first_name = order_data['first_name']
            order.last_name = order_data['last_name']
            order.phone = order_data['phone']
            order.email = order_data['email']
            order.address_line_1 = order_data['address_line_1']
            order.address_line_2 = order_data['address_line_2']
            order.country = order_data['country']
            order.state = order_data['state']
            order.city = order_data['city']
            order.order_note = order_data['order_note']
            order.order_total = order_data['grand_total']
            order.tax = order_data['tax']
            order.ip = request.META.get('REMOTE_ADDR')
            order.save()

            # Generate unique order number
            current_date = datetime.date.today().strftime("%Y%m%d")
            order_number = current_date + str(order.id)
            order.order_number = order_number
            order.save()
            
            # 2. CREATE PAYMENT RECORD
            payment = Payment.objects.create(
                user = request.user,
                payment_id = transaction_id or f"PAY-{order_number}",
                payment_method = "PayPal",
                amount_paid = data.get('amount') or str(order.order_total),
                status = status
            )
            
            # 3. UPDATE ORDER WITH PAYMENT
            order.payment = payment
            order.is_ordered = True
            order.status = "Completed"
            order.save()
            
            # 4. CREATE OrderProduct ENTRIES
            cart_items = CartItem.objects.filter(user=request.user)
            for cart_item in cart_items:
                order_product = OrderProduct()
                order_product.order = order
                order_product.payment = payment
                order_product.user = request.user
                order_product.product = cart_item.product
                order_product.quantity = cart_item.quantity
                order_product.product_price = cart_item.product.price
                order_product.ordered = True
                order_product.save()
                
                # Handle variations if any
                if hasattr(cart_item, 'variations') and cart_item.variations.exists():
                    order_product.variations.set(cart_item.variations.all())
                
                # Reduce product stock
                product = cart_item.product
                product.stock -= cart_item.quantity
                if product.stock < 0:
                    product.stock = 0
                product.save()
            
            # 5. SEND CONFIRMATION EMAIL
            try:
                mail_subject = 'Thank you for your order!'
                message = render_to_string('orders/order_received_email.html', {
                    'user': request.user,
                    'order': order,
                })
                to_email = order.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
            except Exception as e:
                print(f"Email sending failed: {e}")
                # Don't fail the whole process if email fails
            
            # 6. CLEAR CART
            cart_items.delete()
            
            # 7. CLEAR SESSION DATA
            if 'pending_order' in request.session:
                del request.session['pending_order']
            if 'cart_items' in request.session:
                del request.session['cart_items']
            
            # Return success with order number
            return JsonResponse({
                "status": "success", 
                "transaction_id": payment.payment_id,
                "order_number": order.order_number,
                "redirect_url": reverse('payment_success') + f"?order={order.order_number}"
            })

        # GET => show success page
        order_number = request.GET.get("order")
        if order_number:
            # Verify this order belongs to the current user
            order = get_object_or_404(Order, order_number=order_number, user=request.user)
            context = {
                "order": order, 
                "payment": order.payment
            }
            return render(request, "orders/payment_success.html", context)
        else:
            # No order specified, redirect to home
            messages.info(request, "Order completed successfully!")
            return redirect('home')

    except Exception as e:
        traceback.print_exc()
        # Clear session on error
        if 'pending_order' in request.session:
            del request.session['pending_order']
        if 'cart_items' in request.session:
            del request.session['cart_items']
        
        return JsonResponse({
            "status": "error", 
            "message": str(e)
        }, status=500)


@login_required
def payment_failed(request):
    """
    Handle failed/cancelled payments
    """
    # Clear pending order from session
    if 'pending_order' in request.session:
        del request.session['pending_order']
    if 'cart_items' in request.session:
        del request.session['cart_items']
    
    messages.error(request, "Payment was cancelled or failed. Please try again.")
    return render(request, 'orders/payment_cancelled.html')


@login_required
def clear_pending_order(request):
    """
    Clear any pending order data from session
    Useful if user abandons checkout
    """
    if 'pending_order' in request.session:
        del request.session['pending_order']
    if 'cart_items' in request.session:
        del request.session['cart_items']
    
    return JsonResponse({"status": "cleared"})


