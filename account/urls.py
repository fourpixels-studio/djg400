from .import utils as utils
from django.urls import path
from .views import account_signin, account_signout, account_signup, account_profile, edit_profile, change_picture, delete_picture

urlpatterns = [
    path("signin/", account_signin, name="account_signin"),
    path("signup/", account_signup, name="account_signup"),
    path("signout/", account_signout, name="account_signout"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path('like/mix/<int:mix_id>/', utils.like_mix, name='like_mix'),
    path("change-profile-picture/", change_picture, name="change_picture"),
    path("delete-profile-picture/", delete_picture, name="delete_picture"),
    path("mix/update_play/", utils.update_mix_play, name="update_mix_play"),
    path('like/remix/<int:remix_id>/', utils.like_remix, name='like_remix'),
    path("profile/<str:username>/", account_profile, name="account_profile"),
    path('like/playlist/<int:playlist_id>/', utils.like_playlist, name='like_playlist'),
    path('like/playlist/<int:playlist_id>/', utils.like_playlist, name='like_playlist'),
]
