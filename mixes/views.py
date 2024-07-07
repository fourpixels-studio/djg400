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

