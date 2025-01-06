from .models import Customer
from django.utils import timezone
from django.contrib import messages
from seo_management.models import SEO
from newsletter.models import Newsletter
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .email import send_user_verification_email
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomerEditForm


def account_signin(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        context = {}
        seo = SEO.objects.get(pk=8)
        signin_form = AuthenticationForm(request, data=request.POST)
        
        if request.method == "POST":
            try:
                if signin_form.is_valid():
                    username = signin_form.cleaned_data.get("username")
                    password = signin_form.cleaned_data.get("password")
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, f"Welcome back, {user.get_full_name()}")
                        return redirect("index")
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
                    customer, created = Customer.objects.get_or_create(user=user)
                    login(request, user)
                    try:
                        subscription, created = Newsletter.objects.get_or_create(email=email)
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



@login_required(login_url='/account/signin/')
def account_profile(request, username):
    if username != request.user.username:
        return redirect("account_profile", request.user.username)
    user = User.objects.get(username=username)
    context = {
        "user": user,
        "title_tag": "My Profile",
    }
    return render(request, "account_profile.html", context)


@login_required(login_url='/account/signin/')
def edit_profile(request, username):
    if username != request.user.username:
        return redirect("edit_profile", request.user.username)
    if request.method == "POST":
        form = CustomerEditForm(request.POST, request.FILES, instance=request.user.customer, user=request.user)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect("account_profile", request.user.username)
            else:
                messages.error(request, 'Please correct the errors below.')
        except ValidationError as e:
            messages.error(request, f"Error: {', '.join(e.messages)}")
    else:
        form = CustomerEditForm(instance=request.user.customer, user=request.user)
    context = {
        "form": form,
        "title_tag": "Edit Profile",
    }
    return render(request, "edit_profile.html", context)


@login_required
def change_picture(request, username):
    if username != request.user.username:
        return redirect("change_picture", request.user.username)
    if request.method == 'POST':
        customer = request.user.customer
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            customer.profile_picture = profile_picture
            customer.save()
            messages.success(request, 'Profile picture updated successfully.')
        else:
            messages.error(request, 'Please select a valid image.')
    return redirect('edit_profile', request.user.username)


@login_required
def delete_picture(request, username):
    if username != request.user.username:
        return redirect("delete_picture", request.user.username)
    if request.method == 'POST':
        customer = request.user.customer
        if customer.profile_picture:
            customer.profile_picture.delete(save=False)
            customer.profile_picture = None
        if customer.square_thumbnail:
            customer.square_thumbnail.delete(save=False)
            customer.square_thumbnail = None
        customer.save()
        messages.success(request, 'Profile picture deleted successfully.')
    return redirect('edit_profile', request.user.username)
