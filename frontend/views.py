from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# from .models import Mix, Album

def index(request):
    title_tag = "400 Miles Above The Competition"
    meta_descriprion = "Home of epic playlists, banging mixes, dazzling outfits, and unforgettable DJ services. We're your one-stop party shop for epic playlists, banging mixes, dazzling outfits, and unforgettable DJ services."
    meta_keywords = "400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    # mixes = Mix.objects.all()
    context = {
        'title_tag': title_tag,
        # 'mixes': mixes,
    }
    return render(request, 'index.html', context)


def albums(request):
    title_tag = "Albums"
    meta_descriprion = "All ablums"
    meta_keywords = "albums, 400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    # albums = Album.objects.all()
    context = {
        'title_tag': title_tag,
        # 'albums': albums,
    }
    return render(request, 'albums.html', context)

def event(request):
    title_tag = "Events"
    meta_descriprion = "All ablums"
    meta_keywords = "events, 400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    context = {
        'title_tag': title_tag,
    }
    return render(request, 'event.html', context)

def blog_list(request):
    title_tag = "Blogs"
    meta_descriprion = "All blogs"
    meta_keywords = "blogs, 400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    context = {
        'title_tag': title_tag,
    }
    return render(request, 'blog-list.html', context)

def contact(request):
    title_tag = "contact"
    meta_descriprion = "contact"
    meta_keywords = "contact, 400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    context = {
        'title_tag': title_tag,
    }
    return render(request, 'contact.html', context)

def elements(request):
    title_tag = "elements"
    meta_descriprion = "elements"
    meta_keywords = "elements, 400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    context = {
        'title_tag': title_tag,
    }
    return render(request, 'elements.html', context)

def login(request):
    title_tag = "login"
    meta_descriprion = "login"
    meta_keywords = "login, 400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    context = {
        'title_tag': title_tag,
    }
    return render(request, 'login.html', context)

def login(request):
    title_tag = "login"
    meta_descriprion = "login"
    meta_keywords = "login, 400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    context = {
        'title_tag': title_tag,
    }
    return render(request, 'login.html', context)


# def mix_detail(request, slug):
#     mix = get_object_or_404(Mix, slug=slug)
#     context = {
#         'title_tag': mix.title,
#         'mix': mix,
#     }
#     return render(request, 'mix-detail.html', context)
