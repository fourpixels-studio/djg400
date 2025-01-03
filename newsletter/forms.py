from django import forms
from django.forms import ModelForm
from .models import Newsletter, NewsletterArticle
from django_recaptcha.fields import ReCaptchaField
from django_summernote.widgets import SummernoteWidget


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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['captcha'].required = True


class UnsubscribeForm(forms.Form):
    captcha = ReCaptchaField()
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    def clean(self):
        cleaned_data = super().clean()
        captcha_value = cleaned_data.get('captcha')
        if not captcha_value:
            self.add_error('captcha', "Please complete the captcha.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['captcha'].required = True


class NewsletterArticleForm(forms.ModelForm):
    class Meta:
        model = NewsletterArticle
        fields = ['subject', 'content']

        widgets = {
            'content': SummernoteWidget(),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }
