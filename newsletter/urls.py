from django.urls import path
from .views import subscribe_newsletter, unsubscribe_newsletter, send_newsletter_article, newsletter_detail


urlpatterns = [
    path("sent/<int:pk>/", newsletter_detail, name="newsletter_detail"),
    path("subscribe/", subscribe_newsletter, name="subscribe_newsletter"),
    path("send/", send_newsletter_article, name="send_newsletter_article"),
    path("unsubscribe/", unsubscribe_newsletter, name="unsubscribe_newsletter"),
]
