from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


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
            except ValidationError as e:
                messages.error(request, f"Error: {' '.join(e.messages)}")

        context.update({
            "signin_form": signin_form,
            "title_tag": "Secure Login",
            "meta_description": "Log in to your Sibia account to access personalized healthcare solutions, AI-driven insights, and SDG research for improving community health.",
            "meta_keywords": "Sibia, login, secure access, healthcare account, medical AI, personalized healthcare, community health, SDG research",
        })
        return render(request, "account_signin.html", context)


@login_required
def account_signout(request):
    print(f"{request.user} logged out!")
    logout(request)
    return redirect("account_signin")


def account_signup(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        context = {}
        if request.method == "POST":
            register_user_form = CustomUserCreationForm(request.POST)
            if register_user_form.is_valid():
                user = register_user_form.save()
                username = register_user_form.cleaned_data.get('username')
                raw_password = register_user_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    login(request, user)
                    messages.success(
                        request, f"Welcome, {username}! You have successfully signed up.")
                    return redirect("index")
                else:
                    messages.error(
                        request, "There was an error with authentication.")
            else:
                messages.error(request, "There was an error with the form.")
        else:
            register_user_form = CustomUserCreationForm()

        context.update({
            "register_user_form": register_user_form,
            "title_tag": "Create Account",
            "meta_description": "Create your Sibia account to access personalized healthcare solutions, AI-driven insights, and SDG research for improving community health.",
            "meta_keywords": "Sibia, signin, secure access, healthcare account, medical AI, personalized healthcare, community health, SDG research",
        })
        return render(request, "account_signup.html", context)