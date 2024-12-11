from django.urls import path
from .views import subscribe_newsletter, unsubscribe_newsletter


urlpatterns = [
    path("subscribe/", subscribe_newsletter, name="subscribe_newsletter"),
    path("unsubscribe/", unsubscribe_newsletter, name="unsubscribe_newsletter"),
]
