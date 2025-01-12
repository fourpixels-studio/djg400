from django.urls import path
from .utils import update_download_count
from .views import mix_list, filtered_genres, filtered_albums, mix_detail, support_mix, download_mix

urlpatterns = [
    path("mixes/", mix_list, name="mix_list"),
    path("support/mix/", support_mix, name="support_mix"),
    path("mix/<slug:slug>/", mix_detail, name="mix_detail"),
    path("mix/download/<slug:slug>/", download_mix, name="download_mix"),
    path("mixes/genre/<slug:slug>/", filtered_genres, name="filtered_genres"),
    path("mixes/albums/<slug:slug>/", filtered_albums, name="filtered_albums"),

    # utils
    path('download/update_download/', update_download_count, name='update_download_count'),
]
