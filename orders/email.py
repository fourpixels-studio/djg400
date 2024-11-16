from django.conf import settings
from django.utils.html import strip_tags
from emails.utils import get_email_backend
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_order_confirmation_email(order):
    context = {
        "order": order,
        "order_url": f"{settings.SITE_DOMAIN}orders/order/{order.order_number}/"
    }
    html_content = render_to_string('email/order_email.html', context)
    text_content = strip_tags(html_content)
    from_email = "orders@djg400.com"
    email_backend = get_email_backend(from_email)

    email = EmailMultiAlternatives(
        subject=f'Confirmation for Order #{order.get_order_number} - DJ G400',
        body=text_content,
        from_email=from_email,
        to=[order.get_email,],
        connection=email_backend
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
