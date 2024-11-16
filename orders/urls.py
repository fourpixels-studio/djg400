from django.urls import path
from .views import view_order

urlpatterns = [
    path("order/<str:order_number>/", view_order, name="view_order"),
]
