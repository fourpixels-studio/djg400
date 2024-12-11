from django.urls import path
from .views import playlists


urlpatterns = [
    path("", playlists, name="playlists"),
]
