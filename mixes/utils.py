from .models import Mix
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def like_mix(request, slug):
    if request.method == "POST":
        mix = get_object_or_404(Mix, slug=slug)
        mix.like_count += 1
        mix.save()
        return JsonResponse({"like_count": mix.like_count})
    return JsonResponse({"error": "Invalid request"}, status=400)


def reshare_mix(request, slug):
    if request.method == "POST":
        mix = get_object_or_404(Mix, slug=slug)
        mix.reshare_count += 1
        mix.save()
        return JsonResponse({"reshare_count": mix.reshare_count})
    return JsonResponse({"error": "Invalid request"}, status=400)
