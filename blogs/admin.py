from .models import Blog
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin


class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


admin.site.register(Blog, BlogAdmin)
