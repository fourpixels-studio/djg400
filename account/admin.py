from django.contrib import admin
from .models import Customer, Purchase, MixHistory, PlaylistHistory, RemixHistory
admin.site.register(Customer)
admin.site.register(Purchase)
admin.site.register(MixHistory)
admin.site.register(RemixHistory)
admin.site.register(PlaylistHistory)
