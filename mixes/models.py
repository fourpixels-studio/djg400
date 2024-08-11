from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django_resized import ResizedImageField
from django.templatetags.static import static

class Album(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    square_cover = models.ImageField(
        upload_to="mixes/covers/", blank=True, null=True)
    landscape_cover = models.ImageField(
        upload_to="mixes/covers/", blank=True, null=True)
    meta_thumbnail = ResizedImageField(
        size=[1200, 630],
        crop=['middle', 'center'],
        quality=75,
        upload_to='mixes/thumbnails/',
        blank=True,
        null=True
    )
    square_thumbnail = ResizedImageField(
        size=[1200, 1200],
        crop=['middle', 'center'],
        quality=75,
        upload_to='mixes/thumbnails/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    @property
    def get_url(self):
        return reverse("filtered_albums", kwargs={
            "slug": self.slug,
        })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

        if self.landscape_cover and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.landscape_cover.name}"):
            self.landscape_cover.save(
                f"{self.landscape_cover.name}", self.landscape_cover, save=False)
            super().save(update_fields=['meta_thumbnail'])

        if self.square_cover and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.square_cover.name}"):
            self.square_cover.save(
                f"{self.square_cover.name}", self.square_cover, save=False)
            super().save(update_fields=['meta_thumbnail'])


class Genre(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    square_cover = models.ImageField(
        upload_to="mixes/covers/", blank=True, null=True)
    landscape_cover = models.ImageField(
        upload_to="mixes/covers/", blank=True, null=True)
    meta_thumbnail = ResizedImageField(
        size=[1200, 630],
        crop=['middle', 'center'],
        quality=75,
        upload_to='mixes/thumbnails/',
        blank=True,
        null=True
    )
    square_thumbnail = ResizedImageField(
        size=[1200, 1200],
        crop=['middle', 'center'],
        quality=75,
        upload_to='mixes/thumbnails/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    @property
    def get_url(self):
        return reverse("filtered_genres", kwargs={
            "slug": self.slug,
        })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

        if self.landscape_cover and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.landscape_cover.name}"):
            self.landscape_cover.save(
                f"{self.landscape_cover.name}", self.landscape_cover, save=False)
            super().save(update_fields=['meta_thumbnail'])

        if self.square_cover and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.square_cover.name}"):
            self.square_cover.save(
                f"{self.square_cover.name}", self.square_cover, save=False)
            super().save(update_fields=['meta_thumbnail'])


class Mix(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    square_cover = models.ImageField(
        upload_to="mixes/covers/", blank=True, null=True)
    landscape_cover = models.ImageField(
        upload_to="mixes/covers/", blank=True, null=True)
    meta_thumbnail = ResizedImageField(
        size=[1200, 630],
        crop=['middle', 'center'],
        quality=75,
        upload_to='mixes/thumbnails/',
        blank=True,
        null=True
    )
    square_thumbnail = ResizedImageField(
        size=[1200, 1200],
        crop=['middle', 'center'],
        quality=75,
        upload_to='mixes/thumbnails/',
        blank=True,
        null=True
    )
    episode_number = models.CharField(max_length=3, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True)
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, blank=True, null=True)
    stream_link = models.TextField(blank=True, null=True)
    is_popular = models.BooleanField(default=False, blank=True, null=True)
    featured_artists = models.TextField(blank=True, null=True)
    similar_mixes = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    play_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    download_count = models.PositiveIntegerField(
        default=0, blank=True, null=True)
    reshare_count = models.PositiveIntegerField(
        default=0, blank=True, null=True)
    like_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.pk} {self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def meta_url(self):
        return f"mixes/{self.slug}/"

    @property
    def get_title(self):
        if not self.album:
            return "No title"

        episode_number_str = str(self.episode_number).zfill(2)
        if self.album.slug == "highjacked":
            return f"{self.album} Season {episode_number_str}"

        return f"{self.album} Vol {episode_number_str}"

    @property
    def get_url(self):
        return reverse("mix_detail", kwargs={
            "slug": self.slug,
        })

    @property
    def get_square_cover(self):
        if self.square_cover:
            return self.square_cover.url
        return static('cover.jpg')

    @property
    def get_landscape_cover(self):
        if self.square_cover:
            return self.square_cover.url
        return static('cover.jpg')

    @property
    def get_similar_mixes(self):
        if self.similar_mixes:
            pk_list = self.similar_mixes.split(',')
            return Mix.objects.filter(pk__in=pk_list)
        return Mix.objects.none()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        if self.landscape_cover and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.landscape_cover.name}"):
            self.landscape_cover.save(
                f"{self.landscape_cover.name}", self.landscape_cover, save=False)
            super().save(update_fields=['meta_thumbnail'])

        if self.square_cover and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.square_cover.name}"):
            self.square_cover.save(
                f"{self.square_cover.name}", self.square_cover, save=False)
            super().save(update_fields=['meta_thumbnail'])


class Playlist(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    episode = models.CharField(max_length=3, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True)
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, blank=True, null=True)
    stream_link = models.TextField(blank=True, null=True)
    is_popular = models.BooleanField(default=False, blank=True, null=True)
    featured_artists = models.TextField(blank=True, null=True)
    similar_mixes = models.CharField(max_length=15, blank=True, null=True)
    similar_playlists = models.CharField(max_length=15, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    square_cover = models.ImageField(
        upload_to="mixes/covers/", blank=True, null=True)
    landscape_cover = models.ImageField(
        upload_to="mixes/covers/", blank=True, null=True)
    meta_thumbnail = ResizedImageField(
        size=[1200, 630],
        crop=['middle', 'center'],
        quality=75,
        upload_to='mixes/thumbnails/',
        blank=True,
        null=True
    )
    square_thumbnail = ResizedImageField(
        size=[1200, 1200],
        crop=['middle', 'center'],
        quality=75,
        upload_to='mixes/thumbnails/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


