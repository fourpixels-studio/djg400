from django.contrib import admin
from .models import Album, Genre, Mix
admin.site.register(Mix)
admin.site.register(Album)
admin.site.register(Genre)
