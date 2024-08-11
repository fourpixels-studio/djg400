from django.shortcuts import render

def mix_list(request):
    title_tag = "Mixes, Playlists and More."
    meta_descriprion = "Epic playlists, banging video and audio mixes from DJ G400"
    meta_keywords = "400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    context = {
        'title_tag': title_tag,
        'meta_descriprion': meta_descriprion,
        'meta_keywords': meta_keywords,
    }
    return render(request, 'mix_list.html', context)



def filtered_albums(request, slug):
    album = get_object_or_404(Album, slug=slug)
    context = {
        'latest_mix': Mix.objects.latest("release_date"),
        'mixes': Mix.objects.filter(album=album),
        'all_mixes': Mix.objects.all(),
        'genres': Genre.objects.all(),
        'albums': Album.objects.all(),
        'title_tag': f'Showing all {album} Mixes',
    }
    return render(request, 'filtered_mixes.html', context)


def filtered_genres(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    context = {
        'latest_mix': Mix.objects.latest("release_date"),
        'mixes': Mix.objects.filter(genre=genre),
        'genres': Genre.objects.all(),
        'albums': Album.objects.all(),
        'title_tag': f'Showing all {genre} Mixes',
    }
    return render(request, 'filtered_mixes.html', context)


