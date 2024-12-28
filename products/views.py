import uuid
from .models import Product
from orders.models import Order
from django.contrib import messages
from django.http import HttpResponse
from seo_management.models import SEO
from frontend.utils import update_views
from payments.pesapal_payments import PesaPal
from django.shortcuts import render, get_object_or_404, redirect


seo = SEO.objects.get(pk=4)


def view_product(request, product_category, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product,
        'meta_thumbnail': product.meta_thumbnail.url,
        'title_tag': f"Shop | {product.name} - {product.product_category.name}",
        'meta_description': f"Discover {product.name} in the {product.product_category.name} category on DJ G400's Shop. {product.description} available now for just {product.price}. Stay 400 miles above the competition with exclusive DJ G400 products, wallpapers, and remixed tracks.",
        'meta_keywords': f"{product.name}, {product.product_category.name}, DJ G400 shop, exclusive merchandise, wallpapers, remixed tracks, 400 miles above the competition, Arap Trap, 4Hunnid, G400 apparel, trap music gear, urban products, digital downloads, {product.name} on DJ G400 shop, buy {product.name}, DJ G400 store, {product.product_category.name} products",
    }
    update_views(request, product)
    return render(request, 'view_product.html', context)


def buy_product(request):
    if request.method == 'POST':
        order_number = str(uuid.uuid4())
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)
        phone_number = request.POST.get('phone_number')
        description = f"Payment for {product.product_category}: {product.name}"

        order = Order(
            paid=False,
            email=email,
            amount=amount,
            product=product,
            status='pending',
            last_name=last_name,
            first_name=first_name,
            description=description,
            phone_number=phone_number,
            order_number=order_number,
        )
        order.save()
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
