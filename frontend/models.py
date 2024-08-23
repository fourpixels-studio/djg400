from django.db import models


class About(models.Model):
    hero_image = models.FileField(
        upload_to="about/", blank=True, null=True)
    hero_tagline = models.CharField(max_length=80, blank=True, null=True)
    hero_paragraph = models.TextField(blank=True, null=True)

    wide_image = models.FileField(
        upload_to="about/", blank=True, null=True)

    arap_trap_2 = models.FileField(
        upload_to="about/", blank=True, null=True)

    who_is_djg400_title = models.CharField(
        max_length=80, blank=True, null=True)
    who_is_djg400_paragraph = models.TextField(blank=True, null=True)
    who_is_djg400_image = models.FileField(
        upload_to="about/", blank=True, null=True)

    musical_style_title = models.CharField(
        max_length=80, blank=True, null=True)
    musical_style_paragraph = models.TextField(blank=True, null=True)
    musical_style_image = models.FileField(
        upload_to="about/", blank=True, null=True)

    performances_title = models.CharField(
        max_length=80, blank=True, null=True)
    performances_paragraph = models.TextField(blank=True, null=True)
    performances_image = models.FileField(
        upload_to="about/", blank=True, null=True)

    visuals_title = models.CharField(
        max_length=80, blank=True, null=True)
    visuals_paragraph = models.TextField(blank=True, null=True)
    visuals_image = models.FileField(
        upload_to="about/", blank=True, null=True)

    discography_title = models.CharField(
        max_length=80, blank=True, null=True)
    discography_paragraph = models.TextField(blank=True, null=True)
    discography_image = models.FileField(
        upload_to="about/", blank=True, null=True)

    contact_title = models.CharField(
        max_length=80, blank=True, null=True)
    contact_paragraph = models.TextField(blank=True, null=True)

    arap_trap_footer = models.FileField(
        upload_to="about/", blank=True, null=True)

    def __str__(self):
        return str("About")
