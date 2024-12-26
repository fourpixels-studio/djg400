import uuid
from .models import Remix
from orders.models import Order
from products.models import Product
from django.contrib import messages
from django.http import HttpResponse
from seo_management.models import SEO
from frontend.utils import update_views
from payments.pesapal_payments import PesaPal
from django.shortcuts import render, get_object_or_404, redirect


seo = SEO.objects.get(pk=3)


def remixes_list(request):
    context = {
        'title_tag': seo.title_tag,
        'meta_keywords': seo.meta_keywords,
        'meta_thumbnail': seo.get_thumbnail,
        'remixes': Remix.objects.order_by("-pk"),
        'meta_description': seo.meta_description,
    }
    return render(request, 'remixes_list.html', context)


def remix_detail(request, slug):
    remix = get_object_or_404(Remix, slug=slug)
    context = {
        'remix': remix,
        'meta_thumbnail': remix.meta_thumbnail.url,
        'title_tag': f"{remix.title} featuring {remix.artist}",
        'meta_keywords': f"{remix.genre}, {remix.artist}, {seo.meta_keywords}",
        'meta_description': f"Listen to {remix.title} featuring {remix.artist}",
    }
    update_views(request, remix)
    return render(request, 'remix_detail.html', context)


def support_remix(request):
    if request.method == 'POST':
        order_number = str(uuid.uuid4())
        email = request.POST.get('email')
        product = Product.objects.get(pk=4)
        remix_id = request.POST.get('remix_id')
        remix = Remix.objects.get(pk=remix_id)
        last_name = request.POST.get('last_name')
        amount = request.POST.get('supportAmount')
        first_name = request.POST.get('first_name')
        description = f"Payment for '{remix.title}'"
        phone_number = request.POST.get('phone_number')
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
