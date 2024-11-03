from django import forms
from .models import Newsletter
from django.forms import ModelForm
from django_recaptcha.fields import ReCaptchaField


class NewsletterForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Newsletter
        fields = ('email', 'captcha')

    def clean_captcha(self):
        captcha_value = self.cleaned_data.get('captcha')
        if not captcha_value:
            raise forms.ValidationError("Please complete the captcha.")
        return captcha_value
