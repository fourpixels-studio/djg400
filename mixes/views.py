from django.shortcuts import render, get_object_or_404
from .models import Album, Genre, Mix
from frontend.utils import update_views
from seo_management.models import SEO
from shop.models import Product


seo = SEO.objects.first()


def mix_list(request):
    context = {
        'title_tag': seo.title_tag,
        'meta_description': seo.meta_description,
        'meta_keywords': seo.meta_keywords,
        'meta_thumbnail': seo.get_thumbnail,
        'mixes': Mix.objects.order_by("-pk"),
        'latest_mix': Mix.objects.latest("release_date"),
        'albums': Album.objects.all(),
        'genres': Genre.objects.all(),
    }
    return render(request, 'mix_list.html', context)


def video_mix_list(request):
    context = {
        'title_tag': "Video Mixes",
        'meta_description': seo.meta_description,
        'meta_keywords': seo.meta_keywords,
        'meta_thumbnail': seo.get_thumbnail,
        'mixes': Mix.objects.order_by("-pk"),
        'latest_mix': Mix.objects.latest("release_date"),
        'albums': Album.objects.all(),
        'genres': Genre.objects.all(),
    }
    return render(request, 'video_mix_list.html', context)


def filtered_albums(request, slug):
    album = get_object_or_404(Album, slug=slug)
    context = {
        'latest_mix': Mix.objects.latest("release_date"),
        'mixes': Mix.objects.filter(album=album).order_by("-pk"),
        'all_mixes': Mix.objects.all(),
        'genres': Genre.objects.all(),
        'albums': Album.objects.all(),
        'title_tag': f'Showing all {album} Mixes',
        'meta_description': f'Showing all {album} mixes from DJ G400.',
        'album': album,
        'cover_image': album.image,
        'meta_keywords': seo.meta_keywords,
    }
    update_views(request, album)
    return render(request, 'filtered_mixes.html', context)


def filtered_genres(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    context = {
        'latest_mix': Mix.objects.latest("release_date"),
        'mixes': Mix.objects.filter(genre=genre).order_by("-pk"),
        'genres': Genre.objects.all(),
        'albums': Album.objects.all(),
        'title_tag': f'Showing all {genre} Mixes',
        'meta_description': f'Showing all {genre} mixes from DJ G400.',
        'genre': genre,
        'cover_image': genre.image,
        'meta_keywords': seo.meta_keywords,
    }
    update_views(request, genre)
    return render(request, 'filtered_mixes.html', context)


def mix_detail(request, slug):
    mix = get_object_or_404(Mix, slug=slug)
    meta_description = f"Volume {mix.episode_number} in the {mix.album.name} series. This mix embodies the spirit of uptown vibes, evoking a world of sophistication, luxury, and refinement in the world of {mix.genre.name} music."
    meta_keywords = f"{mix.album.name}, {mix.genre.name}, {mix.title}, 400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    if mix.meta_thumbnail:
        meta_thumbnail = mix.meta_thumbnail.url
    else:
        meta_thumbnail = None
    context = {
        'mix': mix,
        'title_tag': f"Playing {mix.get_title}",
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'meta_thumbnail': meta_thumbnail,
    }
    update_views(request, mix)
    return render(request, 'mix_detail.html', context)


def video_mix_detail(request, slug):
    mix = get_object_or_404(Mix, slug=slug)
    meta_description = f"Volume {mix.episode_number} in the {mix.album.name} series. This mix embodies the spirit of uptown vibes, evoking a world of sophistication, luxury, and refinement in the world of {mix.genre.name} music."
    meta_keywords = f"{mix.album.name}, {mix.genre.name}, {mix.title}, 400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    if mix.meta_thumbnail:
        meta_thumbnail = mix.meta_thumbnail.url
    else:
        meta_thumbnail = None
    context = {
        'mix': mix,
        'title_tag': f"Playing {mix.get_title}",
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'meta_thumbnail': meta_thumbnail,
        'products': Product.objects.all(),
    }
    update_views(request, mix)
    return render(request, 'video_mix_detail.html', context)
