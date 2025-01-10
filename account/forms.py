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
        


class CustomerEditForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Last Name',
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
        widget=forms.FileInput(attrs={'class': 'form-control-sm rounded-2 form-control'}),
    )
    delete_picture = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': ' form-check-input'}),
        label='Delete current picture',
    )

    class Meta:
        model = Customer
        fields = ['bio', 'profile_picture']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance.user.email != email:  # if the email is being changed
            if Customer.objects.filter(user__email=email).exists():
                raise forms.ValidationError("This email is already in use. Please choose a different one.")
        return email

    def save(self, commit=True):
        customer = super().save(commit=False)
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if self.cleaned_data.get('delete_picture'):
            self.instance.profile_picture.delete(save=False)
            self.instance.profile_picture = None
            self.instance.square_thumbnail.delete(save=False)
            self.instance.square_thumbnail = None
            super().save(commit=commit)
        if commit:
            user.save()
            customer.save()
        return customer

