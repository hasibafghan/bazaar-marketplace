# orders/signals.py
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from .models import Payment, Order

@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED:
        try:
            # Get order_number back from invoice field
            order_number = ipn.invoice  

            # Find the order
            order = Order.objects.filter(order_number=order_number, is_ordered=False).last()
            if order:
                payment = Payment.objects.create(
                    user=order.user,
                    payment_id=ipn.txn_id,            # ✅ transaction ID from PayPal
                    payment_method="PayPal",
                    amount_paid=str(ipn.mc_gross),   # PayPal sends this as Decimal
                    status=ipn.payment_status,
                )
                order.payment = payment
                order.is_ordered = True
                order.save()

                print(f"✅ Payment saved for Order {order_number} with TXN {ipn.txn_id}")
        except Exception as e:
            print("❌ Error saving PayPal payment:", e)
