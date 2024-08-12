from django.db import models
from django_resized import ResizedImageField


class SEO(models.Model):
    title_tag = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    thumbnail = ResizedImageField(
        size=[1200, 600],
        crop=['middle', 'center'],
        quality=75,
        upload_to='thumbnails/',
        blank=True,
        null=True
    )

    @property
    def get_thumbnail(self):
        return self.thumbnail.url if self.thumbnail else None

    def __str__(self):
        return f"{self.title_tag} Page {self.pk}"

    class Meta:
        verbose_name = "SEO Tag"
        verbose_name_plural = "SEO Tags"
