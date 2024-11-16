import uuid
from .models import Product
from orders.models import Order
from django.contrib import messages
from django.http import HttpResponse
from payments.pesapal_payments import PesaPal
from django.shortcuts import render, get_object_or_404, redirect


def view_product(request, product_category, slug):
    product = get_object_or_404(Product, slug=slug)
    meta_keywords = "400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    context = {
        'product': product,
        'title_tag': product.name,
        'meta_keywords': meta_keywords,
        'meta_description': product.description,
    }
    return render(request, 'view_product.html', context)


def buy_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        order_number = str(uuid.uuid4())
        description = f"Payment for '{product.name}' {product.product_category}"

        order = Order(
            product=product,
            paid=False,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            amount=amount,
            order_number=order_number,
            status='pending',
            description=description,
        )
        order.save()
        messages.success(request, f"Succesfully received order and payment!")
        try:
            pesapal = PesaPal()
            payment_response = pesapal.submit_order(order, description)
            if 'redirect_url' in payment_response:
                order.order_tracking_id = payment_response['order_tracking_id']
                order.status = "Awaiting payment confirmation"
                order.save()
                return redirect(payment_response['redirect_url'])
            else:
                messages.error(request, "Missing redirect URL")
                order.status = "Missing redirect URL"
                order.save()
                return redirect('payment_failed', order_number)
        except KeyError as e:
            messages.error(request, f"Payment initiation failed: {str(e)}")
            order.status = str(e)
            order.save()
            return redirect('payment_failed', order_number)
    return HttpResponse("Invalid request method", status=400)
