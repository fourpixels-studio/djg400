from django.shortcuts import render, get_object_or_404
from .models import Product


def shop(request):
    title_tag = "Shop | Dazzling outfits"
    meta_description = "Shop the latest collection of urban, modern, and fresh merchandise inspired by Arap Trap's unique style."
    meta_keywords = "400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    context = {
        'title_tag': title_tag,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'products': Product.objects.all(),
        'latest_product': Product.objects.first(),
    }
    return render(request, 'shop.html', context)


def view_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    meta_description = "Shop the latest collection of urban, modern, and fresh merchandise inspired by Arap Trap's unique style."
    meta_keywords = "400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    context = {
        'title_tag': product.name,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'product': product,
    }
    return render(request, 'view_product.html', context)
