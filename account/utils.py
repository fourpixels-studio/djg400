from .models import User
from mixes.models import Mix
from products.models import Product
from django.http import JsonResponse
from playlists.models import Playlist
from django.shortcuts import render, get_object_or_404
from .models import Purchase, MixHistory, PlaylistHistory
from django.contrib.auth.decorators import login_required


@login_required
def like_mix(request, mix_id):
    """
    Allows a user to like or unlike a mix.
    """
    mix = get_object_or_404(Mix, id=mix_id)
    if mix in request.user.liked_mixes.all():
        request.user.liked_mixes.remove(mix)
        liked = False
    else:
        request.user.liked_mixes.add(mix)
        liked = True
    return JsonResponse({'liked': liked})


@login_required
def like_playlist(request, playlist_id):
    """
    Allows a user to like or unlike a playlist.
    """
    playlist = get_object_or_404(Playlist, id=playlist_id)
    if playlist in request.user.liked_playlists.all():
        request.user.liked_playlists.remove(playlist)
        liked = False
    else:
        request.user.liked_playlists.add(playlist)
        liked = True
    return JsonResponse({'liked': liked})


@login_required
def like_product(request, product_id):
    """
    Allows a user to like or unlike a product.
    """
    product = get_object_or_404(Product, id=product_id)
    if product in request.user.liked_products.all():
        request.user.liked_products.remove(product)
        liked = False
    else:
        request.user.liked_products.add(product)
        liked = True
    return JsonResponse({'liked': liked})


@login_required
def purchase_product(request, product_id):
    """
    Allows a user to purchase a product.
    """
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    Purchase.objects.create(user=request.user, product=product, quantity=quantity)
    return JsonResponse({'message': 'Purchase successful'})


@login_required
def listen_mix(request, mix_id):
    """
    Records that a user has listened to a mix.
    """
    mix = get_object_or_404(Mix, id=mix_id)
    MixHistory.objects.create(user=request.user, mix=mix)
    return JsonResponse({'message': 'Mix listened'})


@login_required
def listen_playlist(request, playlist_id):
    """
    Records that a user has listened to a playlist.
    """
    playlist = get_object_or_404(Playlist, id=playlist_id)
    PlaylistHistory.objects.create(user=request.user, playlist=playlist)
    return JsonResponse({'message': 'Playlist listened'})


@login_required
def purchase_history(request):
    """
    View for displaying the user's purchase history.
    """
    purchases = Purchase.objects.filter(user=request.user).select_related('product')
    return render(request, 'purchase_history.html', {'purchases': purchases})


@login_required
def listening_history(request):
    """
    View for displaying the user's listening history.
    """
    mix_history = MixHistory.objects.filter(user=request.user).select_related('mix')
    playlist_history = PlaylistHistory.objects.filter(user=request.user).select_related('playlist')
    return render(request, 'listening_history.html', {
        'mix_history': mix_history,
        'playlist_history': playlist_history,
    })
