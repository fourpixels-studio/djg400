from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from django_resized import ResizedImageField
from hitcount.models import HitCountMixin, HitCount  # type: ignore
from django.contrib.contenttypes.fields import GenericRelation


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    similar_products = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField(default=0, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    file = models.FileField(blank=True, null=True, upload_to='products/files/')
    image = models.FileField(
        blank=True, null=True,
        upload_to='products/')
    img_sm = ResizedImageField(
        size=[300, 300],
        quality=75,
        upload_to='thumbnails/',
        blank=True,
        null=True
    )
    img_md = ResizedImageField(
        size=[768, 768],
        quality=75,
        upload_to='resized_images/',
        blank=True,
        null=True
    )
    img_lg = ResizedImageField(
        size=[1200, 1200],
        quality=75,
        upload_to='resized_images/',
        blank=True,
        null=True
    )
    meta_thumbnail = ResizedImageField(
        size=[1200, 630],
        crop=['middle', 'center'],
        quality=75,
        upload_to='resized_images/',
        blank=True,
        null=True
    )
    slug = models.SlugField(unique=True, null=True, blank=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field="object_pk", related_query_name="hit_count_generic_relation")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
        if self.image and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.image.name}"):
            self.meta_thumbnail.save(
                f"{self.image.name}", self.image, save=False)
            super(Product, self).save(update_fields=['meta_thumbnail'])
        if self.image and (not self.img_sm or self.img_sm.name != f"{self.image.name}"):
            self.img_sm.save(
                f"{self.image.name}", self.image, save=False)
            super(Product, self).save(update_fields=['img_sm'])
        if self.image and (not self.img_md or self.img_md.name != f"{self.image.name}"):
            self.img_md.save(
                f"{self.image.name}", self.image, save=False)
            super(Product, self).save(update_fields=['img_md'])
        if self.image and (not self.img_sm or self.img_lg.name != f"{self.image.name}"):
            self.img_lg.save(
                f"{self.image.name}", self.image, save=False)
            super(Product, self).save(update_fields=['img_lg'])

    @property
    def get_url(self):
        return reverse("view_product", kwargs={
            "product_category": self.product_category.slug,
            "slug": self.slug,
        })

    @property
    def get_hit_count(self):
        if self.hit_count_generic.exists():
            return self.hit_count_generic.first().hits
        return 0

    @property
    def get_similar_products(self):
        if self.similar_products:
            similar_products_id = self.similar_products.split(',')
            similar_products = Product.objects.filter(
                Q(pk__in=similar_products_id))
            return similar_products
        return None

    def __str__(self):
        return self.name
