from django.utils import timezone
from django.contrib import messages
from seo_management.models import SEO
from newsletter.models import Newsletter
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .email import send_user_verification_email
from django.core.exceptions import ValidationError
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout


def account_signin(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        context = {}
        seo = SEO.objects.get(pk=8)
        signin_form = LoginForm(request.POST)
        
        if request.method == "POST":
            try:
                if signin_form.is_valid():
                    email = signin_form.cleaned_data.get("email")
                    password = signin_form.cleaned_data.get("password")
                    try:
                        user = User.objects.filter(email=email).first()
                        username = user.username
                        user = authenticate(username=username, password=password)
                        if user is not None:
                            login(request, user)
                            messages.success(request, f"Welcome back, {user}")
                            return redirect("index")
                    except:
                        messages.error(request, f"The email {email} does not exist.")
                else:
                    for field, errors in signin_form.errors.items():
                        for error in errors:
                            messages.error(request, error)
            except ValidationError as e:
                messages.error(request, f"Error: {' '.join(e.messages)}")

        context.update({
            "signin_form": signin_form,
            "title_tag": seo.title_tag,
            "meta_keywords": seo.meta_keywords,
            "meta_description": seo.meta_description,
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
    seo = SEO.objects.get(pk=7)

    if request.method == "POST":
        register_user_form = CustomUserCreationForm(request.POST)
        try:
            if register_user_form.is_valid():
                email = register_user_form.cleaned_data.get('email')
                existing_email = User.objects.filter(email=email).first()
                if existing_email:
                    messages.error(request, "Oops! It seems like this email is already registered with us. If you’ve forgotten your password, you can reset it to regain access.")
                    return redirect("account_signup")
                user = register_user_form.save()
                username = register_user_form.cleaned_data.get('username')
                password = register_user_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    try:
                        subscription = Newsletter.objects.filter(email=email).first()
                        if subscription:
                            if subscription.consent == False:
                                subscription.resubscribed_at = timezone.now()
                                subscription.consent = True
                                subscription.save()
                        else:
                            subscription = Newsletter.objects.create(email=email)
                    except:
                        subscription = None
                    messages.success(request, f"Welcome aboard, {user.get_full_name()}! You are now 400 miles above the rest!")
                    send_user_verification_email(user)
                    return redirect("index")
                else:
                    messages.error(request, "There was an error with authentication.")
            else:
                if 'captcha' in register_user_form.errors:
                    messages.error(request, "Please complete the captcha.")
                else:
                    for field, errors in register_user_form.errors.items():
                        for error in errors:
                            messages.error(request, error)
        except ValidationError as e:
            messages.error(request, f"Error: {', '.join(e.messages)}")
    else:
        register_user_form = CustomUserCreationForm()

    context.update({
        "title_tag": seo.title_tag,
        "meta_keywords": seo.meta_keywords,
        "register_user_form": register_user_form,
        "meta_description": seo.meta_description,
    })

    return render(request, "account_signup.html", context)
