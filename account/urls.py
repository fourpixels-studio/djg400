from .import utils as utils
from django.urls import path
from .views import account_signin, account_signout, account_signup

urlpatterns = [
    path("signin/", account_signin, name="account_signin"),
    path("signup/", account_signup, name="account_signup"),
    path("signout/", account_signout, name="account_signout"),
    path('like/mix/<int:mix_id>/', utils.like_mix, name='like_mix'),
    path('like/remix/<int:remix_id>/', utils.like_remix, name='like_remix'),
    path("mix/update_play/", utils.update_mix_play, name="update_mix_play"),
    path('like/playlist/<int:playlist_id>/', utils.like_playlist, name='like_playlist'),
    path('like/playlist/<int:playlist_id>/', utils.like_playlist, name='like_playlist'),
]
