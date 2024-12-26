from django.urls import path
from .views import remixes_list, remix_detail, support_remix

urlpatterns = [
    path("", remixes_list, name="remixes_list"),
    path("support/", support_remix, name="support_remix"),
    path("remix/<slug:slug>/", remix_detail, name="remix_detail"),
]
