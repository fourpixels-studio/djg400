from datetime import datetime
from products.models import Product
from seo_management.models import SEO
from .models import Album, Genre, Mix
from frontend.utils import update_views
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .get_items import get_albums, get_all_mixes, get_genres, get_latest_mix

seo = SEO.objects.first()


def mix_list(request):
    paginator = Paginator(get_all_mixes(), 9)
    page = request.GET.get("page", 1)

    try:
        mixes = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        mixes = paginator.page(1)

    context = {
        'mixes': mixes,
        'genres': get_genres(),
        'albums': get_albums(),
        'title_tag': seo.title_tag,
        'latest_mix': get_latest_mix(),
        'meta_keywords': seo.meta_keywords,
        'meta_thumbnail': seo.get_thumbnail,
        'meta_description': seo.meta_description,
    }
    return render(request, 'mix_list.html', context)


def filtered_albums(request, slug):
    album = get_object_or_404(Album, slug=slug)
    context = {
        'album': album,
        'albums': get_albums(),
        'genres': get_genres(),
        'cover_image': album.image,
        'all_mixes': get_all_mixes(),
        'latest_mix': get_latest_mix(),
        'meta_keywords': seo.meta_keywords,
        'title_tag': f'Showing all {album} Mixes',
        'mixes': Mix.objects.filter(album=album).order_by("-pk"),
        'meta_description': f'Showing all {album} mixes from DJ G400.',
    }
    update_views(request, album)
    return render(request, 'mix_list.html', context)


def filtered_genres(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    context = {
        'genre': genre,
        'genres': get_genres(),
        'albums': get_albums(),
        'mixes': get_all_mixes(),
        'cover_image': genre.image,
        'active_genre': genre.slug,
        'latest_mix': get_latest_mix(),
        'meta_keywords': seo.meta_keywords,
        'title_tag': f'Showing all {genre} Mixes',
        'meta_description': f'Showing all {genre} mixes from DJ G400.',
    }
    update_views(request, genre)
    return render(request, 'mix_list.html', context)


def mix_detail(request, slug):
    mix = get_object_or_404(Mix, slug=slug)
    context = {
        'mix': mix,
        'products': Product.objects.all(),
        'meta_thumbnail': mix.get_landscape_thumbnail,
        'title_tag': f"{mix.get_title} - {mix.genre.name} Mix | Stream & Download",
        'meta_description': f"Listen to '{mix.title}' by DJ G400, a {mix.genre.name} mix from the album '{mix.album.name}' featuring {mix.get_featured_artists}. Stream or download this popular mix with {mix.play_count} plays and {mix.download_count} downloads. Available now on DJ G400's platform.",
        'meta_keywords': f"{mix.title}, {mix.genre.name}, {mix.album.name}, DJ G400 mix, DJ G400 music, {mix.title} mix, featured artists {mix.get_featured_artists}, popular mixes, hip hop mixes, trap mixes, RnB mixes, stream {mix.title}, download {mix.title}, urban music, DJ G400 playlist, exclusive mixes, top mixes {datetime.now().year}",
    }
    update_views(request, mix)
    return render(request, "mix_detail.html", context)
