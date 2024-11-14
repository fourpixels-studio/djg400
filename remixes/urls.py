from django.urls import path
from .views import remixes_list, remix_detail

urlpatterns = [
    path("", remixes_list, name="remixes_list"),
    path("remix/<slug:slug>/", remix_detail, name="remix_detail"),
]
