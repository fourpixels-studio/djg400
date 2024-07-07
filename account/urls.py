from django.urls import path
from .views import account_signin, account_signout, account_signup

urlpatterns = [
    path("signin/", account_signin, name="account_signin"),
    path("signout/", account_signout, name="account_signout"),
    path("signup/", account_signup, name="account_signup"),
]