from django.contrib import admin
from .models import Album, Genre, Mix, Playlist
admin.site.register(Album)
admin.site.register(Genre)
admin.site.register(Mix)
admin.site.register(Playlist)