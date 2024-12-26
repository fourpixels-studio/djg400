from .models import Order
from django.contrib import messages
from .receipt import generate_receipt
from django.shortcuts import redirect, render
from django.core.files.base import ContentFile
from .email import send_order_confirmation_email


def view_order(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
        if order.paid == True and order.is_email_sent == False:
            pdf_output = generate_receipt(order)
            order.receipt.save(f'order_{order.get_order_number}.pdf', ContentFile(pdf_output), save=True)
            order.save()
            send_order_confirmation_email(order)
            order.is_email_sent = True
            order.save()
            messages.success(request, "Thank you for your order! A confirmation email with your order details and receipt will be sent to you shortly.")
        context = {
            "order": order,
            "title_tag": f"Order No. #{order.get_order_number} Confirmed!",
        }
        return render(request, 'view_order.html', context)
    except Order.DoesNotExist:
        return redirect('shop')
