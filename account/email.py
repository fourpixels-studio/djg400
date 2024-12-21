from django.utils.html import strip_tags
from emails.utils import get_email_backend
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_user_verification_email(user):
    context = {
        "user": user,
    }
    html_content = render_to_string('email/account_email.html', context)
    text_content = strip_tags(html_content)
    from_email = "djg400@djg400.com"
    email_backend = get_email_backend(from_email)

    email = EmailMultiAlternatives(
        subject=f'Welcome To DJ G400',
        body=text_content,
        from_email=from_email,
        to=[user.email,],
        connection=email_backend
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
