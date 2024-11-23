from products.models import Product
from .models import Album, Genre, Mix
from seo_management.models import SEO
from frontend.utils import update_views
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

seo = SEO.objects.first()


def mix_list(request):
    all_mixes = Mix.objects.order_by("-pk")
    paginator = Paginator(all_mixes, 9)
    page = request.GET.get("page", 1)

    try:
        mixes = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        mixes = paginator.page(1)

    context = {
        'mixes': mixes,
        'title_tag': seo.title_tag,
        'albums': Album.objects.all(),
        'genres': Genre.objects.all(),
        'meta_keywords': seo.meta_keywords,
        'meta_thumbnail': seo.get_thumbnail,
        'meta_description': seo.meta_description,
        'latest_mix': Mix.objects.latest("release_date"),
    }
    return render(request, 'mix_list.html', context)


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
        'meta_keywords': seo.meta_keywords,
    }
    update_views(request, album)
    return render(request, 'mix_list.html', context)


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
        'active_genre': genre.slug,
        'meta_keywords': seo.meta_keywords,
    }
    update_views(request, genre)
    return render(request, 'mix_list.html', context)


def audio_mix_detail(request, slug):
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
    return render(request, 'audio_mix_detail.html', context)


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
    return render(request, 'audio_mix_detail.html', context)
    
    
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


def search_mixes(request):
    meta_description = f'Showing "{request.GET.get("q")}" results in DJ G400. {seo.meta_description}'
    context = {
        'genres': Genre.objects.all(),
        'meta_keywords': seo.meta_keywords,
        'meta_description': meta_description,
        "title_tag": f'"{request.GET.get("q")}" results',
    }
    return render(request, 'mix_list.html', context)
