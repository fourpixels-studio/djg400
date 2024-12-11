from .models import Newsletter
from django.utils import timezone
from django.contrib import messages
from .forms import NewsletterForm, UnsubscribeForm
from django.shortcuts import render, get_object_or_404


def subscribe_newsletter(request):
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            existing_subscription = Newsletter.objects.filter(email=email).first()
            if existing_subscription:
                if not existing_subscription.consent:
                    existing_subscription.consent = True
                    existing_subscription.resubscribed_at = timezone.now()
                    existing_subscription.save()
                    messages.success(request, "You've been resubscribed to our newsletter!")
                else:
                    messages.info(request, "You're already subscribed to our newsletter.")
            else:
                newsletter_form.save()
                messages.success(request, "Successfully subscribed to our newsletter!")
                return render(request, 'newsletter.html', {
                    'newsletter_form': NewsletterForm(),
                    'success': True,
                })
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        newsletter_form = NewsletterForm()

    context = {
        'title_tag': "Newsletter Subscription",
        'newsletter_form': newsletter_form,
    }

    return render(request, 'subscribe_newsletter.html', context)


def unsubscribe_newsletter(request):
    if request.method == 'POST':
        unsubscribe_form = UnsubscribeForm(request.POST)
        if unsubscribe_form.is_valid():
            email = unsubscribe_form.cleaned_data['email']
            try:
                subscription = get_object_or_404(Newsletter, email=email, consent=True)
                subscription.unsubscribed_at = timezone.now()
                subscription.consent = False
                subscription.save()
                return render(request, 'unsubscribe_newsletter.html', {
                    "success": True,
                    "title_tag": "Successfully Unsubscribed",
                    "meta_description": "Unsubscribe from our newsletter to stop receiving monthly updates.",
                })
            except Exception as e:
                messages.error(request, "We don't have a subscription with that email.")
        else:
            if 'captcha' in unsubscribe_form.errors:
                messages.error(request, "Please complete the captcha.")
            else:
                for field, errors in unsubscribe_form.errors.items():
                    for error in errors:
                        messages.error(request, error)
    else:
        unsubscribe_form = UnsubscribeForm()

    context = {
        'unsubscribe_form': unsubscribe_form,
        "meta_description": "Unsubscribe from our newsletter to stop receiving monthly updates.",
    }
    return render(request, 'unsubscribe_newsletter.html', context)
