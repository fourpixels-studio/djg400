import re
from django.utils.html import strip_tags
from emails.utils import get_email_backend
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def send_newsletter_email(subscriber_email, article):
    base_url = "https://djg400.com"
    content = article.content
    content = re.sub(r'src="/', f'src="{base_url}/', content)
    context = {
        "article": article,
        "content": content,
        "subscriber_email": subscriber_email,
    }
    html_content = render_to_string('email/email_newsletter.html', context)
    text_content = strip_tags(html_content)
    from_email = "djg400@djg400.com"
    email_backend = get_email_backend(from_email)

    email = EmailMultiAlternatives(
        subject=article.subject,
        body=text_content,
        from_email=from_email,
        to=[subscriber_email,],
        connection=email_backend
    )

    try:
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(f"Failed to send email to {subscriber_email}: {e}")


def send_newsletter_welcome_email(subscriber_email):
    context = {"subscriber_email": subscriber_email}
    html_content = render_to_string('email/newsletter_welcome.html', context)
    text_content = strip_tags(html_content)
    from_email = "djg400@djg400.com"
    email_backend = get_email_backend(from_email)

    email = EmailMultiAlternatives(
        subject="Welcome to DJ G400's Newsletter!",
        body=text_content,
        from_email=from_email,
        to=[subscriber_email,],
        connection=email_backend
    )
    try:
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(f"Failed to send email to {subscriber_email}: {e}")
