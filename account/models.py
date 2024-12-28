from django.db import models
from mixes.models import Mix
from remixes.models import Remix
from products.models import Product
from playlists.models import Playlist
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Extend the base User model to include relationships for likes and history.
    """
    liked_mixes = models.ManyToManyField('Mix', related_name='liked_by', blank=True)
    liked_remixes = models.ManyToManyField('Remix', related_name='Remix', blank=True)
    liked_products = models.ManyToManyField('Product', related_name='liked_by', blank=True)
    liked_playlists = models.ManyToManyField('Playlist', related_name='liked_by', blank=True)

    listened_mixes = models.ManyToManyField('Mix', through='MixHistory', related_name='listened_by', blank=True)
    purchased_products = models.ManyToManyField('Product', through='Purchase', related_name='purchased_by', blank=True)
    listened_premixes = models.ManyToManyField('Remix', through='RemixHistory', related_name='listened_by', blank=True)
    listened_playlists = models.ManyToManyField('Playlist', through='PlaylistHistory', related_name='listened_by', blank=True)


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchased_at = models.DateTimeField(auto_now_add=True)


class MixHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mix = models.ForeignKey(Mix, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)


class PlaylistHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)


class RemixHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remix = models.ForeignKey(Remix, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)
