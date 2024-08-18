from django.urls import path
from .views import mix_list, mix_detail, filtered_genres, filtered_albums, video_mix_list, video_mix_detail


urlpatterns = [
    path("", mix_list, name="mix_list"),
    path("audio/<slug:slug>/", mix_detail, name="mix_detail"),
    path("genre/<slug:slug>/", filtered_genres, name="filtered_genres"),
    path("albums/<slug:slug>/", filtered_albums, name="filtered_albums"),
    path("videos/", video_mix_list, name="video_mix_list"),
    path("videos/<slug:slug>/", video_mix_detail, name="video_mix_detail"),
]
