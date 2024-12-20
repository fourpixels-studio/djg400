from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from hitcount.models import HitCount
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.contrib.contenttypes.fields import GenericRelation


class Event(models.Model):
    name = models.CharField(max_length=255)
    poster = models.ImageField(
        upload_to='event_posters/', null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ticket_link = models.TextField(blank=True, null=True)
    poster = models.ImageField(
        upload_to="event_posters/", blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    meta_thumbnail = ResizedImageField(
        size=[1200, 600], quality=75, upload_to='thumbnails/', blank=True, null=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    slug = models.SlugField(unique=True, null=True, blank=True)
    portrait_thumbnail = ResizedImageField(size=[540, 675], crop=[
                                           'middle', 'center'], quality=75, upload_to='events/thumbnails/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)
        if self.poster and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.poster.name}"):
            self.meta_thumbnail.save(
                f"{self.poster.name}", self.poster, save=False)
            super(Event, self).save(update_fields=['meta_thumbnail'])
        if self.poster and (not self.portrait_thumbnail or self.portrait_thumbnail.name != f"{self.poster.name}"):
            self.portrait_thumbnail.save(
                f"{self.poster.name}", self.poster, save=False)
            super(Event, self).save(update_fields=['portrait_thumbnail'])

    @property
    def get_thumbnail(self):
        return self.meta_thumbnail.url if self.meta_thumbnail else None

    def __str__(self):
        return self.name

    @property
    def get_url(self):
        return reverse("event_detail", kwargs={
            "slug": self.slug,
        })

    @property
    def get_hit_count(self):
        if self.hit_count_generic.exists():
            return self.hit_count_generic.first().hits
        return 0

    @property
    def is_upcoming(self):
        if self.date >= timezone.now().date():
            return True
        return False

    @property
    def get_share_link(self):
        current_site = settings.PUBLIC_URL
        blog_url = self.get_url
        return f"{current_site}{blog_url}"


class EventMedia(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_media/', null=True, blank=True)
    youtube_link = models.TextField(null=True, blank=True)
    youtube_embed_link = models.TextField(null=True, blank=True)
    video_file = models.FileField(
        null=True, blank=True, upload_to="event_media/")

    def __str__(self):
        if self.image:
            file = str("IMAGE")
        elif self.youtube_link:
            file = str("YOUTUBE LINK")
        elif self.youtube_embed_link:
            file = str("YOUTUBE EMBED LINK")
        elif self.video_file:
            file = str("VIDEO FILE")
        else:
            file = "NO FILE"
        return f"{file} --- {self.name} --- {self.event.pk}"
