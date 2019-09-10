from django import forms
from django.forms import ModelForm

from django.core.mail import EmailMessage

from .models import Person


class WahlForm(ModelForm):
    class Meta:
        model = Person
        exclude = "vorname, nachname, code, seminarort".split(', ')

