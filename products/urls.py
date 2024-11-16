from django.urls import path
from .views import view_product, buy_product


urlpatterns = [
    path("buy-product", buy_product, name="buy_product"),
    path("<slug:product_category>/<slug:slug>/", view_product, name="view_product"),
]
