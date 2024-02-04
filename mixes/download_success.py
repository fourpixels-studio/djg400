from django.shortcuts import render, get_object_or_404, redirect
from .models import Mix
def download_success(request, pk):
    mix = get_object_or_404(Mix, pk=pk)
    mix.download_count = mix.download_count + 1
    mix.save()
    context = {
        'title_tag': "Success!",
        'mix': mix,
    }
    return render(request, 'download-success.html', context)