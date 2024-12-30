import json
from mixes.models import Mix
from products.models import Product
from django.http import JsonResponse
from playlists.models import Playlist
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import MixHistory, PlaylistHistory, Remix
from django.contrib.auth.decorators import login_required


# Like a mix
@login_required
def like_mix(request, mix_id):
    mix = get_object_or_404(Mix, id=mix_id)
    customer = request.user.customer
    if mix in customer.liked_mixes.all():
        customer.liked_mixes.remove(mix)
        liked = False
    else:
        customer.liked_mixes.add(mix)
        liked = True
    return JsonResponse({'liked': liked})


# Like a playlist
@login_required
def like_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    customer = request.user.customer
    if playlist in customer.liked_playlists.all():
        customer.liked_playlists.remove(playlist)
        liked = False
    else:
        customer.liked_playlists.add(playlist)
        liked = True
    return JsonResponse({'liked': liked})


# Like a remix
@login_required
def like_remix(request, remix_id):
    remix = get_object_or_404(Remix, id=remix_id)
    customer = request.user.customer
    if remix in customer.liked_remixes.all():
        customer.liked_remixes.remove(remix)
        liked = False
    else:
        customer.liked_remixes.add(remix)
        liked = True
    return JsonResponse({'liked': liked})


# Like a product
@login_required
def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer
    if product in customer.liked_products.all():
        customer.liked_products.remove(product)
        liked = False
    else:
        customer.liked_products.add(product)
        liked = True
    return JsonResponse({'liked': liked})


# Add to Mix history
@login_required
def add_mix_history(request, mix_id):
    mix = get_object_or_404(Mix, id=mix_id)
    customer = request.user.customer
    MixHistory.objects.get_or_create(customer=customer, mix=mix)
    return JsonResponse({'status': 'success'})


# Add to Playlist history
@login_required
def add_playlist_history(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    customer = request.user.customer
    PlaylistHistory.objects.get_or_create(customer=customer, playlist=playlist)
    return JsonResponse({'status': 'success'})


@method_decorator(csrf_exempt, name="dispatch")
def update_mix_play(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mix_id = data.get('mix_id')
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'message': 'User not authenticated'}, status=403)
        try:
            mix = Mix.objects.get(id=mix_id)
            customer = user.customer
            mix_history, created = MixHistory.objects.get_or_create(customer=customer, mix=mix)
            if not created:
                mix_history.increment_play_count()
            return JsonResponse({'message': 'Play count updated successfully'})
        except Mix.DoesNotExist:
            return JsonResponse({'message': 'Mix not found'}, status=404)
    return JsonResponse({'message': 'Invalid request method'}, status=405)
