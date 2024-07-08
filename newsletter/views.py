from .models import Newsletter
from .forms import NewsletterForm
from django.contrib import messages
from django.shortcuts import render, redirect


def newsletter(request):
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data.get('email')
            if Newsletter.objects.filter(email=email).exists():
                pass
            else:
                newsletter_form.save()
            return render(request, 'newsletter.html', {
                'newsletter_form': NewsletterForm(),
                'success': True,
            })
    else:
        newsletter_form = NewsletterForm()

    context = {
        'title_tag': "Newsletter Subscription",
        'newsletter_form': newsletter_form,
    }

    return render(request, 'newsletter.html', context)