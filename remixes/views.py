from .models import Remix
from products.models import Product
from seo_management.models import SEO
from frontend.utils import update_views
from django.shortcuts import render, get_object_or_404


seo = SEO.objects.first()


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
        'title_tag': remix.title,
        'meta_description': remix.title,
        'meta_keywords': remix.artist,
        'meta_thumbnail': remix.meta_thumbnail,
        'products': Product.objects.all(),
    }
    update_views(request, remix)
    return render(request, 'remix_detail.html', context)
