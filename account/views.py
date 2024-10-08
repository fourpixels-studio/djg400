from django.contrib import messages
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout


def account_signin(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        context = {}

        signin_form = AuthenticationForm(request, data=request.POST)
        if request.method == "POST":
            try:
                if signin_form.is_valid():
                    username = signin_form.cleaned_data.get("username")
                    password = signin_form.cleaned_data.get("password")
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, f"Welcome back, {user}")
                        return redirect("index")
                else:
                    for field, errors in signin_form.errors.items():
                        for error in errors:
                            messages.error(request, error)
            except ValidationError as e:
                messages.error(request, f"Error: {' '.join(e.messages)}")

        context.update({
            "signin_form": signin_form,
            "title_tag": "Secure Login",
            "meta_keywords": "DJ G400, Sign In, Log In",
            "meta_description": "Log in to access exclusive releases, latest mixes, ad-free experienec and curated playlists.",
        })
        return render(request, "account_signin.html", context)


@login_required
def account_signout(request):
    logout(request)
    return redirect("account_signin")


def account_signup(request):
    if request.user.is_authenticated:
        return redirect("index")

    context = {}

    if request.method == "POST":
        register_user_form = CustomUserCreationForm(request.POST)
        try:
            if register_user_form.is_valid():
                user = register_user_form.save()
                username = register_user_form.cleaned_data.get('username')
                password = register_user_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Welcome, {username}! You have successfully signed up.")
                    return redirect("index")
                else:
                    messages.error(
                        request, "There was an error with authentication.")
            else:
                for field, errors in register_user_form.errors.items():
                    for error in errors:
                        messages.error(request, error)
        except ValidationError as e:
            messages.error(request, f"Error: {', '.join(e.messages)}")
    else:
        register_user_form = CustomUserCreationForm()

    context.update({
        "title_tag": "Create Account",
        "register_user_form": register_user_form,
        "meta_keywords": "DJ G400, Sign Up, Create Account",
        "meta_description": "Create your account to access exclusive releases, latest mixes, ad-free experience, and curated playlists.",
    })

    return render(request, "account_signup.html", context)
