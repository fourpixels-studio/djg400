from django import forms
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
