from .models import About
from blogs.models import Blog
from .forms import ContactForm
from events.models import Event
from remixes.models import Remix
from mixes.models import Mix, Genre
from django.contrib import messages
from seo_management.models import SEO
from django.shortcuts import render, redirect


seo = SEO.objects.first()


def index(request):
    context = {
        'title_tag': seo.title_tag,
        'blogs': Blog.objects.all()[:3],
        'meta_keywords': seo.meta_keywords,
        'remixes': Remix.objects.order_by("-pk"),
        'meta_description': seo.meta_description,
        'events': Event.objects.order_by("-date")[:3],
        'latest_mix': Mix.objects.latest("release_date"),
    }
    return render(request, 'index.html', context)


def about(request):
    about = About.objects.first()
    contact_form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Your message has been received. I will get back to you soon.')
            return redirect('about')
        else:
            if contact_form.errors:
                for field, errors in contact_form.errors.items():
                    for error in errors:
                        messages.error(request, error)
    context = {
        'about': about,
        'title_tag': "About DJ G400",
        'contact_form': contact_form,
        'meta_keywords': seo.meta_keywords,
        'meta_description': about.who_is_djg400_paragraph,
    }
    return render(request, 'about.html', context)


def search(request):
    meta_description = f'Showing "{request.GET.get("q")}" results in DJ G400. {seo.meta_description}'
    context = {
        'genres': Genre.objects.all(),
        'meta_keywords': seo.meta_keywords,
        'meta_description': meta_description,
        "title_tag": f'"{request.GET.get("q")}" results',
    }
    return render(request, 'mix_list.html', context)
