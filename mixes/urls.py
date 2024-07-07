from django.urls import path
from .views import mix_list


urlpatterns = [
    path("", mix_list, name="mix_list"),
]