from .models import Mix
from blogs.models import Blog
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_results(request):
    search_context = {}
    random_mixes = Mix.objects.order_by('?')[:3]

    if request.GET:
        query = request.GET.get("q")
        if query:
            # Mix model search criteria
            title_results = Q(title__icontains=query)
            albums_description_results = Q(album__description__icontains=query)
            genre_results = Q(genre__name__icontains=query)
            album_name_results = Q(album__name__icontains=query)
            featured_artists_results = Q(featured_artists__icontains=query)
            release_date_results = Q(release_date__year=query)

            mix_results = Mix.objects.filter(
                title_results |
                genre_results |
                album_name_results |
                featured_artists_results |
                albums_description_results
            ).order_by('-release_date').distinct()

            if query.isdigit():
                release_date_results = Q(release_date__year=query)
                mix_results = mix_results.filter(
                    release_date_results).distinct()

            # Blog model search criteria
            blog_title_results = Q(title__icontains=query)
            blog_summary_results = Q(summary__icontains=query)
            blog_content_results = Q(content__icontains=query)
            blog_keywords_results = Q(keywords__icontains=query)
            blog_category_results = Q(category__icontains=query)

            blog_results = Blog.objects.filter(
                blog_title_results |
                blog_summary_results |
                blog_content_results |
                blog_keywords_results |
                blog_category_results
            ).filter(is_published=True).order_by('-published_date').distinct()

            mixes_paginator = Paginator(mix_results, 9)
            page = request.GET.get("page", 1)

            try:
                mixes = mixes_paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                mixes = mixes_paginator.page(1)

            blogs_paginator = Paginator(blog_results, 9)
            page = request.GET.get("page", 1)

            try:
                blogs = blogs_paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                blogs = blogs_paginator.page(1)

            results = {
                "mixes": mixes,
                "blogs": blogs,
            }

        else:
            results = {
                "mixes": [],
                "blogs": [],
            }

        search_context = {
            "results": results,
            "query": query,
            "num_results": {
                "mixes": len(results["mixes"]),
                "blogs": len(results["blogs"]),
            },
            'random_mixes': random_mixes,
        }

    return search_context
