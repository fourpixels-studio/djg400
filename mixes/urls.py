from django.urls import path
from .views import mix_list, audio_mix_detail, filtered_genres, filtered_albums, video_mix_list, video_mix_detail, search_mixes
from .utils import like_mix, reshare_mix

urlpatterns = [
    path("mixes/", mix_list, name="mix_list"),
    path("mix/<slug:slug>/", audio_mix_detail, name="audio_mix_detail"),
    path("mixes/genre/<slug:slug>/", filtered_genres, name="filtered_genres"),
    path("mixes/albums/<slug:slug>/", filtered_albums, name="filtered_albums"),
    path("mixes/videos/", video_mix_list, name="video_mix_list"),
    path("mixes/video/<slug:slug>/", video_mix_detail, name="video_mix_detail"),
    path("mixes/search/results/", search_mixes, name="search_mixes"),

    # utils
    path("mixes/like-mix/<slug:slug>/", like_mix, name="like_mix"),
    path("mixes/reshare-mix/<slug:slug>/", reshare_mix, name="reshare_mix"),
]
