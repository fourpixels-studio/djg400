from .models import Playlist
from django.shortcuts import render


def playlists(request):
    context = {
        "title_tag": "Playlists",
        "playlists": Playlist.objects.order_by("-release_date"),
    }
    return render(request, 'playlists.html', context)
