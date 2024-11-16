import os
from django.core.mail import get_connection


def get_email_backend(from_email):
    """
    This function returns a custom email backend configuration
    based on the `from_email` provided.
    """
    if from_email == 'orders@djg400.com':
        return get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='mail.djg400.com',
            port=465,
            username='orders@djg400.com',
            password=os.environ.get('ORDERS_EMAIL_PASSWORD'),
            use_tls=False,
            use_ssl=True
        )
    elif from_email == 'music@djg400.com':
        return get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='mail.djg400.com',
            port=465,
            username='music@djg400.com',
            password=os.environ.get('MUSIC_EMAIL_PASSWORD'),
            use_tls=False,
            use_ssl=True
        )
    elif from_email == 'newsletter@djg400.com':
        return get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='mail.djg400.com',
            port=465,
            username='newsletter@djg400.com',
            password=os.environ.get('NEWSLETTER_EMAIL_PASSWORD'),
            use_tls=False,
            use_ssl=True
        )
    elif from_email == 'bookings@djg400.com':
        return get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='mail.djg400.com',
            port=465,
            username='bookings@djg400.com',
            password=os.environ.get('BOOKINGS_EMAIL_PASSWORD'),
            use_tls=False,
            use_ssl=True
        )
    elif from_email == 'info@djg400.com':
        return get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='mail.djg400.com',
            port=465,
            username='info@djg400.com',
            password=os.environ.get('INFO_EMAIL_PASSWORD'),
            use_tls=False,
            use_ssl=True
        )
    elif from_email == 'localhost':
        return get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='localhost',
            port=1025,
            username='localhost',
            password="",
            use_tls=False,
            use_ssl=True
        )
    else:
        raise ValueError(f"Unknown from_email: {from_email}")
