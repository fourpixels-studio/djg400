from django.urls import path
from .views import playlists, playlist_detail


urlpatterns = [
    path("", playlists, name="playlists"),
    path("<slug:slug>/", playlist_detail, name="playlist_detail"),
]
