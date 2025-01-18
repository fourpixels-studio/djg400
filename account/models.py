from django.db import models
from mixes.models import Mix
from remixes.models import Remix
from products.models import Product
from playlists.models import Playlist
from django.contrib.auth.models import User
from django_resized import ResizedImageField


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    square_thumbnail = ResizedImageField(size=[150, 150], crop=['middle', 'center'], quality=75, upload_to='profile_pictures/thumbnails/', blank=True, null=True)
    liked_mixes = models.ManyToManyField(Mix, related_name='liked_by', blank=True)
    liked_remixes = models.ManyToManyField(Remix, related_name='Remix', blank=True)
    purchased_products = models.ManyToManyField(Product, related_name='purchased_by', blank=True)
    liked_playlists = models.ManyToManyField(Playlist, related_name='liked_by', blank=True)
    listened_mixes = models.ManyToManyField(Mix, through='MixHistory', related_name='listened_by', blank=True)
    purchased_products = models.ManyToManyField(Product, through='Purchase', related_name='purchased_by', blank=True)
    listened_remixes = models.ManyToManyField(Remix, through='RemixHistory', related_name='listened_by', blank=True)
    listened_playlists = models.ManyToManyField(Playlist, through='PlaylistHistory', related_name='listened_by', blank=True)
    bio = models.CharField(max_length=200, blank=True)
    newsletter_email_notification = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        if self.profile_picture:
            if not self.pk:
                super().save(*args, **kwargs)
            if not self.square_thumbnail or self.square_thumbnail.name != f"profile_pictures/thumbnails/{self.profile_picture.name}":
                self.square_thumbnail.save(f"profile_pictures/thumbnails/{self.profile_picture.name}", self.profile_picture, save=False)
        super().save(*args, **kwargs)


class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.user.get_full_name()} purchased {self.quantity} {self.product.product_category.name} on {self.purchased_at}"


class MixHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    mix = models.ForeignKey(Mix, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)
    num_plays = models.PositiveIntegerField(default=1)

    def increment_play_count(self):
        self.num_plays += 1
        self.save(update_fields=["num_plays"])

    def __str__(self):
        return f"{self.customer.user.get_full_name()} listened to '{self.mix.get_title}' {self.num_plays} times"


class PlaylistHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)
    num_plays = models.PositiveIntegerField(default=1)

    def increment_play_count(self):
        self.num_plays += 1
        self.save(update_fields=["num_plays"])

    def __str__(self):
        return f"{self.customer.user.get_full_name()} listened to '{self.playlist.title}' {self.num_plays} times"


class RemixHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    remix = models.ForeignKey(Remix, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)
    num_plays = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.customer.user.get_full_name()} listened to '{self.remix.title}' {self.num_plays} times"
