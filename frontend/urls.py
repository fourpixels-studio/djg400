from django.urls import path
from .views import index, about, search


urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("search/results/", search, name="search"),
]
