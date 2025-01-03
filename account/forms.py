from django import forms
from .models import Customer
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField()
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'captcha',
            'username',
            'last_name',
            'password1',
            'password2',
            'first_name',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
        
    def clean_captcha(self):
        captcha_value = self.cleaned_data.get('captcha')
        if not captcha_value:
            raise forms.ValidationError("Please complete the captcha.")
        return captcha_value
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        return cleaned_data


class CustomerEditForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        label='Full Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    bio = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Tell us about yourself...'
        })
    )
    profile_picture = forms.ImageField(
        required=False,
        label='Profile Picture',
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Customer
        fields = ['bio', 'profile_picture']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['full_name'].initial = user.get_full_name()
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        customer = super().save(commit=False)
        user = self.instance.user
        user.first_name, user.last_name = self.cleaned_data['full_name'].split(
            ' ', 1)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            customer.save()
        return customer
