from django.urls import path
from .views import event_detail, event_list

urlpatterns = [
    path("", event_list, name="event_list"),
    path("<slug:slug>/", event_detail, name="event_detail"),
]
