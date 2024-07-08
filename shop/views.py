from django.shortcuts import render

def shop(request):
    title_tag = "Shop | Dazzling outfits"
    meta_description = "Shop the latest collection of urban, modern, and fresh merchandise inspired by Arap Trap's unique style."
    meta_keywords = "400 miles above the competition, arap trap, 4hunnid, g400, highjacked, hood love, trap, hip hop, rnb, rap, quality mixes, hd mixes, 1080p mixes"
    context = {
        'title_tag': title_tag,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    }
    return render(request, 'shop.html', context)
