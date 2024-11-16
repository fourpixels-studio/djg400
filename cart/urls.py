from django.urls import path
from .views import cart, checkout

urlpatterns = [
    path("<slug:slug>/", cart, name="cart"),
    path("checkout/<slug:slug>/", checkout, name="checkout"),
]
