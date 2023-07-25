from django import forms
from django.forms import ModelForm
from .models import Search

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255)