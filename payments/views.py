from orders.models import Order
from django.shortcuts import render


def payment_failed(request, order_number):
    order = Order.objects.get(order_number=order_number)
    context = {
        "order": order,
        "title_tag": f"Failed! Order No. #{order.get_order_number}",
    }
    return render(request, 'payment_failed.html', context)
