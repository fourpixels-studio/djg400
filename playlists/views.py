from .models import Playlist
from django.shortcuts import render


def playlists(request):
    context = {
        "title_tag": "Playlists",
        "playlists": Playlist.objects.all(),
    }
    return render(request, 'playlists.html', context)
