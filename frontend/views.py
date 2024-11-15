from .models import About
from mixes.models import Mix
from blogs.models import Blog
from .forms import ContactForm
from remixes.models import Remix
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
