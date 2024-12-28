from django.shortcuts import render
from products.models import Product
from seo_management.models import SEO


def shop(request):
    seo = SEO.objects.get(pk=4)
    context = {
        'title_tag': seo.title_tag,
        'products': Product.objects.all(),
        'meta_keywords': seo.meta_keywords,
        'meta_thumbnail': seo.get_thumbnail,
        'meta_description': seo.meta_description,
    }
    return render(request, 'shop.html', context)
