from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.urls import reverse
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation


class Type(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    type = models.ForeignKey(
        Type, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.IntegerField(default=0, blank=True, null=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    img_small = models.ImageField(null=True, blank=True, upload_to="shop/")
    img_md = models.ImageField(null=True, blank=True, upload_to="shop/")
    img_lg = models.ImageField(null=True, blank=True, upload_to="shop/")

    meta_thumbnail = ResizedImageField(
        size=[1200, 630],
        crop=['middle', 'center'],
        quality=75,
        upload_to='thumbnails/',
        blank=True,
        null=True
    )
    slug = models.SlugField(unique=True, null=True, blank=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field="object_pk", related_query_name="hit_count_generic_relation")

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.img_lg and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.img_lg.name}"):
            self.meta_thumbnail.save(
                f"{self.img_lg.name}", self.img_lg, save=False)
            super(Product, self).save(update_fields=['meta_thumbnail'])

    @property
    def get_url(self):
        return reverse("view_product", kwargs={
            "slug": self.slug
        })

    @property
    def get_hit_count(self):
        if self.hit_count_generic.exists():
            return self.hit_count_generic.first().hits
        return 0

    def __str__(self):
        return self.name
