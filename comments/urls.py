from django.urls import path
from .views import comment_mix, comment_reply

urlpatterns = [
    path("new-comment/<int:pk>/", comment_mix, name="comment_mix"),
    path("new-reply/<int:pk>/", comment_reply, name="comment_reply"),
]
