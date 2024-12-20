from django.shortcuts import render
from django.utils.timezone import now
from .models import Event, EventMedia
from frontend.utils import update_views
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def event_detail(request, slug):
    event = Event.objects.get(slug=slug)
    keywords = [
        keyword.strip()
        for keyword in event.keywords.split(',')
        if keyword.strip()
    ]
    all_gallery_items = EventMedia.objects.filter(event=event)
    images = []
    youtube_embed_links = []
    video_files = []
    snippets = []
    for item in all_gallery_items:
        if item.image:
            images.append(item.image.url)
        if item.youtube_embed_link:
            youtube_embed_links.append(item.youtube_embed_link)
        if item.video_file:
            if item.video_file and item.youtube_link:
                snippets.append(item)
            else:
                video_files.append(item.video_file)
    context = {
        "event": event,
        "images": images,
        "keywords": keywords,
        "meta_keywords": event.keywords,
        "title_tag": f"Events | {event.name}",
        "meta_description": event.description,
        "meta_thumbnail": event.portrait_thumbnail.url,
        "upcoming_events": Event.objects.filter(date__gte=now().date()).order_by('date').exclude(pk=event.pk),
    }
    update_views(request, event)
    return render(request, "event_detail.html", context)


def event_list(request):
    all_events = Event.objects.order_by("-date")
    paginator = Paginator(all_events, 4)
    page = request.GET.get("page", 1)

    try:
        events = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        events = paginator.page(1)

    context = {
        "events": events,
        "title_tag": "Events",
        "meta_keywords": "Events, DJ G400 Events",
        "meta_description": "Events, DJ G400 Events",
    }
    return render(request, "event_list.html", context)
