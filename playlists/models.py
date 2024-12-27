from django.db import models
from django.db.models import Q
from django.urls import reverse
from colorthief import ColorThief
from mixes.models import Genre, Mix
from hitcount.models import HitCount
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.templatetags.static import static
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.contenttypes.fields import GenericRelation


class Playlist(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    square_cover = models.ImageField(upload_to="playlists/covers/", blank=True, null=True)
    landscape_cover = models.ImageField(upload_to="playlists/covers/", blank=True, null=True)
    meta_thumbnail = ResizedImageField(size=[1200, 630], crop=['middle', 'center'], quality=75, upload_to='playlists/thumbnails/', blank=True, null=True)
    square_thumbnail = ResizedImageField(size=[150, 150], crop=['middle', 'center'], quality=75,upload_to='playlists/thumbnails/', blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    is_popular = models.BooleanField(default=False, blank=True, null=True)
    spotify_link = models.TextField(blank=True, null=True)
    youtube_link = models.TextField(blank=True, null=True)
    similar_playlists = models.CharField(max_length=100, blank=True, null=True)
    similar_mixes = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    video_download_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    audio_download_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    reshare_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    like_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    color = models.CharField(max_length=10, null=True, blank=True)
    dark_color = models.CharField(max_length=10, null=True, blank=True)
    light_color = models.CharField(max_length=10, null=True, blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Playlist, self).save(*args, **kwargs)

        # Extract colors from square_cover
        if self.square_cover:
            # Save the image temporarily to access it
            temp_path = default_storage.save(
                self.square_cover.name, ContentFile(self.square_cover.read()))
            temp_file_path = default_storage.path(temp_path)

            try:
                # Extract dominant color and palette
                color_thief = ColorThief(temp_file_path)
                dominant_color = color_thief.get_color(quality=1)
                palette = color_thief.get_palette(color_count=5, quality=1)

                # Convert RGB to Hex for dominant color
                hex_color = "#{:02x}{:02x}{:02x}".format(*dominant_color)

                # Generate lighter and darker shades
                def adjust_brightness(color, factor):
                    return tuple(max(0, min(255, int(c * factor))) for c in color)

                dark_color = adjust_brightness(dominant_color, 0.7)  # Darker
                light_color = adjust_brightness(dominant_color, 1.3)  # Lighter

                # Convert to Hex
                dark_hex = "#{:02x}{:02x}{:02x}".format(*dark_color)
                light_hex = "#{:02x}{:02x}{:02x}".format(*light_color)

                # Update the color fields
                self.color = hex_color
                self.dark_color = dark_hex
                self.light_color = light_hex
                super(Playlist, self).save(update_fields=[
                    'color', 'dark_color', 'light_color'])

            finally:
                # Clean up temporary file
                default_storage.delete(temp_path)

    def __str__(self):
        return f"{self.pk} - {self.title}"

    @property
    def get_similar_playlists(self):
        if not self.similar_playlists:
            return []

        try:
            playlist_ids = [int(pk.strip()) for pk in self.similar_playlists.split(',') if pk.strip().isdigit()]
            return list(Playlist.objects.filter(pk__in=playlist_ids).exclude(pk=self.pk))
        except ValueError:
            return []

    @property
    def get_similar_mixes(self):
        if not self.similar_mixes:
            return []

        try:
            mix_ids = [int(pk.strip()) for pk in self.similar_mixes.split(',') if pk.strip().isdigit()]
            return list(Mix.objects.filter(pk__in=mix_ids))
        except ValueError:
            return []

    @property
    def get_hit_count(self):
        if self.hit_count_generic.exists():
            return self.hit_count_generic.first().hits
        return 0

    @property
    def get_like_count(self):
        if self.like_count > 0:
            return self.like_count
        return 0

    @property
    def get_reshare_count(self):
        if self.reshare_count > 0:
            return self.reshare_count
        return 0

    @property
    def get_url(self):
        return reverse("playlist_detail", kwargs={
            "slug": self.slug,
        })
    
    @property
    def get_thumbnail(self):
        if self.genre:
            return self.genre.get_thumbnail
        return static('playlist_thumbnail.jpg')
