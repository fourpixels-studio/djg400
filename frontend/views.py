from django.shortcuts import render
from django.contrib import messages
from mixes.models import Mix
from .models import About
from seo_management.models import SEO

seo = SEO.objects.first()


def index(request):
    context = {
        'title_tag': seo.title_tag,
        'meta_description': seo.meta_description,
        'meta_keywords': seo.meta_keywords,
        'latest_mix': Mix.objects.latest("release_date"),
    }
    return render(request, 'index.html', context)


def about(request):
    about = About.objects.first()
    context = {
        'title_tag': "About DJ G400",
        'meta_description': about.who_is_djg400_paragraph,
        'meta_keywords': seo.meta_keywords,
        'about': about,
    }
    return render(request, 'about.html', context)
