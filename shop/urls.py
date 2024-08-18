from django.urls import path
from .views import shop, view_product


urlpatterns = [
    path("", shop, name="shop"),
    path("<slug:slug>/", view_product, name="view_product"),
]
