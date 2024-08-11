from django.urls import path
from .views import mix_list, filtered_genres, filtered_albums


urlpatterns = [
    path("", mix_list, name="mix_list"),
    path("genre/<slug:slug>/", filtered_genres, name="filtered_genres"),
    path("albums/<slug:slug>/", filtered_albums, name="filtered_albums"),
]
