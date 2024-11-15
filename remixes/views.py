from .models import Remix
from seo_management.models import SEO
from frontend.utils import update_views
from django.shortcuts import render, get_object_or_404


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
    meta_keywords = f"{remix.genre}, {remix.artist}, {seo.meta_keywords}"
    meta_description = f"Listen to {remix.title} featuring {remix.artist}"
    title_tag = f"{remix.title} featuring {remix.artist}"
    context = {
        'remix': remix,
        'title_tag': title_tag,
        'meta_keywords': meta_keywords,
        'meta_description': meta_description,
        'meta_thumbnail': remix.meta_thumbnail.url,
    }
    update_views(request, remix)
    return render(request, 'remix_detail.html', context)
