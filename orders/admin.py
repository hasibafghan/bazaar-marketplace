from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'first_name', 'last_name', 'phone', 'email', 'order_total', 'status', 'is_ordered', 'created_at')
    list_filter = ('status', 'is_ordered', 'created_at')
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email')
    ordering = ('-created_at',)


admin.site.register(Payment)
admin.site.register(Order , OrderAdmin)
admin.site.register(OrderProduct)
