from .models import Newsletter
from django import forms
from django.forms import ModelForm

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('email',)