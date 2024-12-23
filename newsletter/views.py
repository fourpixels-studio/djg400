from django.utils import timezone
from django.contrib import messages
from .models import Newsletter, NewsletterArticle
from django.shortcuts import render, get_object_or_404, redirect
from .email import send_newsletter_email, send_newsletter_welcome_email
from .forms import NewsletterForm, UnsubscribeForm, NewsletterArticleForm



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
                send_newsletter_welcome_email(email)
                newsletter_form.save()
                return render(request, 'subscribe_newsletter.html', {
                    'newsletter_form': NewsletterForm(),
                    'success': True,
                })
        else:
            if 'captcha' in newsletter_form.errors:
                messages.error(request, "Please complete the captcha.")
            else:
                for field, errors in newsletter_form.errors.items():
                    for error in errors:
                        messages.error(request, error)
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


def send_newsletter_article(request):
    if request.method == 'POST':
        newletter_article_form = NewsletterArticleForm(request.POST or None, request.FILES or None)
        if newletter_article_form.is_valid():
            newletter_article_form.save()
            article = newletter_article_form.save(commit=False)
            article.save()
            selected_emails = request.POST.getlist('selected_emails')
            num_emails = len(selected_emails)
            if num_emails > 0:
                for subscriber_email in selected_emails:
                    send_newsletter_email(subscriber_email, article)
                article.is_sent = True
                article.num_emails_sent = num_emails
                article.save()
                messages.success(request, f"Successfuly sent newsletter to {num_emails} emails.")
                return redirect("send_newsletter_article")
            else:
                messages.warning(request, "No emails to send newsletter")
                return redirect("send_newsletter_article")
    else:
        newletter_article_form = NewsletterArticleForm()
    context = {
        "title_tag": "Send Newsletter",
        "newletters_count": Newsletter.objects.count(),
        "newletter_article_form": newletter_article_form,
        "sent_newsletters": NewsletterArticle.objects.order_by("-pk"),
        "newletters": Newsletter.objects.filter(consent=True).order_by("-pk"),
    }
    return render(request, "send_newsletter_article.html", context)
    

def newsletter_detail(request, pk):
    newsletter = get_object_or_404(NewsletterArticle, pk=pk)
    context = {
        'newsletter': newsletter,
        'title_tag': newsletter.subject,
    }
    return render(request, 'newsletter_detail.html', context)
