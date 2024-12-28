from django.urls import path
from .utils import like_mix, reshare_mix
from .views import mix_list, filtered_genres, filtered_albums, mix_detail, support_mix

urlpatterns = [
    path("mixes/", mix_list, name="mix_list"),
    path("support/mix/", support_mix, name="support_mix"),
    path("mix/<slug:slug>/", mix_detail, name="mix_detail"),
    path("mixes/genre/<slug:slug>/", filtered_genres, name="filtered_genres"),
    path("mixes/albums/<slug:slug>/", filtered_albums, name="filtered_albums"),

    # utils
    path("mixes/like-mix/<slug:slug>/", like_mix, name="like_mix"),
    path("mixes/reshare-mix/<slug:slug>/", reshare_mix, name="reshare_mix"),
]
