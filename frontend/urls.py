from django.urls import path
# from .views import index, albums, event, blog_list, contact, elements, login, mix_detail
from .views import index


urlpatterns = [
    path("", index, name="index"),
    # path("albums/", albums, name="albums"),
    # path("event/", event, name="event"),
    # path("blogs/", blog_list, name="blog_list"),
    # path("contact/", contact, name="contact"),
    # path("elements/", elements, name="elements"),
    # path("login/", login, name="login"),
    # path("<slug:slug>/", mix_detail, name="mix_detail"),
]