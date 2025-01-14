from mixes.models import Mix
from blogs.models import Blog
from django.db.models import Q
from events.models import Event
from remixes.models import Remix
from products.models import Product
from playlists.models import Playlist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_results(request):
    search_context = {}
    random_mixes = Mix.objects.order_by('?')[:6]

    if request.GET:
        query = request.GET.get("q")
        if query:
            # Remix model search criteria
            remix_title_results = Q(title__icontains=query)
            remix_artist_results = Q(artist__icontains=query)
            remix_genre_results = Q(genre__name__icontains=query)

            remixes_results = Remix.objects.filter(
                remix_title_results |
                remix_artist_results |
                remix_genre_results
            ).order_by('-release_date').distinct()

            remixes_paginator = Paginator(remixes_results, 12)
            page = request.GET.get("page", 1)

            try:
                remixes = remixes_paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                remixes = remixes_paginator.page(1)

            # Event model search criteria
            event_name_results = Q(name__icontains=query)
            event_location_results = Q(location__icontains=query)
            event_venue_results = Q(venue__icontains=query)
            event_description_results = Q(description__icontains=query)
            event_keywords_results = Q(keywords__icontains=query)
            event_date_results = Q(date__year=query)

            events_results = Event.objects.filter(
                event_name_results |
                event_location_results |
                event_venue_results |
                event_description_results |
                event_keywords_results
            ).order_by('-date').distinct()

            if query.isdigit():
                event_date_results = Q(date__year=query)
                events_results = events_results.filter(
                    event_date_results).distinct()

            events_paginator = Paginator(events_results, 12)
            page = request.GET.get("page", 1)

            try:
                events = events_paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                events = events_paginator.page(1)

            # Mix model search criteria
            mix_title_results = Q(title__icontains=query)
            mix_albums_description_results = Q(
                album__description__icontains=query)
            mix_genre_results = Q(genre__name__icontains=query)
            mix_album_name_results = Q(album__name__icontains=query)
            mix_featured_artists_results = Q(featured_artists__icontains=query)
            mix_release_date_results = Q(release_date__year=query)

            mix_results = Mix.objects.filter(
                mix_title_results |
                mix_genre_results |
                mix_album_name_results |
                mix_featured_artists_results |
                mix_albums_description_results
            ).order_by('-release_date').distinct()

            if query.isdigit():
                mix_release_date_results = Q(release_date__year=query)
                mix_results = mix_results.filter(
                    mix_release_date_results).distinct()

            mixes_paginator = Paginator(mix_results, 9)
            page = request.GET.get("page", 1)

            try:
                mixes = mixes_paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                mixes = mixes_paginator.page(1)

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

            blogs_paginator = Paginator(blog_results, 9)
            page = request.GET.get("page", 1)

            try:
                blogs = blogs_paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                blogs = blogs_paginator.page(1)

            # Playlist model search criteria
            playlist_title_results = Q(title__icontains=query)
            playlist_genre_results = Q(genre__name__icontains=query)

            playlists_results = Playlist.objects.filter(
                playlist_title_results |
                playlist_genre_results
            ).order_by('-release_date').distinct()

            playlists_paginator = Paginator(playlists_results, 9)
            page = request.GET.get("page", 1)

            try:
                playlists = playlists_paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                playlists = playlists_paginator.page(1)

            # Product model search criteria
            product_category_results = Q(
                product_category__name__icontains=query)
            prodyct_description_results = Q(description__icontains=query)

            products_results = Product.objects.filter(
                product_category_results |
                prodyct_description_results
            ).order_by('-pk').distinct()

            products_paginator = Paginator(products_results, 9)
            page = request.GET.get("page", 1)

            try:
                products = products_paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                products = products_paginator.page(1)

            results = {
                "mixes": mixes,
                "blogs": blogs,
                "events": events,
                "remixes": remixes,
                "products": products,
                "playlists": playlists,
            }

        else:
            results = {
                "mixes": [],
                "blogs": [],
                "events": [],
                "remixes": [],
                "products": [],
                "playlists": [],
            }

        search_context = {
            "results": results,
            "query": query,
            "num_results": {
                "mixes": len(results["mixes"]),
                "blogs": len(results["blogs"]),
                "events": len(results["events"]),
                "remixes": len(results["remixes"]),
                "products": len(results["products"]),
                "playlists": len(results["playlists"]),
            },
            'random_mixes': random_mixes,
        }

    return search_context
