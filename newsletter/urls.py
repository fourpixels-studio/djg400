from django.urls import path
from .views import newsletter


urlpatterns = [
    path("", newsletter, name="newsletter"),
]