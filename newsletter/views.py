from django.shortcuts import render
from .models import Newsletter
from .forms import NewsletterForm

def newsletter(request):
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if not Newsletter.objects.filter(email=email).exists():
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
