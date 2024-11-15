import math
from django.db import models
from bs4 import BeautifulSoup
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from hitcount.models import HitCount
from django_resized import ResizedImageField
from django.contrib.contenttypes.fields import GenericRelation


class Blog(models.Model):
    title = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(
        upload_to="blog_images/", blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    meta_thumbnail = ResizedImageField(
        size=[1200, 600], quality=75, upload_to='thumbnails/', blank=True, null=True)
    published_date = models.DateTimeField(
        default=timezone.now, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    read_time = models.IntegerField(blank=True, null=True, editable=False)

    def calculate_read_time(self):
        if self.content:
            plain_text = BeautifulSoup(self.content, "html.parser").get_text()
            word_count = len(plain_text.split())
            read_time = math.ceil(word_count / 200)
            return read_time
        return 0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.read_time = self.calculate_read_time()
        super(Blog, self).save(*args, **kwargs)
        if self.cover_image and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.cover_image.name}"):
            self.meta_thumbnail.save(
                f"{self.cover_image.name}", self.cover_image, save=False)
            super(Blog, self).save(update_fields=['meta_thumbnail'])

    @property
    def get_thumbnail(self):
        return self.meta_thumbnail.url if self.meta_thumbnail else None

    def __str__(self):
        return self.title

    @property
    def get_url(self):
        return reverse("blog_detail", kwargs={
            "slug": self.slug,
        })

    @property
    def get_hit_count(self):
        if self.hit_count_generic.exists():
            return self.hit_count_generic.first().hits
        return 0

    @property
    def get_related_blogs(self):
        if self.category:
            articles = Blog.objects.filter(
                category=self.category, is_published=True).exclude(pk=self.pk)
            return articles
        return None
