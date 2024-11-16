from products.models import Product
from django.shortcuts import render


def cart(request, slug):
    context = {
        "title_tag": "Cart",
        'product': Product.objects.get(slug=slug),
    }
    return render(request, "cart.html", context)


def checkout(request, slug):
    context = {
        "title_tag": "Checkout",
        'product': Product.objects.get(slug=slug),
    }
    return render(request, "checkout.html", context)
