from django.db import models
from django.urls import reverse
from colorthief import ColorThief
from hitcount.models import HitCount
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.contenttypes.fields import GenericRelation


class RemixGenre(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    square_cover = models.ImageField(upload_to="remixes/covers/", blank=True, null=True)
    landscape_cover = models.ImageField(upload_to="remixes/covers/", blank=True, null=True)
    meta_thumbnail = ResizedImageField(size=[1200, 630], crop=['middle', 'center'], quality=75, upload_to='remixes/thumbnails/', blank=True, null=True)
    square_thumbnail = ResizedImageField( size=[1200, 1200], crop=['middle', 'center'], quality=75, upload_to='remixes/thumbnails/', blank=True, null=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.name

    @property
    def get_url(self):
        return reverse("remix_detail", kwargs={
            "slug": self.slug,
        })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.landscape_cover and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.landscape_cover.name}"):
            self.landscape_cover.save(f"{self.landscape_cover.name}", self.landscape_cover, save=False)
            super().save(update_fields=['meta_thumbnail'])
        if self.square_cover and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.square_cover.name}"):
            self.square_cover.save(f"{self.square_cover.name}", self.square_cover, save=False)
            super().save(update_fields=['meta_thumbnail'])


class Remix(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    artist = models.TextField(blank=True, null=True)
    square_cover = models.ImageField(upload_to="remixes/covers/", blank=True, null=True)
    landscape_cover = models.ImageField(upload_to="remixes/covers/", blank=True, null=True)
    meta_thumbnail = ResizedImageField(size=[1200, 630], crop=['middle', 'center'], quality=75, upload_to='remixes/thumbnails/', blank=True, null=True)
    square_thumbnail = ResizedImageField(size=[150, 150], crop=['middle', 'center'], quality=75, upload_to='remixes/thumbnails/', blank=True, null=True)
    genre = models.ForeignKey(RemixGenre, on_delete=models.CASCADE, blank=True, null=True)
    is_popular = models.BooleanField(default=False, blank=True, null=True)
    video_download_link = models.URLField(blank=True, null=True)
    audio_download_link = models.URLField(blank=True, null=True)
    similar_remixes = models.CharField(max_length=100, blank=True, null=True)
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

        super(Remix, self).save(*args, **kwargs)

        # Extract colors from square_cover
        if self.square_cover:
            # Save the image temporarily to access it
            temp_path = default_storage.save(self.square_cover.name, ContentFile(self.square_cover.read()))
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
                super(Remix, self).save(update_fields=['color', 'dark_color', 'light_color'])

            finally:
                # Clean up temporary file
                default_storage.delete(temp_path)

    def __str__(self):
        return self.title

    @property
    def is_video_link(self):
        if self.video_download_link:
            return True
        return False

    @property
    def is_audio_link(self):
        if self.audio_download_link:
            return True
        return False

    @property
    def get_similar_remixes(self):
        remixes = []
        if self.genre:
            remixes = Remix.objects.filter(genre=self.genre)
        return remixes

    @property
    def get_hit_count(self):
        if self.hit_count_generic.exists():
            return self.hit_count_generic.first().hits
        return 0

    @property
    def get_download_count(self):
        count = 0
        if self.video_download_count:
            count += self.video_download_count
        if self.audio_download_count:
            count += self.audio_download_count
        return count

    @property
    def get_url(self):
        return reverse("remix_detail", kwargs={
            "slug": self.slug,
        })
