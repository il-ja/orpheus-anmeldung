from django import forms
from django.forms import ModelForm

from .models import Teilnahme


class DateInput(forms.DateInput):
    input_type = 'date'

class TeilnahmeForm(ModelForm):
    class Meta:
        model = Teilnahme
        fields = '__all__'
        widgets = {
            'geburtsdatum': DateInput(),
        }
