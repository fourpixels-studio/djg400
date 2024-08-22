from .models import Mix
from django.db.models import Q


def search_results(request):
    search_context = {}
    random_mixes = Mix.objects.order_by('?')[:10]
    if request.GET:
        query = request.GET.get("q")
        if query:
            title_results = Q(title__icontains=query)
            albums_description_results = Q(album__description__icontains=query)
            genre_results = Q(genre__name__icontains=query)
            album_name_results = Q(album__name__icontains=query)
            featured_artists_results = Q(featured_artists__icontains=query)
            release_date_results = Q(release_date__year=query)

            results = Mix.objects.filter(
                title_results |
                genre_results |
                album_name_results |
                featured_artists_results |
                albums_description_results
            ).order_by('-release_date').distinct()

            if query.isdigit():
                release_date_results = Q(release_date__year=query)
                results = results.filter(release_date_results).distinct()
        else:
            results = []

        search_context = {
            "results": results,
            "query": query,
            "num_results": results.count(),
            'random_mixes': random_mixes,
        }

    return search_context
