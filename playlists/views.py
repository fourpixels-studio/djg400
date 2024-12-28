from .models import Playlist
from mixes.models import Genre
from django.shortcuts import render
from seo_management.models import SEO
from frontend.utils import update_views


def playlists(request):
    seo = SEO.objects.get(pk=9)
    context = {
        "title_tag": seo.title_tag,
        "genres": Genre.objects.all(),
        "meta_keywords": seo.meta_keywords,
        "meta_thumbnail": seo.get_thumbnail,
        "meta_description": seo.meta_description,
        "playlists": Playlist.objects.order_by("-release_date"),
    }
    return render(request, 'playlists.html', context)


def playlist_detail(request, slug):
    playlist = Playlist.objects.get(slug=slug)
    context = {
        "playlist": playlist,
        "meta_thumbnail": playlist.get_thumbnail,
        "title_tag": f"Playlist | {playlist.title} Hits",
        "meta_description": f"Immerse yourself in {playlist.title}, a playlist by DJ G400 featuring the best of {playlist.genre.name}. Available on Spotify and YouTube, download your favorite tracks and videos.",
        "meta_keywords": f"DJ G400 playlist, {playlist.genre.name} playlist, Spotify playlist, YouTube playlist, curated {playlist.genre.name} music, DJ G400 Spotify, DJ G400 YouTube, music downloads, trending playlists",
    }
    update_views(request, playlist)
    return render(request, 'playlist_detail.html', context)
