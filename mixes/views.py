import uuid
from datetime import datetime
from orders.models import Order
from products.models import Product
from django.contrib import messages
from django.http import HttpResponse
from .models import Album, Genre, Mix
from seo_management.models import SEO
from frontend.utils import update_views
from payments.pesapal_payments import PesaPal
from django.shortcuts import render, get_object_or_404, redirect
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


def support_mix(request):
    if request.method == 'POST':
        order_number = str(uuid.uuid4())
        mix_id = request.POST.get('mix_id')
        mix = Mix.objects.get(pk=mix_id)
        email = request.POST.get('email')
        product = Product.objects.get(pk=5)
        last_name = request.POST.get('last_name')
        amount = request.POST.get('supportAmount')
        first_name = request.POST.get('first_name')
        description = f"Payment for '{mix.get_title}' Mix"
        phone_number = request.POST.get('phone_number')
        order = Order(
            paid=False,
            email=email,
            amount=amount,
            product=product,
            status='pending',
            last_name=last_name,
            first_name=first_name,
            description=description,
            phone_number=phone_number,
            order_number=order_number,
        )
        order.save()
        try:
            pesapal = PesaPal()
            payment_response = pesapal.submit_order(order, description)
            if 'redirect_url' in payment_response:
                order.order_tracking_id = payment_response['order_tracking_id']
                order.status = "Awaiting payment confirmation"
                order.save()
                return redirect(payment_response['redirect_url'])
            else:
                messages.error(request, "Missing redirect URL")
                order.status = "Missing redirect URL"
                order.save()
                return redirect('payment_failed', order_number)
        except KeyError as e:
            messages.error(request, f"Payment initiation failed: {str(e)}")
            order.status = str(e)
            order.save()
            return redirect('payment_failed', order_number)
    return HttpResponse("Invalid request method", status=400)
