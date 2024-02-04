from django.shortcuts import render


def shop(request):
    title_tag = ""
    meta_descriprion = ""
    meta_keywords = ""
    context = {
        'title_tag': title_tag,
    }
    return render(request, 'shop.html', context)
